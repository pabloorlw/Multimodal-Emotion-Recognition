import os
import argparse
from pathlib import Path
import subprocess
from multiprocessing import Pool

def convert_mp4_to_wav_single(mp4_file, output_dir):
    output_path = Path(output_dir)
    wav_file = output_path / (mp4_file.stem + ".wav")

    command = [
        "ffmpeg",
        "-i", str(mp4_file),
        "-ar", "16000",     # Resamplear a 16kHz
        "-ac", "1",         # Canal mono 
        "-y",               # Sobrescribir si ya existe
        str(wav_file)
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print(f"Convertido: {mp4_file.name} -> {wav_file.name}")

def convert_mp4_to_wav_parallel(input_dir, output_dir, num_processes=None):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    mp4_files = list(input_path.glob("*.mp4"))

    if not mp4_files:
        print(f"No se encontraron archivos .mp4 en {input_path}")
        return

    if num_processes is None:
        num_processes = os.cpu_count()

    print(f"Convirtiendo {len(mp4_files)} archivos usando {num_processes} procesos...")

    with Pool(processes=num_processes) as pool:
        tasks = [(mp4_file, output_dir) for mp4_file in mp4_files]
        pool.starmap(convert_mp4_to_wav_single, tasks)

    print("Conversión completada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convierte todos los mp4 en una carpeta a archivos wav a 16kHz usando paralelización.")
    parser.add_argument("--input_dir", type=str, required=True, help="Ruta a la carpeta de entrada con archivos .mp4")
    parser.add_argument("--output_dir", type=str, required=True, help="Ruta a la carpeta donde se guardarán los .wav")
    parser.add_argument("-j", "--jobs", type=int, help="Número de procesos a usar (por defecto: número de CPUs)")

    args = parser.parse_args()
    convert_mp4_to_wav_parallel(args.input_dir, args.output_dir, args.jobs)

