import streamlit as st
import requests
import base64
import os

# Feedback URL has /feedback prefix already included for simplicity
FEEDBACK_URL = os.getenv("FEEDBACK_URL", "http://localhost:5000/feedback")
PREDICT_URL = os.getenv("PREDICT_URL", "http://localhost:5001/predict")

def connection_error(error_text: str):
  st.error("Failed to fetch labels.")
  st.write("Response text:", error_text)
  temp = [
        "Toyota",
        "Honda",
        "Ford",
        "Chevrolet",
        "Nissan",
        "Volkswagen",
        "Hyundai",
        "Kia",
        "Subaru",
        "Mazda",
        "BMW",
        "Mercedes-Benz",
        "Audi",
        "Lexus",
        "Porsche",
      ]
  return temp

st.title("charre: car brand classifier")

st.header("Find your car brand")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
  st.image(uploaded_file, caption="Uploaded Image")
  if st.button("Predict"):
    bytes_data = uploaded_file.getvalue()

    try:
      response = requests.post(PREDICT_URL, data=bytes_data, headers={'Content-Type': 'application/octet-stream'})
      if response.status_code == 200:
        st.success("Prediction successful!")
        st.write("Predicted Brand: ", response.json()["predicted_brand"])
      else:
        st.error("Failed to predict brand.")
        st.write("Response text:", response.text)
    except requests.exceptions.RequestException as e:
      st.error("Failed to predict brand.")
      st.write("Error:", e)
  #st.write("Predicted Brand: <Result from model>")

st.header("Feedback")

if "thumb_status" not in st.session_state:
  st.session_state.thumb_status = None

col1, col2 = st.columns(2)

with col1:
  if st.button("👍", key="thumbs_up"):
    st.session_state.thumb_status = True

with col2:
  if st.button("👎", key="thumbs_down"):
    st.session_state.thumb_status = False

try:
    url = f"{FEEDBACK_URL}/labels"
    response = requests.get(url)
    print(response.json())
    list_brands = []
    if response.status_code == 200:
        list_brands = response.json()["labels"]
    else:
        list_brands = connection_error(response.text)     
except requests.exceptions.RequestException as e:
  list_brands = connection_error(e.strerror)

if st.session_state.thumb_status is None or uploaded_file is None:
  st.warning("Please provide image and feedback before submitting.")
else:

  selected_brand = st.selectbox("What brand was the car?", list_brands, index=None)

  if st.button("Submit Feedback") and selected_brand:
    url = f"{FEEDBACK_URL}/feedback"
    bytes_data = uploaded_file.getvalue()

    base64_image = base64.b64encode(bytes_data).decode("utf-8")

    payload = {
      "correct_label": selected_brand,
      "correct": st.session_state.thumb_status,
      "label": "TODO",
      "image": base64_image,
    }
    try:
      response = requests.post(url, json=payload)

      if response.status_code == 201:
        st.success("Feedback submitted successfully!")
      else:
        st.error("Failed to submit feedback.")
        st.write("Response text:", response.text)
    except requests.exceptions.RequestException as e:
      st.error("Failed to submit feedback.")
      st.write("Error:", e)

