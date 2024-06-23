import os

# Install xlsxwriter if not already installed
try:
    import xlsxwriter
except ImportError:
    os.system('pip install xlsxwriter')

import streamlit as st
import pandas as pd
from datetime import date

#Function to create and download the excel file
def create_excel(subject, shift, selected_date, submitted_roll_numbers, not_submitted_roll_numbers):
    file_name = f"{subject}_{shift}_{selected_date}.xlsx"
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Create dataframe
    max_len = max(len(submitted_roll_numbers), len(not_submitted_roll_numbers))
    submitted_roll_numbers.extend([''] * (max_len - len(submitted_roll_numbers)))
    not_submitted_roll_numbers.extend([''] * (max_len - len(not_submitted_roll_numbers)))
    
    data = {
        'Submitted': submitted_roll_numbers,
        'Not Submitted': not_submitted_roll_numbers
    }
    
    df = pd.DataFrame(data)

    # Write dataframe to a single worksheet
    df.to_excel(writer, sheet_name='Submission', index=False)

    # Close the Pandas Excel writer and output the Excel file
    writer.close()

    return file_name


#Streamlit app
st.title('Submission Tracker')


selected_date = st.date_input('Select Date', date.today())
day_of_week = st.selectbox('Select Day', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
subject = st.selectbox('Select Subject', ['Maths Book', 'English Book', 'Maths Copy', 'English Copy', 'Drawing', 'Craft'])

shift = st.selectbox('Select Shift', ['Morning Shift', 'Day Shift'])

if shift == 'Morning Shift':
    roll_numbers = list(range(1, 11))
else:
    roll_numbers = list(range(1, 16))

st.write('Select the roll numbers of students who have submitted:')
submitted_roll_numbers = []
for roll_number in roll_numbers:
    if st.checkbox(f"Roll Number {roll_number}"):
        submitted_roll_numbers.append(roll_number)

#Calculate not submitted roll numbers
not_submitted_roll_numbers = [rn for rn in roll_numbers if rn not in submitted_roll_numbers]

if st.button('Submit'):
    file_name = create_excel(subject, shift, selected_date, submitted_roll_numbers, not_submitted_roll_numbers)
    with open(file_name, 'rb') as f:
        st.download_button('Download Excel File', f, file_name)
