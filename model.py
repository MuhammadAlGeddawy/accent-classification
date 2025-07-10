from speechbrain.pretrained import EncoderClassifier
import torch

class AccentClassifier:
    def __init__(self):
        self.model = EncoderClassifier.from_hparams(
            source="Jzuluaga/accent-id-commonaccent_ecapa",
            savedir="pretrained_models/accent-id-commonaccent_ecapa"
        )

    def predict(self, audio_path):
        out = self.model.classify_file(audio_path)
        label = out[3]
        conf = torch.nn.functional.softmax(out[1], dim=0).max().item()
        return {"label": label, "confidence": round(conf, 3)}
