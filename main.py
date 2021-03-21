import pydicom
import os 
from pydicom.data import get_testdata_files
dir_path = os.path.dirname(os.path.realpath(__file__))
#w_dir=os.path.join(dir_path, "User/Desktop", "file.txt")
#raw_data_dir=os.path.join(dir_path, "User/Desktop", "file.txt")

# get some test data
raw_data = r"""C:\Users\Jonathan\Documents\Projects\Caristo_Test\DICOM_utility\raw_data\different_birthdate_dicom_files\image10_28021985.dcm"""
#get_testdata_files()
ds = pydicom.dcmread(raw_data)
patient_name=ds.PatientName
patient_sex=ds.PatientSex
patient_bd=ds.PatientBirthDate

ds.dir("pat")

patient_bd=19900525


print(ds)
print(ds.PatientName)