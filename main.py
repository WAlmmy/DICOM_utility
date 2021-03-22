import click
#import * from utils.dicom_utils
#from dicom_utils import dicom_utils


import os, sys
from pathlib import Path
from tempfile import TemporaryDirectory
import warnings

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
from pydicom.uid import generate_uid
from pydicom_PIL import show_PIL
import matplotlib.pyplot as plt

import datetime
#import dateutil.relativedelta
from dateutil.relativedelta import *



def get_datetime_obj():
    # Set current date/time
    dt = datetime.datetime.now()
    
    current_date= dt.strftime('%Y%m%d')
    current_time = dt.strftime('%H%M%S')
    print(current_date)
    print(current_time)
    return dt, current_date, current_time



def file_generator(folder_path):
    """

    Parameters
    ----------
    folder_path : string
        this opens each file in a directory to be editted.
        on next, file is written

    Returns
    -------
    None.

    """
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".dcm"): 
            file_path=os.path.join(folder_path,file_name)
            patient = dcmread(file_path)
            yield patient
            
            patient.save_as(file_path)
    
    
def set_current_dt_for_files_in_folder(folder_path,print_patient):
    
    dt, current_date, current_time=get_datetime_obj()
    for patient in file_generator(folder_path):
        #print(patient.ContentDate)
        #print(patient.ContentTime)
        patient.ContentDate=current_date
        patient.ContentTime=current_time
        patient_data_output_control(patient,print_patient)
    #print(patient.ContentDate)
    #print(patient.ContentTime)
    
    
    # print(os.path.join(directory, filename))
        
def set_patient_age_for_files_in_folder(folder_path,print_patient):
    
    for patient in file_generator(folder_path):
        set_patient_age(patient)
        patient_data_output_control(patient,print_patient)
    
def set_patient_age(patient):
    #print("In patient age")
    birth_date=patient.PatientBirthDate
    study_date=patient.StudyDate
    #print("bd: " + birth_date)
    #print("sd: "+study_date)
    patient_age=str(get_patient_age(birth_date,study_date))
    #print("original patient age: " + patient_age)
    patient.Age=patient_age
    #print("new patient age: " + patient_age)
    
def get_patient_age(birth_date,study_date):
    birth_date=datetime.datetime(int(birth_date[:4]), int(birth_date[4:6]), int(birth_date[6:]))
    study_date=datetime.datetime(int(study_date[:4]), int(study_date[4:6]), int(study_date[6:]))
    
    time_difference = relativedelta(study_date,birth_date)
    return time_difference.years
    

def patient_data_output_control(patient,print_patient):    
    if print_patient:
        print(patient)

def print_patient_data(file_path,print_patient):
    patient = dcmread(file_path)
    patient_data_output_control(patient, print_patient)
    
def show_patient_image(item_path):
    
    #ds = read_file(item_path)
    patient=dcmread(item_path)
    #show_PIL(ds)
    show_PIL(patient)
    print("Showing patient image")
    
    #plt.imshow(patient.pixel_array,cmap=plt.cm.bone)
    return(patient)
    
def modify_patient_data(file_path, name="", sex="", birth_date=""):
    patient = dcmread(file_path)
    if name:
        patient.PatientName=name
    if sex:
        patient.PatientSex=sex
    if  birth_date:
        patient.PatientBirthDate=birth_date
    patient.save_as(file_path)
    return patient
    
def parse_input(input_str):
    if input_str=="Y":
        input_bool=True
    elif input_str=="N":
        input_bool=False
    elif not input_str:
        input_bool=False
    else:
       raise ValueError("Unidentified value set")
    return input_bool


@click.command()
@click.option('--p_name', default='', help='Patient\'s name')
@click.option('--p_birth_date', default='', help='Patient\'s birth date')
@click.option('--p_sex', default='', help='Patient\'s sex')
@click.option('--set_datetime', default='N', help='Y/N sets content date and \
              time to current datetime')
@click.option('--set_age', default='N', help='Set patient\'s age at time of \
              scan')
@click.option('--display_image', default='N', help='Display image')
@click.option('--print_patient', default='N', help='Y/N prints patient\'s data\
              after modification')
@click.argument('item_path')             
def main(p_name,p_birth_date,p_sex,set_datetime,set_age,display_image,print_patient,item_path):
    set_datetime=parse_input(set_datetime)
    set_age=parse_input(set_age)
    print_patient=parse_input(print_patient)
    display_image=parse_input(display_image)
      
    print("parsed input")
    print_flag=False
    patient=None
    if print_patient:
        print_flag=True
        print("print flage set")
    if p_name or p_sex or p_birth_date:
        print("modifying data")
        print(print_patient)
        patient=modify_patient_data(item_path, name=p_name, sex=p_sex,
                            birth_date=p_birth_date)
        print_flag=False
    if set_age:
        print("Setting age")
        set_patient_age_for_files_in_folder(item_path,print_patient)
        print_flag=False
    if set_datetime:
        print("Setting datetime")
        set_current_dt_for_files_in_folder(item_path,print_patient)
        print_flag=False
    if display_image:
        patient=show_patient_image(item_path)
        print_flage=False
    if print_flag and not patient:
            patient = dcmread(item_path)
    if patient:
        patient_data_output_control(patient,print_patient)
    
    
if __name__=="__main__":
    main()