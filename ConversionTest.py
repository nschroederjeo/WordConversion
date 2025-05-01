import streamlit as st
from docx import Document
from io import BytesIO

# Replacement dictionary
replace_dict = {
    "minutes": "Minutes",
    "seconds": "Seconds",
    "feet": "feet;"
}

st.title("DOCX Word Replacer")

uploaded_file = st.file_uploader("Upload a Word (.docx) file", type="docx")

if uploaded_file:
    document = Document(uploaded_file)
    changes_made = False

    for para in document.paragraphs:
        for key, value in replace_dict.items():
            if key in para.text:
                st.write(f"Replacing '{key}' with '{value}' in: {para.text}")
                para.text = para.text.replace(key, value)
                changes_made = True

    if changes_made:
        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="Download modified file",
            data=buffer,
            file_name="modified.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.info("No matches found for replacement.")