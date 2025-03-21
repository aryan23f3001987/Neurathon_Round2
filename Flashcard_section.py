import openai

# Set your OpenAI API key
OPENAI_API_KEY = "your-api-key-here"
openai.api_key = OPENAI_API_KEY

# Function to generate Flashcards
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    return response["choices"][0]["message"]["content"]

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to save Flashcards to a file
def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

# Load text from text.txt
lecture_text = read_text_from_file("text.txt")

# Generate and save Flashcards
flashcards = generate_flashcards(lecture_text)
save_to_file("flashcards.txt", flashcards)
print("✅ Flashcards saved to flashcards.txt")
