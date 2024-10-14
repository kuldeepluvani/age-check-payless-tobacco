"""
@ANSI636014090102DL00410278ZC03190024DLDAQY3503753DCSBARBIERIDDENDACNICOLASDDFNDADNONEDDGNDCACDCBNONEDCDNONEDBD01102019DBB09111994DBA09112020DBC1DAU070 INDAYGRNDAG1927 17TH TDAISANTAMONICADAJCADAK904040000CF10/6/201561638/BBFD/20DCGUSADAW184DAZBRODCK19010Y35037530401DDANDDB08292017ZCZCAGRNZCBBRNZCCZCD
"""
import re
from datetime import datetime
import streamlit as st
import csv
from pathlib import Path

# Helper function to append data to a CSV file
def log_to_csv(log_data):
    log_file_path = 'log.csv'
    file_exists = Path(log_file_path).exists()
    with open(log_file_path, 'a', newline='') as csvfile:
        headers = ['Timestamp', 'ID Number', 'Date of Birth', 'Age']
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        if not file_exists:
            writer.writeheader()  # Write header only once

        writer.writerow(log_data)

def extract_dob(text):
    """Extracts the date of birth (DOB) from the driver's license text."""
    pattern = r'DBB(\d{8})'
    match = re.search(pattern, text)
    if match:
        dob_str = match.group(1)
        try:
            dob = datetime.strptime(dob_str, '%m%d%Y')
            return dob
        except ValueError as e:
            st.error(f"Date conversion error: {e}")
            return None
    return None

def extract_id(text):
    """Extracts the ID number following 'DLDAQ' that starts with 'Y' and is followed by seven digits."""
    match = re.search(r'DLDAQ(Y\d{7})', text)
    return match.group(1) if match else None

def calculate_age(dob):
    """Calculates the age given a date of birth."""
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def display_age_check(dob, age):
    """Displays a large green check or red X based on age, with the age number displayed in large font next to the symbol."""
    if age >= 21:
        symbol = "✔️"
        color = "green"
    else:
        symbol = "❌"
        color = "red"

    html_content = f"<span style='font-size: 150pt; color: {color};'>{symbol}</span> <span style='color: {color};'>Age: </span><span style='font-size: 150pt; color: {color};'>{age}</span><br>"
    html_content += f"<span style='font-size: 50pt; color: {color};'>Birthdate: {dob.strftime('%B %d, %Y')}</span>"
    st.markdown(html_content, unsafe_allow_html=True)

st.title('Driver\'s License DOB Extractor and Age Calculator')
text_input = st.text_area("Enter scanned text data containing DBB<YYYYMMDD>:", height=150, max_chars=1000, key="text_input")

def clear_text():
    st.session_state.text_input = ""

if st.button("Clear", on_click=clear_text):
    clear_text()

if text_input:
    dob = extract_dob(text_input)
    if dob:
        age = calculate_age(dob)
        id_number = extract_id(text_input)
        if id_number:
            # Log the data
            log_data = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ID Number': id_number,
                'Date of Birth': dob.strftime('%Y-%m-%d'),
                'Age': age
            }
            log_to_csv(log_data)
        display_age_check(dob, age)
    else:
        st.error('DOB not found in the text data or invalid format.')