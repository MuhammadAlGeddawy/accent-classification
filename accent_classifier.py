from speechbrain.pretrained import EncoderClassifier

classifier = EncoderClassifier.from_hparams(
    source="Jzuluaga/accent-id-commonaccent_ecapa",
    savedir="pretrained_models/accent-id-commonaccent_ecapa"
)

def predict_accent(audio_path: str):
    """
    Predict accent label, score, and summary explanation from audio.

    Returns:
        tuple: (accent_label:str, score:float, summary:str)
    """
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)
    summary = (
        f"The model is {score*100:.2f}% confident that the accent in the audio is '{text_lab}'. "
        "This prediction is based on acoustic features learned from a diverse dataset of common accents."
    )
    return text_lab, score, summary
