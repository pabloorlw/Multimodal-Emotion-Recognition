import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sns.set(style="whitegrid")

main_characters = {"Chandler", "Ross", "Phoebe", "Monica", "Joey", "Rachel"}

emotion_colors = {
    "neutral": "#1f77b4",
    "sadness": "#aec7e8",
    "disgust": "#9467bd",
    "surprise": "#2ca02c",
    "fear": "#ff7f0e",
    "joy": "#d62728",
    "anger": "#bcbd22"
}

def plot_emotion_distribution(csv_files):
    df_list = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)

    df['Emotion'] = df['Emotion'].astype(str).str.strip().str.lower()
    df['Speaker'] = df['Speaker'].astype(str).str.strip()

    df['Speaker'] = df['Speaker'].apply(lambda x: x if x in main_characters else 'Otros')

    emotion_counts = df.groupby(['Speaker', 'Emotion']).size().unstack(fill_value=0)

    emotion_counts = emotion_counts[[e for e in emotion_colors if e in emotion_counts.columns]]

    order = ['Chandler', 'Ross', 'Phoebe', 'Monica', 'Joey', 'Rachel', 'Otros']
    emotion_counts = emotion_counts.reindex(order).fillna(0)

    ax = emotion_counts.plot(kind='bar', stacked=True,
                              color=[emotion_colors[e] for e in emotion_counts.columns],
                              figsize=(10, 6))

    plt.xticks(rotation=45)
    plt.xlabel("Actor")
    plt.ylabel("Número de muestras")
    plt.legend(title='Emoción', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py archivo1.csv archivo2.csv archivo3.csv")
    else:
        plot_emotion_distribution(sys.argv[1:4])

