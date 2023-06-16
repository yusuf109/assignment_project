import webrtcvad
from flask import Flask, request, jsonify
from pydantic import BaseModel


app = Flask(__name__)


class Frame(BaseModel):
    data: bytes


@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame = request.data

    # Validate frame size and bytes
    if not isinstance(frame, bytes):
        return jsonify({"error": "Invalid frame size or bytes"})

    # Assuming speech ends after 500ms
    chunk_size = 500
    accumulated_frames = []

    accumulated_frames.append(frame)

    if len(accumulated_frames) >= chunk_size:
        # Check if speech has ended
        speech_ended = check_speech_ended(accumulated_frames)
        if speech_ended:
            accumulated_frames = []
            return jsonify({"result": True})

    return jsonify({"result": False})


def check_speech_ended(accumulated_frames):
    vad = webrtcvad.Vad()
    vad.set_mode(3)  # Set the aggressiveness level (0-3, 3 being the most aggressive)

    # Convert accumulated frames to a waveform
    waveform = bytearray(b''.join(accumulated_frames))

    # Detect speech segments using VAD
    frame_duration = 20  # Duration of each frame in milliseconds
    chunk_duration = 500  # Duration of each speech chunk in milliseconds
    frames_per_chunk = int(chunk_duration / frame_duration)

    speech_ended = False
    for duration in range(0, len(waveform), frame_duration):
        frame = waveform[duration: duration+frame_duration]
        is_speech = vad.is_speech(frame, sample_rate=16000)

        if is_speech:
            # Speech detected, continue accumulating frames
            accumulated_frames.append(frame)

            # Check if chunk size (500ms) is reached
            if len(accumulated_frames) >= frames_per_chunk:
                speech_ended = True
                break
        else:
            # Non-speech detected, reset accumulated frames
            accumulated_frames = []

    return speech_ended


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
