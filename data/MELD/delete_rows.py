import os
import pandas as pd
import argparse

def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(description="Elimina las filas de un CSV que no tienen archivos de audio correspondientes en una carpeta.")
    parser.add_argument("audio_folder", help="Ruta a la carpeta que contiene los archivos de audio .wav")
    parser.add_argument("csv_file", help="Ruta al archivo CSV")
    parser.add_argument("--confirm", action="store_true", help="Confirma la eliminación de las filas (sin esta opción, solo se mostrarán las filas a eliminar)")

    # Obtiene los argumentos pasados por la línea de comandos
    args = parser.parse_args()
    audio_folder_path = args.audio_folder
    csv_file_path = args.csv_file
    confirm_deletion = args.confirm

    try:
        # Carga el archivo CSV en un DataFrame de pandas
        df = pd.read_csv(csv_file_path)
        initial_row_count = len(df)

        # Crea un conjunto de los nombres de archivo de audio existentes
        existing_audio_files = {filename for filename in os.listdir(audio_folder_path) if filename.endswith('.wav')}

        # Crea una lista para almacenar los índices de las filas a eliminar
        rows_to_drop = []

        # Itera a través de cada fila del DataFrame con su índice
        for index, row in df.iterrows():
            dialogue_id = row['Dialogue_ID']
            utterance_id = row['Utterance_ID']
            expected_filename = f"dia{dialogue_id}_utt{utterance_id}.wav"

            # Comprueba si el nombre de archivo esperado NO existe en el conjunto de archivos de audio
            if expected_filename not in existing_audio_files:
                rows_to_drop.append(index)

        if rows_to_drop:
            print("Filas en el CSV que NO tienen archivo de audio correspondiente:")
            for index_to_drop in rows_to_drop:
                print(f"Índice: {index_to_drop}, Dialogue_ID: {df.loc[index_to_drop, 'Dialogue_ID']}, Utterance_ID: {df.loc[index_to_drop, 'Utterance_ID']}")

            if confirm_deletion:
                # Elimina las filas utilizando los índices
                df_cleaned = df.drop(rows_to_drop)

                # Guarda el DataFrame modificado de nuevo al archivo CSV (sobrescribiendo el original)
                df_cleaned.to_csv(csv_file_path, index=False)
                final_row_count = len(df_cleaned)
                deleted_count = initial_row_count - final_row_count
                print(f"\nSe eliminaron {deleted_count} filas del archivo CSV: {csv_file_path}")
            else:
                print("\nNo se eliminaron las filas. Ejecuta el script con la opción '--confirm' para realizar la eliminación.")
        else:
            print("Todos los archivos en el CSV tienen su correspondiente archivo de audio. No se eliminaron filas.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en: {csv_file_path} o la carpeta de audio en: {audio_folder_path}. Por favor, verifica las rutas.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
