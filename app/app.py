import base64
import os

import requests
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

FEEDBACK_URL = os.getenv("FEEDBACK_URL", "http://localhost:5000/feedback/")
CLASSIFIER_URL = os.getenv(
  "CLASSIFIER_URL",
  "https://fabio-kost--flask-server-flask-app.modal.run/model_endpoint",
)

if "thumb_status" not in st.session_state:
  st.session_state.thumb_status = None
if "label" not in st.session_state:
  st.session_state.label = None


def connection_error(message: str | None) -> list[str]:
  st.error("Failed to fetch labels.")
  st.write("Response text:", message)
  return []


def classify_image(file: UploadedFile) -> None:
  import io
  bytes_data = file.read()
  files = {"image": (file.name, io.BytesIO(bytes_data), file.type)}


  try:
    response = requests.post(
      CLASSIFIER_URL,
      files=files,
      # headers={"Content-Type": "application/octet-stream"},
    )
    if response.status_code == 200:
      st.success("Prediction successful!")
      st.write("Predicted Brand: ", response.json()["predicted_class"])
      st.session_state.label = response.json()["predicted_class"]
    else:
      st.error("Failed to predict brand.")
      st.write("Response text:", response.text)
  except requests.exceptions.RequestException as e:
    st.error("Failed to predict brand.")
    st.write("Error:", e)


def submit_feedback(file: UploadedFile, correct_label: str, label: str) -> None:
  try:
    response = requests.post(
      url=f"{FEEDBACK_URL}/feedback",
      json={
        "correct_label": correct_label,
        "correct": st.session_state.thumb_status,
        "label": label,
        "image": base64.b64encode(file.getvalue()).decode("utf-8"),
      },
      timeout=20,
    )

    if response.status_code == 201:
      st.success("Feedback submitted successfully!")
    else:
      st.error("Failed to submit feedback.")
      st.write("Response text:", response.text)
  except requests.exceptions.RequestException as e:
    st.error("Failed to submit feedback.")
    st.write("Error:", e)


# Classifier Section
st.title("charre: car brand classifier")
st.header("Find your car brand")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
st.button(
  "Predict",
  disabled=uploaded_file is None,
  on_click=classify_image,
  args=(uploaded_file,),
)

# Feedback Section
st.header("Feedback")

col1, col2 = st.columns(2)
with col1:
  if st.button("👍", key="thumbs_up"):
    st.session_state.thumb_status = True
with col2:
  if st.button("👎", key="thumbs_down"):
    st.session_state.thumb_status = False

try:
  response = requests.get(f"{FEEDBACK_URL}/labels", timeout=20)
  print(response.json())
  if response.status_code == 200:
    list_brands = response.json()["labels"]
  else:
    print(response.text)
    list_brands = connection_error(response.text)
except requests.exceptions.RequestException as e:
  list_brands = connection_error(e.strerror)

if st.session_state.thumb_status is None or uploaded_file is None:
  st.warning("Please provide image and feedback before submitting.")
else:
  correct_label = st.selectbox("What brand was the car?", list_brands, index=None)
  st.button(
    "Submit Feedback",
    disabled=correct_label is None,
    on_click=submit_feedback,
    args=(uploaded_file, correct_label, st.session_state.label),
  )
