import streamlit as st
import os
import tempfile
import subprocess

# Streamlit app
def main():
    st.title("Audio, Text, or Image to Text Converter")

    # Clear text.txt on refresh
    if os.path.exists("text.txt"):
        os.remove("text.txt")

    # Ensure uploaded_image is deleted on refresh
    if os.path.exists("uploaded_image.jpg"):
        os.remove("uploaded_image.jpg")

    option = st.radio("Choose an input method:", ["Audio", "Text", "Upload Image"])

    if option == "Audio":
        uploaded_audio = st.file_uploader("Upload an audio file (.mp3 or .wav)", type=['mp3', 'wav'])
        if uploaded_audio is not None:
            st.audio(uploaded_audio)
            if st.button("Convert Audio to Text"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                    temp_audio.write(uploaded_audio.read())
                    temp_audio_path = temp_audio.name

                with st.spinner("Processing audio..."):
                    result = subprocess.run(["python", "Audio_To_Text_Actual.py", temp_audio_path], capture_output=True, text=True)
                    st.session_state['text'] = result.stdout.strip()
                    st.success("Audio conversion complete!")

                os.remove(temp_audio_path)  # Cleanup temp file

    elif option == "Text":
        user_text = st.text_area("Enter text below:")
        if st.button("Save Text"):
            with open("text.txt", "w") as f:
                f.write(user_text)
            st.session_state['text'] = user_text
            st.success("Text saved successfully!")

    elif option == "Upload Image": 
        uploaded_file = st.file_uploader("\U0001F4F7 Upload an Image", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            # Save uploaded image as "uploaded_image.jpg"
            with open("uploaded_image.jpg", "wb") as f:
                f.write(uploaded_file.read())
            
            st.image("uploaded_image.jpg", caption="Uploaded Image", use_column_width=True)

            # Run Image_To_Text.py
            subprocess.run(["python", "Image_To_Text.py"])

            # Debugging: Check if text.txt exists
            if os.path.exists("text.txt"):
                with open("text.txt", "r", encoding="utf-8") as check_file:
                    extracted_text = check_file.read().strip()
                    if extracted_text:
                        st.session_state['text'] = extracted_text  # Store extracted text
                        st.write("✅ Extracted Text from Image!")
                    else:
                        st.write("❌ Image text extraction failed: `text.txt` is empty!")
            else:
                st.write("❌ `text.txt` was not created!")

            # Run translation_to_english.py
            subprocess.run(["python", "translation_to_english.py"])

    # Display extracted text
    if 'text' in st.session_state:
        st.subheader("Extracted/Saved Text:")
        st.write(st.session_state['text'])

if __name__ == "__main__":
    main()