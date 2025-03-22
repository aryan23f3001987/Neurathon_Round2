from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from pathlib import Path

# Load the model
def load_model():
    model_path = Path.home().joinpath('mistral_models', '7B-Instruct-v0.3')
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16)
    if torch.cuda.is_available():
        model = model.to("cuda")
    return model, tokenizer

model, tokenizer = load_model()

# Generate flashcards
def generate_flashcards(lecture_text):
    prompt = f"""
    Extract key concepts and their definitions from the following lecture text.
    Format them as flashcards.

    Lecture Text:
    {lecture_text}

    Format:
    Concept: [Concept Name]
    Definition: [Short Explanation]
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = inputs.to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,  # 300 new tokens for flashcards
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()

# Read and save functions
def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

# Run it
lecture_text = read_text_from_file("text.txt")
flashcards = generate_flashcards(lecture_text)
save_to_file("flashcards.txt", flashcards)
print("✅ Flashcards saved to flashcards.txt")