import requests
import wave
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/process_audio', methods=['POST'])
def process_audio():
    frames = split_audio_frames("app/assignment_audio.wav", chunk_size=20)
    results = []

    for frame in frames:
        response = requests.post(
            "http://localhost:6000/process_frame", data=frame)
        print("res", response.content)
        if response.ok:
            results.append(response.json())

    return jsonify(results)


def split_audio_frames(file_path, chunk_size):
    chunk_duration = chunk_size / 1000  # Duration of each chunk in seconds

    with wave.open(file_path, 'rb') as audio_file:
        frame_rate = audio_file.getframerate()

        chunk_frames = int(frame_rate * chunk_duration)

        chunks = []
        while True:
            chunk_data = audio_file.readframes(chunk_frames)
            if len(chunk_data) == 0:
                break
            chunks.append(chunk_data)

    return chunks


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
