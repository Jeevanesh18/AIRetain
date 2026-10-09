import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path='dataset.xlsx'):
    # Load all sheets
    employees = pd.read_excel(file_path, sheet_name='Employees')
    onboarding = pd.read_excel(file_path, sheet_name='Onboarding_Survey')
    pulse = pd.read_excel(file_path, sheet_name='Pulse_Survey')
    exit_survey = pd.read_excel(file_path, sheet_name='Exit_Survey')
    actions = pd.read_excel(file_path, sheet_name='Action_Tracker')

    # Standardise Exit Survey ID column to match others
    if 'Employee_ID' in exit_survey.columns:
        exit_survey = exit_survey.rename(columns={'Employee_ID': 'employee_id'})

    # Merge demographics (Division, Location, Status) into the surveys
    demographics = employees[['employee_id', 'division', 'location', 'exit_status', 'employee_group']]
    
    onboarding_merged = pd.merge(onboarding, demographics, on=['employee_id', 'division', 'employee_group'], how='left')
    pulse_merged = pd.merge(pulse, demographics, on='employee_id', how='left')
    exit_merged = pd.merge(exit_survey, demographics, on='employee_id', how='left')

    return employees, onboarding_merged, pulse_merged, exit_merged, actions