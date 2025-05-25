import argparse
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

# Mapas de clases
emotion_map = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}
intensity_map = {
    '01': 'normal',
    '02': 'strong'
}

def parse_filename(filename):
    parts = filename.split('.')[0].split('-')
    if len(parts) != 7:
        return None
    modality, channel, emotion, intensity, statement, repetition, actor = parts
    return {
        'emotion': emotion_map.get(emotion, 'unknown'),
        'intensity': intensity_map.get(intensity, 'unknown'),
        'actor': f"Actor_{actor.zfill(2)}"
    }

def collect_data(data_path):
    data = []
    for actor_dir in os.listdir(data_path):
        actor_path = os.path.join(data_path, actor_dir)
        if not os.path.isdir(actor_path):
            continue
        for file in os.listdir(actor_path):
            if file.endswith('.wav'):
                parsed = parse_filename(file)
                if parsed:
                    data.append(parsed)
    return pd.DataFrame(data)

def plot_distribution(df):
    # Distribución total por emoción e intensidad
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='emotion', hue='intensity')
    #plt.title('Distribución de emociones por intensidad (total)')
    plt.xlabel('Emoción')
    plt.ylabel('Número de ejemplos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Distribución por actor
    actor_emotion_counts = df.groupby(['actor', 'emotion']).size().unstack(fill_value=0)
    actor_emotion_counts.plot(kind='bar', stacked=True, figsize=(15, 6), colormap='tab20')
    #plt.title('Distribución de emociones por actor')
    plt.xlabel('Actor')
    plt.ylabel('Número de ejemplos')
    plt.legend(title='Emoción', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análisis exploratorio del dataset RAVDESS")
    parser.add_argument("--data_path", type=str, required=True, help="Ruta a la carpeta Audio_Speech_Actors_01-24")
    args = parser.parse_args()

    df = collect_data(args.data_path)
    print(df.head())
    print("\nDistribución total:\n", df.value_counts(['emotion', 'intensity']))
    print("\nDistribución por actor:\n", df.groupby(['actor', 'emotion']).size())

    plot_distribution(df)


