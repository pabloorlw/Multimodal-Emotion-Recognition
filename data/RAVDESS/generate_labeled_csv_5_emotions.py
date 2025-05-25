import os
import argparse
import pandas as pd

# Mapeo de número de emoción a etiqueta
emotion_map = {
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "08": "surprised"
}


# Asigna split basado en el ID del actor
def get_split(actor_id):
    if actor_id <= 18:
        return "train"
    elif actor_id <= 21:
        return "val"
    else:
        return "test"
        
        
# Extrae la emoción y el actor desde el nombre del archivo
def extract_info_from_filename(file_path):
    filename = os.path.basename(file_path)
    parts = filename.split("-")
    emotion_num = parts[2]
    emotion = emotion_map.get(emotion_num, "unknown")
    actor_str = parts[-1].split(".")[0]  # ultima parte antes de .wav
    actor_id = int(actor_str.replace("Actor_", "").zfill(2))
    split = get_split(actor_id)
    return emotion, actor_id, split



def generate_csv(audio_dir, output_path="ravdess_labels.csv"):
    data = []

    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.endswith(".wav"):
                full_path = os.path.join(root, file)
                try:
                    emotion, actor_id, split = extract_info_from_filename(full_path)
                    data.append({
                        "file": full_path,
                        "emotion": emotion,
                        "actor_id": actor_id,
                        "split": split
                    })
                except Exception as e:
                    print(f"Error procesando {full_path}: {e}")

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"CSV guardado en: {output_path}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera un CSV con rutas y emociones de RAVDESS")
    parser.add_argument("--audio_dir", type=str, required=True, help="Directorio raíz con las carpetas Actor_XX")
    parser.add_argument("--output", type=str, default="ravdess_labels_5_emotions.csv", help="Ruta del CSV de salida")
    args = parser.parse_args()

    generate_csv(args.audio_dir, args.output)

