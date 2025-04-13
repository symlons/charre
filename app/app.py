import streamlit as st
import requests

st.title("charre: car brand classifier")

st.header("Find your car brand")

uploaded_file = st.file_uploader("Choose a image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
  st.image(uploaded_file, caption="Uploaded Image")
  if st.button("Predict"):
    # Read file
    bytes_data = uploaded_file.getvalue()

    # TODO rest call to be defined

    # Send bytestream to the model
    # url = "http://example:"
    # response = requests.post(url, files={"file": bytes_data})
    # if response.status_code == 200:
    #    result = response.json()
    #    st.write(f"Predicted Brand: {result.get('brand', 'Unknown')}")
    # else:
    #    st.error("Failed to get a response from the model.")
    st.write("Predicted Brand: <Result from model>")

st.header("Feedback")

# TODO fix that buttons are next to each other
col1, col2 = st.columns(2)
with col1:
  if st.button("👍", key="thumbs_up"):
    st.success("Thank you for your feedback!")
with col2:
  if st.button("👎", key="thumbs_down"):
    st.warning("Thank you for your feedback! We'll work on improving.")

list_brands = None

if list_brands is None:
  # TODO rest call to be defined
  # url = "http://example:"
  # response = requests.get(url)
  # if response.status_code == 200:
  #    list_brands = response.json()

  list_brands = [
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

# Ensure the button is only clickable after a selection is made
selected_brand = st.selectbox("What brand was the car?", list_brands, index=None)

if st.button("Submit Feedback") and selected_brand:
  # Functionality to handle feedback submission
  # TODO rest call to be defined
  # response = requests.post(url, selected_brand)
  # if response.status_code == 200:
  #    st.success("Feedback submitted successfully!")
  # else:
  #    st.error("Failed to submit feedback.")
  # For now, just show a success message
  st.success(f"Feedback submitted successfully for brand: {selected_brand}")
