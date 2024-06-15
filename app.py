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
    returner_pdf_path, first_timer_pdf_path = gen.generate_pdf(comp_id, finished_data)

    st.write('Click the links below to download the generated PDF files.')

    with open(returner_pdf_path, "rb") as returner_pdf_file:
        st.download_button(
            label="Download Returner PDF",
            data=returner_pdf_file.read(),
            file_name="returner.pdf",
            mime="application/pdf"
        )

    with open(first_timer_pdf_path, "rb") as first_timer_pdf_file:
        st.download_button(
            label="Download First Timer PDF",
            data=first_timer_pdf_file.read(),
            file_name="first_timer.pdf",
            mime="application/pdf"
        )
    