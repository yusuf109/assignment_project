import webrtcvad

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class Frame(BaseModel):
    data: bytes


@app.post("/process_frame")
def process_frame(request: Request):
    frame: Frame = request.body()

    # Validate frame size and bytearray
    if not isinstance(frame, bytearray):
        return {"error": "Invalid frame size or bytearray"}

    # Assuming speech ends after 500ms
    chunk_size = 500
    accumulated_frames = []

    accumulated_frames.append(frame)

    if len(accumulated_frames) >= chunk_size:
        # Check if speech has ended
        speech_ended = check_speech_ended(accumulated_frames)
        if speech_ended:
            accumulated_frames = []
            return {"result": True}

    return {"result": False}


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
