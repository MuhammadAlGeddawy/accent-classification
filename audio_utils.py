from yt_dlp import YoutubeDL
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os

def get_video_path(input_path: str, output_dir: str = "downloads", filename: str = "downloaded_video.mp4") -> str:
    """
    Download video from a YouTube URL or use local path.

    Args:
        input_path: YouTube URL or local file path.
        output_dir: Directory to save downloaded video.
        filename: Filename for the downloaded video.

    Returns:
        Path to the downloaded or local video file.
    """
    if input_path.startswith("http"):
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': output_path,
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([input_path])
        return output_path
    else:
        # Assume local file path
        if os.path.exists(input_path):
            return input_path
        else:
            raise FileNotFoundError(f"Local file not found: {input_path}")

def extract_audio(video_path: str, audio_path: str = "audio.wav") -> str:
    """
    Extract audio from a video file and save as WAV.

    Args:
        video_path: Path to video file.
        audio_path: Path to save extracted audio.

    Returns:
        Path to extracted audio WAV file.
    """
    clip = AudioFileClip(video_path)
    clip.write_audiofile(audio_path, codec='pcm_s16le')  # WAV format
    clip.close()
    print(f"✅ Audio extracted to: {audio_path}")
    return audio_path
