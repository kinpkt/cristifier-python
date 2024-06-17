import pdf_generator as gen
import streamlit as st
from logic import *

st.title('Cristifier')

with st.form('reg_paper'):
    st.header('Registration Paper')
    comp_id = st.text_input('Competition ID')
    submitted_reg_paper = st.form_submit_button('Submit')
    
if submitted_reg_paper and comp_id:
    wcif = get_wcif(comp_id)
    finished_data = sort_competitors(wcif)
    merged_pdf_path = gen.generate_pdf(comp_id, finished_data)

    st.write('Click the button below to download the generated PDF file.')

    print(merged_pdf_path)

    with open(merged_pdf_path, 'rb') as merged_pdf_file:
        st.download_button(
            label=f'Download {finished_data[0]} PDF',
            data=merged_pdf_file.read(),
            file_name=f'{comp_id}-reg-table-all.pdf',
            mime='application/pdf'
        )
    