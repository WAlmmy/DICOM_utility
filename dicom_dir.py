import os
from pathlib import Path
from tempfile import TemporaryDirectory
import warnings

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
from pydicom.uid import generate_uid

import datetime











import os

# Set current date/time
dt = datetime.datetime.now()

current_date= dt.strftime('%Y%m%d')
current_time = dt.strftime('%H%M%S')
print(current_date)
print(current_time)




folder_path = "C:/Users/Jonathan/Documents/Projects/Caristo_Test/DICOM_utility/raw_data/cube_dicom_files/"

for file_name in os.listdir(folder_path):
    if file_name.endswith(".dcm"): 
        file_path=os.path.join(folder_path,file_name)
        patient = dcmread(file_path)
        print(patient.ContentDate)
        print(patient.ContentTime)
        patient.ContentDate=current_date
        patient.ContentTime=current_time
        #print(patient.ContentDate)
        #print(patient.ContentTime)
        
        patient.save_as(file_path)
        # print(os.path.join(directory, filename))


