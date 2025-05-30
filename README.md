
# Accent Classification from Video

Classify speaker accents from YouTube or uploaded videos by extracting audio and using a pretrained SpeechBrain model.

---

## Features

* Download YouTube videos or upload local videos
* Extract and play audio
* Predict accents from audio
* Automatic cleanup of temporary files

---

## Requirements

* Python 3.10
* Conda (recommended) or pip
* FFmpeg installed and in system PATH

---

## Setup

1. Clone repo
2. Create and activate env:

```bash
conda env create -f environment.yml  
conda activate accent-detector  
```

3. Alternatively, install dependencies via pip
4. Ensure ffmpeg is installed and accessible

---

## Run

```bash
streamlit run app.py  
```

Choose input method → provide video → click **Process Video** → see results and play audio

---

## Notes

* Supported upload formats: mp4, mov, avi
* Some YouTube URLs may fail due to restrictions
* Activate environment before running

---

## Troubleshooting

* Install missing packages if errors occur
* Verify ffmpeg installation
* Check internet connection for YouTube downloads
