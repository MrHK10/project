import os
import django
import pandas as pd
from django.db.utils import IntegrityError
from django.utils import timezone

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_website.settings')

# Initialize Django
django.setup()

# Import the Job model from the dataglassdors app
from company.models import Job

def import_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    
    # Mapping between Excel column names and Job model fields
    column_mapping = {
        'Company Name': 'company_name',
        'Website': 'website',
        'Location': 'job_location',
        'Employees': 'employees',
        'Locations': 'locations',
        'Type': 'job_type',
        'Founded': 'founded',
        'Revenue': 'revenue',
        'Industry': 'industry',
        'All Location Info': 'all_location_info'
    }
    
    for index, row in df.iterrows():
        valid_fields = {}
        for column in df.columns:
            if column in column_mapping and not pd.isnull(row[column]):
                valid_fields[column_mapping[column]] = row[column]
     
        try:
            Job.objects.create(**valid_fields)
        except IntegrityError as e:
            print(f"Skipping duplicate entry for company: {valid_fields['company_name']}")
            # Optionally, you can handle or log the error here
            pass

def main():
    excel_file_path = 'excelfiles/Mergedfile2222.xlsx'
    import_data_from_excel(excel_file_path)

if __name__ == "__main__":
    main()
