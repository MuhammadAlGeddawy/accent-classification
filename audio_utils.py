import os
import uuid
import logging
from yt_dlp import YoutubeDL
from moviepy.audio.io.AudioFileClip import AudioFileClip

logging.basicConfig(level=logging.INFO)

def get_video_path(input_path: str, output_dir: str = "downloads", filename: str = "downloaded_video.mp4") -> str:
    """
    Download video from a YouTube URL or return local path.

    Args:
        input_path: YouTube URL or local file path.
        output_dir: Directory to save downloaded video.
        filename: Filename for the downloaded video.

    Returns:
        Path to the video file.
    """
    if input_path.startswith("http"):
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': output_path,
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([input_path])
            logging.info(f"✅ Video downloaded to: {output_path}")
            return output_path
        except Exception as e:
            raise RuntimeError(f"❌ Failed to download video: {e}")
    else:
        # Assume local file path
        if os.path.exists(input_path):
            logging.info(f"✅ Using local video: {input_path}")
            return input_path
        else:
            raise FileNotFoundError(f"❌ Local file not found: {input_path}")

def extract_audio(video_path: str, audio_path: str = None) -> str:
    """
    Extract audio from a video file and save as WAV.

    Args:
        video_path: Path to video file.
        audio_path: Optional path to save extracted audio.

    Returns:
        Path to extracted audio WAV file.
    """
    if not audio_path:
        audio_path = f"audio_{uuid.uuid4().hex}.wav"
    clip = AudioFileClip(video_path)
    clip.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)
    clip.close()
    logging.info(f"✅ Audio extracted to: {audio_path}")
    return audio_path

def clean_temp_files(*paths):
    """
    Delete temporary files safely.
    """
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logging.info(f"🧹 Deleted temp file: {path}")
        except Exception as e:
            logging.warning(f"⚠️ Could not delete {path}: {e}")
