import requests
import wave
from fastapi import FastAPI

app = FastAPI()


@app.post("/process_audio")
async def process_audio():
    frames = split_audio_frames("app/assignment_audio.wav", chunk_size=20)
    results = []
    headers = {'Content-Type': 'application/octet-stream'}
    for frame in frames:
        response = requests.post(
            "http://localhost:6000/process_frame", data=frame, headers=headers)
        print("res", response.json())
        if response.ok:
            results.append(response.json())

    return results


def split_audio_frames(file_path, chunk_size):
    chunk_duration = chunk_size / 1000  # Duration of each chunk in seconds

    with wave.open(file_path, 'rb') as audio_file:
        frame_rate = audio_file.getframerate()  # Get the frame rate (sample rate)

        chunk_frames = int(frame_rate * chunk_duration)

        chunks = []
        while True:
            chunk_data = audio_file.readframes(chunk_frames)
            print("chunck", chunk_data)
            if len(chunk_data) == 0:
                break
            chunks.append(chunk_data)

    return chunks
