import pandas as pd
from datetime import timedelta
import numpy as np

# Function to check if a person has dementia phenotype
def has_dementia_phenotype(group):
    dates = group['condition_start_date'].drop_duplicates().sort_values()
    for i in range(len(dates)):
        for j in range(i + 1, len(dates)):
            if dates.iloc[j] <= dates.iloc[i] + timedelta(days=365):  # Check if within 12 months
                return True
    return False

def process_dementia_data(path_to_dementia_file, path_to_demographics_file):
    """
    Process dementia and demographic data to identify individuals with a dementia phenotype
    and calculate their age at the start of the condition.

    Parameters:
    - path_to_dementia_file (str): Path to the dementia diagnosis code CSV file.
    - path_to_demographics_file (str): Path to the demographics CSV file.

    Returns:
    - pd.DataFrame: A DataFrame with individuals who meet the dementia phenotype criteria,
                    including their demographic details and age at the condition start date.
    """
    # Read data files
    dementia_df = pd.read_csv(path_to_dementia_file)
    dem_df = pd.read_csv(path_to_demographics_file)
    dem_df['DOB'] = dem_df.apply(lambda x: str(x['year_of_birth'])+'-'+str(x['month_of_birth'])+\
                                       '-'+str(x['day_of_birth']),axis = 1)

    # Convert condition start date to datetime and sort values
    dementia_df['condition_start_date'] = pd.to_datetime(dementia_df['condition_start_date'])
    dementia_df = dementia_df.sort_values(['person_id', 'condition_start_date'])

    # Group data by person_id
    dementia_groups = dementia_df.groupby('person_id')

    # Filter person_ids with dementia phenotype
    dementia_person_ids = dementia_groups.filter(has_dementia_phenotype)['person_id'].unique()
    dementia_pdf = dementia_df[dementia_df['person_id'].isin(dementia_person_ids)].reset_index(drop=True)

    # Retain only the first occurrence for each person
    dementia_pdf = dementia_pdf.sort_values(['person_id', 'condition_start_date']).drop_duplicates(subset=['person_id'], keep='first')

    # Merge with demographic data
    dementia_pdf = dementia_pdf.merge(dem_df[['person_id', 'DOB', 'gender']], on='person_id')
    dementia_pdf['DOB'] = pd.to_datetime(dementia_pdf['DOB'])
    dementia_pdf['condition_start_date'] = pd.to_datetime(dementia_pdf['condition_start_date'])

    # Calculate age at condition start
    dementia_pdf['condition_start_age'] = (dementia_pdf['condition_start_date'] - dementia_pdf['DOB']).apply(lambda x: x.days // 365.24)

    return dementia_pdf, list(set(dementia_df['person_id']))



