import argparse
import os
import torchaudio
import torchaudio.transforms as T

def resample_and_mono(input_path, output_path, target_sr=16000):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".wav"):
                full_input = os.path.join(root, file)
                rel_path = os.path.relpath(full_input, input_path)
                full_output = os.path.join(output_path, rel_path)
                os.makedirs(os.path.dirname(full_output), exist_ok=True)

                waveform, orig_sr = torchaudio.load(full_input)

                # si es stereo, convertir a mono
                if waveform.shape[0] > 1:
                    waveform = waveform.mean(dim=0, keepdim=True)

                # resamplear a 16kHz si no lo esta ya
                if orig_sr != target_sr:
                    resampler = T.Resample(orig_freq=orig_sr, new_freq=target_sr)
                    waveform = resampler(waveform)

                torchaudio.save(full_output, waveform, sample_rate=target_sr)
                print(f"{rel_path} -> mono, {target_sr} Hz")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reescala los audios a 16kHz y canal mono")
    parser.add_argument("--input_dir", type=str, required=True, help="Ruta original de los audios")
    parser.add_argument("--output_dir", type=str, required=True, help="Ruta de salida para los audios reescalados")
    args = parser.parse_args()

    resample_and_mono(args.input_dir, args.output_dir)

