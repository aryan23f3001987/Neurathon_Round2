Audio, Text, or Image to Text Converter & AI Processing

Overview:
This Streamlit-based web app extracts text from audio, YouTube videos, and images, using AI for speech-to-text, OCR, and NLP tasks.
Users can manually input text or extract it from media formats, then leverage AI to summarize content, answer questions, and generate flashcards.
Designed for students, researchers, and professionals, it streamlines learning by converting raw data into structured insights.


Evaluation with Weights & Biases (WandB):
We use Weights & Biases (WandB) to evaluate the performance of our summarization model.
This includes:
ROUGE Score Calculation: Automatically computing ROUGE-1, ROUGE-2, and ROUGE-L scores for generated summaries against ground truth references.
Logging Sample Summaries: Recording text, generated summaries, and ground truth summaries for performance tracking.
Result Storage & Analysis: Storing evaluation results in CSV format for further analysis.


Features:

Audio to Text Conversion:
Upload an audio file (MP3/WAV) or provide a YouTube link.
Uses Whisper for high-accuracy speech-to-text conversion.
Supports multiple languages for transcription.

Text Processing:
Users can manually enter text for further processing.
The text is stored and can be analyzed using AI-powered tools.

Image to Text Conversion:
Upload an image in JPG, PNG, or JPEG format.
Uses OCR technology to extract text from the image.
Displays the extracted text for further processing.

Text Summarization:
Generates a concise summary of the extracted or entered text.
Uses an AI language model to provide accurate and meaningful summaries.

Question Answering:
Users can ask questions related to the extracted or entered text.
AI model generates precise answers based on the content provided.

Flashcard Generation:
Automatically creates flashcards from extracted text.
Helps in learning and revision by converting text into a Q&A format.
Saves the generated flashcards in a separate file for future reference.


Tech Stack:
Python, Streamlit, Hugging Face Transformers, Torch, FFmpeg & Whisper.


Files and Scripts:
app.py: Main Streamlit app.
Audio_To_Text_Actual.py: Converts audio to text.
Youtube_Audio_To_Text.py: Processes YouTube audio.
Image_To_Text.py: Extracts text from images.
FlashCard2.py: Generates flashcards.
text.txt: Stores extracted or inputted text.
