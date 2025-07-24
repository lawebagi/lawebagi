import sounddevice as sd
import numpy as np
import wave
import whisper
import os

def record_audio(filename: str, duration: int = 5, samplerate: int = 44100):
    """
    Records audio for a given duration and saves it to a WAV file.
    
    Parameters:
      filename (str): Path to output WAV file.
      duration (int): Duration to record in seconds.
      samplerate (int): Sampling rate, default is 44100 Hz.
    """
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording complete. Saving to file.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

def transcribe_audio(filename: str) -> str:
    """
    Transcribes the given audio file using the Whisper model.
    
    Parameters:
      filename (str): Path to the input WAV file.
    
    Returns:
      str: Transcribed text.
    """
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Transcribing audio...")
    
    result = model.transcribe(filename)
    transcription = result.get("text", "").strip()
    print("Transcription complete.")
    
    return transcription

if __name__ == "__main__":
    AUDIO_FILENAME = "meeting_recording.wav"
    
    # Record a short audio clip (adjust duration as needed)
    record_audio(AUDIO_FILENAME, duration=5)
    
    # Check if the recording is saved properly before transcription
    if os.path.exists(AUDIO_FILENAME):
        transcript = transcribe_audio(AUDIO_FILENAME)
        print("Transcript:")
        print(transcript)
    else:
        print("Audio file not found. Please check the recording step.")