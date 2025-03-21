from moviepy.editor import VideoFileClip

def convert_video_to_audio(video_path, output_audio_path="output_audio.wav"):
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Extract and save the audio
    video.audio.write_audiofile(output_audio_path)
    
    return output_audio_path

# Example Usage
video_path = "input_video.mp4"  # Replace with your actual video file
audio_path = convert_video_to_audio(video_path)
print(f"Audio saved at: {audio_path}")
