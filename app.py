import streamlit as st
import os
import tempfile
import subprocess
import time
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

def save_language(language):
    with open("language.txt", "w", encoding="utf-8") as lang_file:
        lang_file.write(language.lower())

def read_text():
    if os.path.exists("text.txt"):
        with open("text.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    return ""

def load_model():
    model_path = Path.home().joinpath('mistral_models', '7B-Instruct-v0.3')
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16)
    if torch.cuda.is_available():
        model = model.to("cuda")
    return model, tokenizer

@st.cache_resource
def get_model():
    return load_model()

model, tokenizer = get_model()

def generate_response(prompt, max_new_tokens=150):
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = inputs.to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.7, top_p=0.9)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()

def summarize_text(article_text):
    prompt = f"Below is an article. Summarize it in a few sentences:\n\n{article_text}\n\nSummary:"
    return generate_response(prompt)

def answer_question(article_text, question):
    prompt = f"Below is an article:\n\n{article_text}\n\nQuestion: {question}\nAnswer:"
    return generate_response(prompt)

def generate_flashcards(article_text):
    with open("temp_article.txt", "w", encoding="utf-8") as f:
        f.write(article_text)
    subprocess.run(["python", "FlashCard2.py", "temp_article.txt"])
    if os.path.exists("flashcards.txt"):
        with open("flashcards.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return "❌ No flashcards generated."

st.title("Audio, Text, or Image to Text Converter & AI Processing")
option = st.radio("Choose an input method:", ["Audio (File/YouTube)", "Text", "Upload Image"])

if option in ["Text", "Upload Image"]:
    language = st.selectbox("Select language:", ["English", "Hindi"])
else:
    language = "English"
save_language(language)

if option == "Audio (File/YouTube)":
    audio_option = st.radio("Choose audio source:", ["Upload File", "YouTube Link"])
    if audio_option == "Upload File":
        uploaded_audio = st.file_uploader("Upload an audio file", type=['mp3', 'wav'])
        if uploaded_audio and st.button("Convert Audio to Text"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(uploaded_audio.read())
                temp_audio_path = temp_audio.name
            subprocess.run(["python", "Audio_To_Text_Actual.py", temp_audio_path])
            os.remove(temp_audio_path)
    elif audio_option == "YouTube Link":
        yt_link = st.text_input("Enter YouTube Video Link:")
        if st.button("Extract & Convert Audio") and yt_link:
            subprocess.run(["python", "Youtube_Audio_To_Text.py", yt_link])

elif option == "Text":
    user_text = st.text_area("Enter text below:")
    if st.button("Save Text"):
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(user_text)

elif option == "Upload Image":
    uploaded_file = st.file_uploader("\U0001F4F7 Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        with open("uploaded_image.jpg", "wb") as f:
            f.write(uploaded_file.read())
        st.image("uploaded_image.jpg", caption="Uploaded Image", use_column_width=True)
        subprocess.run(["python", "Image_To_Text.py"])

text_content = read_text()
if text_content:
    st.subheader("Extracted/Saved Text")
    with st.expander("📄 View Text"):
        st.write(text_content)
    if st.button("Summarize Article"):
        with st.spinner("Generating summary..."):
            st.write(summarize_text(text_content))
    question = st.text_input("Ask a question about the article:")
    if st.button("Get Answer") and question:
        with st.spinner("Generating answer..."):
            st.write(answer_question(text_content, question))
    if st.button("Generate Flashcards"):
        with st.spinner("Generating flashcards..."):
            st.write(generate_flashcards(text_content))

if st.button("Refresh App"):
    for file in ["text.txt", "language.txt", "uploaded_image.jpg", "translated.txt"]:
        if os.path.exists(file):
            os.remove(file)
    st.experimental_rerun()