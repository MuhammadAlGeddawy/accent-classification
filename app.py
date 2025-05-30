import streamlit as st
import os
from audio_utils import get_video_path, extract_audio
from speechbrain.pretrained import EncoderClassifier

@st.cache_resource
def load_model():
    return EncoderClassifier.from_hparams(
        source="Jzuluaga/accent-id-commonaccent_ecapa",
        savedir="pretrained_models/accent-id-commonaccent_ecapa"
    )

classifier = load_model()

def classify_accent(audio_path):
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)
    score_float = score.item()  # convert tensor to float

    summary = (
        f"The model is {score.item()*100:.2f}% confident that the accent in the audio is '{text_lab}'. "
        "This prediction is based on acoustic features learned from a diverse dataset of common accents."
    )
    return text_lab, score_float, summary

st.title("Accent Classification from Video")

input_option = st.radio("Select input method:", ["YouTube URL", "Upload Video"])

# Initialize session state variables
if 'input_value' not in st.session_state:
    st.session_state.input_value = ""
if 'process_triggered' not in st.session_state:
    st.session_state.process_triggered = False
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'audio_path' not in st.session_state:
    st.session_state.audio_path = None
if 'result' not in st.session_state:
    st.session_state.result = None

# Input UI
if input_option == "YouTube URL":
    url = st.text_input("Enter YouTube video URL:", value=st.session_state.input_value)
    st.session_state.input_value = url
elif input_option == "Upload Video":
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        st.session_state.input_value = uploaded_file.name
    else:
        st.session_state.input_value = ""

def process():
    st.session_state.process_triggered = True
    st.session_state.result = None  # reset previous result

st.button("Process Video", on_click=process)

if st.session_state.process_triggered:
    try:
        if input_option == "YouTube URL":
            if not st.session_state.input_value:
                st.warning("Please enter a valid YouTube URL.")
                st.session_state.process_triggered = False
            else:
                with st.spinner("Downloading video..."):
                    st.session_state.video_path = get_video_path(st.session_state.input_value)
                st.success("Video downloaded successfully.")
        else:
            if not uploaded_file:
                st.warning("Please upload a video file.")
                st.session_state.process_triggered = False
            else:
                video_path = f"uploads/{uploaded_file.name}"
                os.makedirs("uploads", exist_ok=True)
                with open(video_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state.video_path = video_path
                st.success("Video uploaded successfully.")

        if st.session_state.video_path:
            with st.spinner("Extracting audio..."):
                st.session_state.audio_path = extract_audio(st.session_state.video_path, "temp_audio.wav")
            st.audio(st.session_state.audio_path)

            with st.spinner("Classifying accent..."):
                label, score, summary = classify_accent(st.session_state.audio_path)
            st.session_state.result = {
                "label": label,
                "score": score,
                "summary": summary
            }
            st.success(f"Predicted Accent: **{label}**")

            # Delete downloaded YouTube video to save space
            if input_option == "YouTube URL" and st.session_state.video_path:
                try:
                    os.remove(st.session_state.video_path)
                    st.session_state.video_path = None
                except Exception as e:
                    st.warning(f"Could not delete downloaded video: {e}")

        # Reset trigger to allow next input
        st.session_state.process_triggered = False

    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.process_triggered = False

# Show result if available
if st.session_state.result:
    st.markdown(f"### Predicted Accent: **{st.session_state.result['label']}**")
    st.markdown(f"**Confidence Score:** {st.session_state.result['score']:.4f}")
    st.markdown(f"**Summary:** {st.session_state.result['summary']}")
