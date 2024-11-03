import pandas as pd

# Helper function to match controls for a single case
def match_controls(case, control_df, used_ids, age_tolerance, num_controls):
    matched_controls = control_df[
        (control_df['gender'] == case['gender']) &
        (control_df['age'] >= case['condition_start_age'] - age_tolerance) &
        (control_df['age'] <= case['condition_start_age'] + age_tolerance) &
        (~control_df['person_id'].isin(used_ids))
    ]

    # Sort by age difference, prioritizing positive then closest negative
    matched_controls['age_difference'] = matched_controls['age'] - case['condition_start_age']
    positive_age_diff = matched_controls[matched_controls['age_difference'] >= 0].sort_values('age_difference').head(num_controls)
    negative_age_diff = matched_controls[matched_controls['age_difference'] < 0].sort_values('age_difference', key=abs).head(num_controls - len(positive_age_diff))

    prioritized_controls = pd.concat([positive_age_diff, negative_age_diff]).head(num_controls)
    prioritized_controls = prioritized_controls.drop(columns='age_difference')

    return prioritized_controls

def match_controls_to_cases(control_df, dementia_df, 
                            dementia_age_cutoff_lower=45, dementia_age_cutoff_higher=85, 
                            num_controls=25, age_tolerance=1):
    """
    Matches controls to dementia cases based on gender and age criteria.
    
    Parameters:
    - control_df (DataFrame): Dataframe with all control data.
    - dementia_df (DataFrame): Dataframe with dementia cases to match on.
    - dementia_age_cutoff_lower (int): Minimum age for dementia cases to consider.
    - dementia_age_cutoff_higher (int): Maximum age for dementia cases to consider.
    - num_controls (int): Number of controls to match per case.
    - age_tolerance (int): Age tolerance in years for matching controls to cases.
    
    Returns:
    - pd.DataFrame: A DataFrame with matched controls for each dementia case.
    """
    control_df['diagnosis'] = 0

    # Filter dementia cases based on age range
    dementia_df_considered = dementia_df[
        (dementia_df['condition_start_age'] > dementia_age_cutoff_lower) &
        (dementia_df['condition_start_age'] < dementia_age_cutoff_higher)
    ].reset_index(drop=True)

    

    # Initialize the matched DataFrame and set for used IDs
    matched_df = pd.DataFrame()
    used_ids = set()

    # Perform matching for each dementia case
    for _, case in dementia_df_considered.iterrows():
        matched_controls = match_controls(case, control_df, used_ids, age_tolerance, num_controls)
        used_ids.update(matched_controls['person_id'])  # Track used controls to avoid duplicates
        matched_df = pd.concat([matched_df, matched_controls])

    # Reset index in the final matched DataFrame
    matched_df.reset_index(drop=True, inplace=True)
    
    return matched_df

