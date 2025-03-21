import os
import sys
import whisper

# Ensure FFmpeg is available
os.environ["PATH"] += os.pathsep + r"C:\Users\sanje\Downloads\ffmpeg\ffmpeg-2025-03-13-git-958c46800e-essentials_build\bin"

# Ensure audio file is provided
if len(sys.argv) < 2:
    print("❌ Error: No audio file provided.")
    sys.exit(1)

audio_path = sys.argv[1]
language = sys.argv[2] if len(sys.argv) > 2 else None  # Language argument (optional)

# Load Whisper model
model = whisper.load_model("base")

try:
    result = model.transcribe(audio_path, language=language)  # Set language explicitly if provided
    text = result["text"]

    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(text)  # Output text to be captured by subprocess
except Exception as e:
    print(f"❌ Error: {str(e)}")