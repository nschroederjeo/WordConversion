import streamlit as st
from docx import Document
from io import BytesIO
import os
import zipfile
import re

# Replacement dictionary
replace_dict = {
    "minutes": "Minutes",
    "seconds": "Seconds",
    "feet": "feet;"
}

st.title("Batch DOCX Word Replacer")

uploaded_files = st.file_uploader(
    "Upload one or more Word (.docx) files", type="docx", accept_multiple_files=True
)

if uploaded_files:
    modified_files = []

    for uploaded_file in uploaded_files:
        document = Document(uploaded_file)
        changes_made = False

        for para in document.paragraphs:
            for key, value in replace_dict.items():
                if key in para.text:
                    st.write(f"Replacing '{key}' with '{value}' in {uploaded_file.name}: {para.text}")
                    # Inside your loop:
                    if key == "feet":
                        # Only replace 'feet' when NOT followed by a semicolon
                        new_text = re.sub(r'\bfeet\b(?!;)', value, para.text)
                    else:
                        new_text = para.text.replace(key, value)
                    
                    if para.text != new_text:
                        para.text = new_text
                    changes_made = True

        if changes_made:
            buffer = BytesIO()
            document.save(buffer)
            buffer.seek(0)
            modified_files.append((uploaded_file.name, buffer))

    if modified_files:
        # Create a ZIP file of all modified docs
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for filename, file_buffer in modified_files:
                base, _ = os.path.splitext(filename)
                modified_filename = f"{base}_modified.docx"
                zipf.writestr(modified_filename, file_buffer.read())

        zip_buffer.seek(0)
        st.download_button(
            label="Download all modified files as ZIP",
            data=zip_buffer,
            file_name="modified_documents.zip",
            mime="application/zip"
        )
    else:
        st.info("No matches found for replacement in any document.")
