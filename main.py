import click
#import * from utils.dicom_utils
#from dicom_utils import dicom_utils


import os, sys


from pydicom import dcmread
from pydicom_PIL import show_PIL

import datetime
#import dateutil.relativedelta
from dateutil.relativedelta import *



def get_datetime_obj():
    """
    Returns
    -------
    dt : DateTime Object
        Current time.
    current_date : String
        Current date.
    current_time : STRING
        Current time.

    """
    # Set current date/time
    dt = datetime.datetime.now()
    
    current_date= dt.strftime('%Y%m%d')
    current_time = dt.strftime('%H%M%S')
    return dt, current_date, current_time



def file_generator(folder_path):
    """
    Parameters
    ----------
    folder_path : string.
        this opens each file in a directory to be editted.
        on next, file is written.

    Yields
    -------
    patient : FileDataset
        pydicom object to r/w files.
    """
    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".dcm"): 
                file_path=os.path.join(folder_path,file_name)
                patient = open_file_safely(file_path)
                yield patient
                
                patient.save_as(file_path)
    except:
        print("Could not parse folder:" + folder_path + 
              "\nThis is often caused by entering a filename, instead of folder")
        sys.exit()
    
    
def set_current_dt_for_files_in_folder(folder_path,print_patient):
    """
    Parameters
    ----------
    folder_path : STRING
        Folder path.
    print_patient : BOOLEAN
        Controls whether to print patient details

    Returns
    -------
    None.

    """
    
    dt, current_date, current_time=get_datetime_obj()
    for patient in file_generator(folder_path):
        patient.ContentDate=current_date
        patient.ContentTime=current_time
        patient_data_output_control(patient,print_patient)

        
def set_patient_age_for_files_in_folder(folder_path,print_patient):
    """
    Parameters
    ----------
    folder_path : STRING
        Folder path
    print_patient : BOOLEAN
        Controls whether to print patient details

    Returns
    -------
    None.

    """
    for patient in file_generator(folder_path):
        set_patient_age(patient)
        patient_data_output_control(patient,print_patient)
    
def set_patient_age(patient):
    """
    Parameters
    ----------
    patient : FileDataset
        pydicom object to r/w files.

    Returns
    -------
    None.

    """
    birth_date=patient.PatientBirthDate
    study_date=patient.StudyDate
    patient_age=str(get_patient_age(birth_date,study_date))
    patient.Age=patient_age
    
def get_patient_age(birth_date,study_date):
    """
    Parameters
    ----------
    birth_date : STRING
        Birth date in YYYYMMDD format
    study_date: STRING
        Study date in YYYYMMDD format

    Returns
    -------
    time_difference.years : INTEGER
        The time difference in years from the birth_date to study_date

    """
    birth_date=datetime.datetime(int(birth_date[:4]), int(birth_date[4:6]), int(birth_date[6:]))
    study_date=datetime.datetime(int(study_date[:4]), int(study_date[4:6]), int(study_date[6:]))
    
    time_difference = relativedelta(study_date,birth_date)
    return time_difference.years
    

def patient_data_output_control(patient,print_patient):  
    """
    Parameters
    ----------
    patient : FileDataset
        pydicom object to r/w files.
    print_patient : BOOLEAN
        Whether to print patient date.

    Returns
    -------
    None

    """
    if print_patient:
        print(patient)

def print_patient_data(file_path,print_patient):
    
    patient = open_file_safely(file_path)
    patient_data_output_control(patient, print_patient)
    
def show_patient_image(file_path):
    """
    Parameters
    ----------
    file_path : STRING
        File path to be read.

    Returns
    -------
    patient : FileDataset
        pydicom object to r/w files.
    """
    
    patient=open_file_safely(file_path)
    show_PIL(patient)
    return(patient)
    
def modify_patient_data(file_path, name="", sex="", birth_date=""):
    """
    Parameters
    ----------
    file_path : STRING
        File path to be read.
    name : STRING
        Patient name.
    sex : STRING
        Patient sex as "0" or "1"
    birth_date : "STRING"
        Patient birth_date as STRING in YYYYMMDD format
    Returns
    -------
    patient : FileDataset
        pydicom object to r/w files.
    """
    patient = open_file_safely(file_path)
    if name:
        patient.PatientName=name
    if sex:
        patient.PatientSex=sex
    if  birth_date:
        patient.PatientBirthDate=birth_date
    patient.save_as(file_path)
    return patient
    
def parse_input(input_str):
    """

    Parameters
    ----------
    input_str : STRING
        'Y' or 'N'.

    Raises
    ------
    ValueError
        This is thrown if any string other than 'Y', or 'N' input.

    Returns
    -------
    input_bool : BOOLEAN
        BOOLEAN output, True for input _str =="Y" else, False

    """
    if input_str=="Y":
        input_bool=True
    elif input_str=="N":
        input_bool=False
    elif not input_str:
        input_bool=False
    else:
        input_bool=False
        raise ValueError("Unidentified value set. Only (Y/N) accepted.")
    return input_bool

def open_file_safely(file_path):
    """
    This function takes a file path and opens it while handling errors with \
        permissions. This issue is most common when a user inputs a folder as \
            a file.
    """
    print("Opening file")
    try:
        patient = dcmread(file_path)
    except:
        print("Could not open/read file:", file_path)
        sys.exit()
    
    return patient
    

@click.command()
@click.option('--p_name', default='', help='Patient\'s name')
@click.option('--p_birth_date', default='', help='Patient\'s birth date')
@click.option('--p_sex', default='', help='Patient\'s sex')
@click.option('--set_datetime', default='N', 
              help='Y/N sets content date and time to current datetime')
@click.option('--set_age', default='N', 
              help='Set patient\'s age at time of scan')
@click.option('--display_image', default='N', help='Display image')
@click.option('--print_patient', default='N', 
              help='Y/N prints patient\'s data after modification')
@click.argument('item_path')             
def main(p_name,p_birth_date,p_sex,set_datetime,set_age,display_image,print_patient,item_path):
    set_datetime=parse_input(set_datetime)
    set_age=parse_input(set_age)
    print_patient=parse_input(print_patient)
    display_image=parse_input(display_image)
      
    
    print_flag=False
    patient=None
    if print_patient:
        print_flag=True
        
    if p_name or p_sex or p_birth_date:
        patient=modify_patient_data(item_path, name=p_name, sex=p_sex,
                            birth_date=p_birth_date)
        print_flag=False
    if set_age:
        set_patient_age_for_files_in_folder(item_path,print_patient)
        print_flag=False
    if set_datetime:
        set_current_dt_for_files_in_folder(item_path,print_patient)
        print_flag=False
    if display_image:
        patient=show_patient_image(item_path)
        print_flage=False
    if print_flag and not patient:
            patient = open_file_safely(item_path)
    if patient:
        patient_data_output_control(patient,print_patient)
    
    
if __name__=="__main__":
    main()