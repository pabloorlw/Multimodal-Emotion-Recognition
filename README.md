# Multimodal-Emotion-Recognition

In this repository you will find the code used for the experimentation in the final thesis: “Introduction to multimodal emotion recognition”. 

This thesis utilizes both unimodal and multimodal approaches for emotion detection. Below is a breakdown of the models and datasets used, along with links to their respective Hugging Face repositories and relevant code locations.

1. Text model: we fine-tuned DistilBERT on Emotions dataset.
   * The code used to fine-tune DisilBERT can be found in the models/ directory.
2. Audio model: we fine-tuned Wav2Vec 2.0 on RAVDESS dataset.
   * The code for preprocessing the RAVDESS dataset is located in data/RAVDESS/.
   * The code used to fine-tune Wav2Vec 2.0 can be found in the models/ directory.
3. The multimodal models and evaluation of transfer-learning capabilities on MELD dataset can be found in in models/ directory.
   * The code for preprocessing the MELD dataset is located in data/MELD.

Both fine-tuned models and preprocessed datasets can be obtained from [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Repository-blue)(https://huggingface.co/pabloorlw)
