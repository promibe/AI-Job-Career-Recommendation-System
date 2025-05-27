import streamlit as st
import requests

st.title("Resume Career Guidance Tester")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Analyze Resume"):
    if not uploaded_file:
        st.error("Please upload a resume file first.")
    else:
        # Read file bytes and send to backend as multipart/form-data
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        
        api_url = "http://127.0.0.1:8000/analyze_resume_file/"  # We will update backend for this endpoint
        
        try:
            response = requests.post(api_url, files=files)
            data = response.json()
            
            if response.status_code == 200:
                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success(f"Predicted Role: **{data['predicted_role']}**")
                    #st.write(f"Confidence: {data['confidence']:.2f}")
                    st.write(f"Certified Skills: {', '.join(data['certified_skills'])}")
                    st.write(f"Missing Skills: {', '.join(data['missing_skills'])}")
                    st.write(f"Skill Gap Percentage: {data['skill_gap_percentage']:.2f}%")
                    st.write(f"Status: {data['status']}")
            else:
                st.error("Failed to get a valid response from the backend.")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
