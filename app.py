from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env files
import streamlit as st
import os  # Picking up the assigned variable
from PIL import Image
import google.generativeai as genai

# Configure the API key for Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the gemini model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Failed to load the model: {e}")
    st.stop()

def gem_resp(input, image, prompt):
    try:
        res = model.generate_content([input, image[0], prompt])
        return res.text
    except Exception as e:
        return f"Error in processing: {e}"

def input_image(upload_fl):
    if upload_fl is not None:
        byte = upload_fl.getvalue()
        image_parts = [
            {
                "mime_type": upload_fl.type,
                "data": byte
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Streamlit app configuration
st.set_page_config(page_title="Multi-language Invoice Extractor")
st.header("Multi-language Invoice Extractor")

# Input and file uploader
input = st.text_input("Input Prompt:", key="input")
upload_fl = st.file_uploader("Choose an image of the Invoice ....", type=["jpg", "jpeg", "png"])

# Display uploaded image
if upload_fl is not None:
    image = Image.open(upload_fl)
    st.image(image, caption="Uploaded Image.", use_container_width=True)

# Button to process the invoice
submit = st.button("Tell me about the Invoice")

# Default model prompt
input_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice, 
and you will have to answer any questions based on the uploaded invoice image.
"""

# Process user input
if submit:
    if not input.strip():
        # Case when no input is provided
        st.warning("No input prompt provided. How can I assist you?")
        st.write("Here are some suggestions for questions you can ask:")
        st.write("- What is the total amount on the invoice?")
        st.write("- What is the due date of the invoice?")
        st.write("- Who is the sender of the invoice?")
        st.write("- What is the invoice number?")
    else:
        # Process the uploaded image and generate a response
        if upload_fl is None:
            st.error("Please upload an invoice image to proceed.")
        else:
            try:
                image_data = input_image(upload_fl)
                res = gem_resp(input_prompt, image_data, input)
                st.subheader("The Response is:")
                st.write(res)
            except FileNotFoundError as e:
                st.error(e)
            except Exception as e:
                st.error(f"Unexpected error: {e}")
