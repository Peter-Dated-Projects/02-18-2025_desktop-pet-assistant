from TTS.tts.configs.xtts_config import XttsConfig
import torch.serialization

torch.serialization.add_safe_globals([XttsConfig])

import torch
from TTS.api import TTS


print("PyTorch version:", torch.__version__)
print("MPS available:", torch.backends.mps.is_available())

# Check if MPS is available and set the device accordingly
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)

# Change the model_name to use the Glow-TTS model
model_name = "tts_models/en/ljspeech/glow-tts"
tts = TTS(model_name=model_name, progress_bar=True, gpu=False)

# Convert text to speech and save the output as a WAV file.
output_file = "assets/output.wav"
tts.tts_to_file(
    text="Hello, this is a test of Coqui TTS using the Glow-TTS model!",
    file_path=output_file,
)

print(f"Audio saved to {output_file}")
