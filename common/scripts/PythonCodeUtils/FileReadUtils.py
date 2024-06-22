from io import TextIOWrapper
from django.core.files.uploadedfile import UploadedFile
import pandas as pd

# csv_file_obj = self.request.FILES['csv_file']
def read_csv_file2df(csv_file_obj:UploadedFile,
                     encoding:str = 'cp932') -> pd.DataFrame:
    csv_file_data = TextIOWrapper(csv_file_obj.file, encoding=encoding)
    return pd.read_csv(csv_file_data)