import os.path
from os.path import dirname, join
from pprint import pprint

import pydicom
from pydicom.data import get_testdata_files
from pydicom.filereader import read_dicomdir




#pydicom.config.datetime_conversion= True

# fetch the path to the test data
#filepath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"/raw_data", "/cube_dicom_files/")
#filepath=os.path.abspath("C:\Users\Jonathan\Documents\Projects\Caristo_Test\DICOM_utility\raw_data\cube_dicom_files")


filepath = "C:/Users/Jonathan/Documents/Projects/Caristo_Test/DICOM_utility/raw_data/cube_dicom_files/"
#filepath = r"""C:\Users\Jonathan\Documents\Projects\Caristo_Test\DICOM_utility\raw_data\cube_dicom_files\ """
filepath=filepath.replace("\\","/")
print('Path to the DICOM directory: {}'.format(filepath))
# load the data
dicom_dir = read_dicomdir(filepath)
base_dir = dirname(filepath)



# Set current date/time
dt = datetime.datetime.now()

current_date= dt.strftime('%Y%m%d')
current_time = dt.strftime('%H%M%S')


# go through the patient record and print information
for patient_record in dicom_dir.patient_records:
    patient_record.ContentDate=current_date
    patient_record.ContentTime=current_time







# fetch the path to the test data
path = r"""C:\Users\Jonathan\Documents\Projects\Caristo_Test\DICOM_utility\raw_data\cube_dicom_files"""
ds = dcmread(path)
root_dir = Path(ds.filename).resolve().parent
print(f'Root directory: {root_dir}\n')




# Iterate through the PATIENT records
for patient in ds.patient_records:
    patient.ContentDate=current_date
    patient.ContentTime=current_time
    