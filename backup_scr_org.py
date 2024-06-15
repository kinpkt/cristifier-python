import streamlit as st
from io import BytesIO
import requests
import tempfile
import zipfile
import os

WCA_API_URL = 'https://www.worldcubeassociation.org/api/v0/competitions'

def extract_zip(zip_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(temp_dir)
            return temp_dir

def extract_scrambles(temp_dir, comp_name):
    inner_zip_path = None
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file == f'{comp_name} - Computer Display PDFs.zip':
                inner_zip_path = os.path.join(root, file)
                break
        if inner_zip_path:
            break
    
    if inner_zip_path:
        with zipfile.ZipFile(inner_zip_path, 'r') as zf:
            inner_temp_dir = tempfile.mkdtemp()
            zf.extractall(inner_temp_dir)
            return inner_temp_dir
    else:
        raise FileNotFoundError(f'{comp_name} - Computer Display PDFs.zip not found in the extracted ZIP file.')

def get_wcif(comp_id):
    response = requests.get(f'{WCA_API_URL}/{comp_id}/wcif/public')
    wcif = response.json()
    return wcif

def organize(temp_dir, schedule):
    with tempfile.TemporaryDirectory() as reorganized_dir:
        for room in schedule['venues'][0]['rooms']:
            st.write(room)
            room_dir = os.path.join(reorganized_dir, room['name'])
            os.makedirs(room_dir, exist_ok=True)
    return None

with st.form('scr_org'):
    st.header('Scramble Organizer')
    comp_id = st.text_input('Competition ID')
    scr_upload = st.file_uploader('Scrambles File', type='zip')
    submitted_src_org = st.form_submit_button('Submit')

    if submitted_src_org and scr_upload and comp_id != '':
        stringio_zip = BytesIO(scr_upload.getvalue())
        temp_dir = extract_zip(stringio_zip)
        wcif = get_wcif(comp_id)
        schedule = wcif['schedule']
        temp_scr_dir = extract_scrambles(temp_dir, wcif['name'])
    
        reorganized_scr = organize(temp_dir, schedule)
        st.write(wcif['schedule'])