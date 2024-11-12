import time
import streamlit as st
from reasoner import Reasoner

r = Reasoner(api_key="INSERT API KEY")
r.initialize()

st.title("📝 Reasoner Playground")
uploaded_files = st.file_uploader("Upload an article", type=("pdf"), accept_multiple_files=True)

is_batch_ready = False
batch_uid = None
if uploaded_files and not is_batch_ready:
    st.info("Uploading to reasoner...")

    result = r.documents.upload(files=uploaded_files)
    batch_uid = result.batch.uid

    st.info(f"Batch {batch_uid} uploaded")

    while True:
        status = r.batches.get_status(batch_uid)
        if status == "success":
            st.info("Documents processed ✓")
            is_batch_ready = True
            break
        elif status == "failed":
            raise Exception("Document processing failed")
        time.sleep(5)

question = st.text_input(
    "Ask something about the files",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_files,
)

if is_batch_ready and question:
    messages = [{"role": "user", "content": question}]
    response = r.chat.completion(
        batch_uid=batch_uid, messages=messages
    )
    st.write("### Answer")
    st.write(response)
