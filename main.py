import os
import wave
import tkinter as tk
import pyaudio
import threading

CARTELLA_SUONI = "suoni"
INDICE_MICROFONO_VIRTUALE = 2  # Cambia questo valore se necessario

def riproduci_audio(percorso_file):
    wf = wave.open(percorso_file, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=INDICE_MICROFONO_VIRTUALE)

    CHUNK = 1024
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

def riproduci(percorso):
    threading.Thread(target=riproduci_audio, args=(percorso,), daemon=True).start()

finestra = tk.Tk()
finestra.title("Soundboard")
finestra.geometry("400x400")

file_suoni = [f for f in os.listdir(CARTELLA_SUONI) if f.lower().endswith('.wav')]

for file in file_suoni:
    percorso = os.path.join(CARTELLA_SUONI, file)
    nome = os.path.splitext(file)[0]
    tk.Button(finestra, text=nome, command=lambda p=percorso: riproduci(p)).pack(pady=5, fill="x")

finestra.mainloop()
