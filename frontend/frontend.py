import streamlit as st
import requests

st.title("Resume Career Job Filter")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Submit Resume"):
    if not uploaded_file:
        st.error("Please upload a resume file first.")
    else:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        api_url = "http://127.0.0.1:8000/analyze_resume_file/"

        try:
            response = requests.post(api_url, files=files)
            if response.status_code == 200:
                data = response.json()
                if data['predicted_role'] == 'NOT_A_RESUME':
                    st.warning("Kindly Upload a Resume, What you Uploaded isn't a Resume")
                else:
                    st.success("Resume uploaded successfully, we shall get back to you soon.")
            else:
                st.error("Upload failed. Please try again.")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
