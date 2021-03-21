import os
from pathlib import Path
from tempfile import TemporaryDirectory
import warnings

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
from pydicom.uid import generate_uid

import datetime
#import dateutil.relativedelta
from dateutil.relativedelta import *
import os


global folder_path
global second_folder_path

second_folder_path = "C:/Users/Jonathan/Documents/Projects/Caristo_Test/DICOM_utility/raw_data/different_birthdate_dicom_files/"
folder_path = "C:/Users/Jonathan/Documents/Projects/Caristo_Test/DICOM_utility/raw_data/cube_dicom_files/"

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
    
    
def set_current_dt_for_files_in_folder(folder_path):
    
    dt, current_date, current_time=get_datetime_obj()
    for patient in file_generator(folder_path):
        print(patient.ContentDate)
        print(patient.ContentTime)
        patient.ContentDate=current_date
        patient.ContentTime=current_time
    #print(patient.ContentDate)
    #print(patient.ContentTime)
    
    
    # print(os.path.join(directory, filename))
        
def set_patient_age_for_files_in_folder(folder_path):
    
    for patient in file_generator(folder_path):
        print(patient.PatientAge)
        set_patient_age(patient)
    
def set_patient_age(patient):
    print("In patient age")
    birth_date=patient.PatientBirthDate
    study_date=patient.StudyDate
    print("bd: " + birth_date)
    print("sd: "+study_date)
    patient_age=str(get_patient_age(birth_date,study_date))
    print("patient_age: " + patient_age)
    patient.PatientAge=patient_age
    
def get_patient_age(birth_date,study_date):
    birth_date=datetime.datetime(int(birth_date[:4]), int(birth_date[4:6]), int(birth_date[6:]))
    study_date=datetime.datetime(int(study_date[:4]), int(study_date[4:6]), int(study_date[6:]))
    
    time_difference = relativedelta(study_date,birth_date)
    return time_difference.years
    

if __name__=="__main__":
    set_current_dt_for_files_in_folder(folder_path)
    set_patient_age_for_files_in_folder(second_folder_path)