import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def split_audio_on_silence(input_file, silence_thresh=-50, min_silence_len=1.0):
    # Load the audio file
    y, sr = librosa.load(input_file)

    # Convert silence_thresh from dB to amplitude
    # silence_thresh_amp = librosa.db_to_amplitude(silence_thresh)
    # silence_thresh_amp = librosa.amplitude_to_db()
    # librosa.display.waveshow(y=y)
    # plt.show()

    # Find silent frames
    non_silent_intervals = librosa.effects.split(y, top_db=-silence_thresh)

    # Create a list to store audio chunks
    chunks = []

    # Iterate through non-silent intervals
    for start, end in non_silent_intervals:
        chunk = y[start:end]
        if librosa.get_duration(y=chunk, sr=sr) >= min_silence_len:
            chunks.append(chunk)

    return y, sr, chunks, non_silent_intervals


def save_audio_chunks(chunks, sr, base_filename):
    for i, chunk in enumerate(chunks):
        # Save each chunk as a separate WAV file
        sf.write(f"{base_filename}_{i}.wav", chunk, sr)


def plot_audio_with_intervals(y, sr, intervals):
    plt.figure(figsize=(14, 6))
    librosa.display.waveshow(y, sr=sr, alpha=0.5)
    for start, end in intervals:
        plt.axvspan(start / sr, end / sr, color="red", alpha=0.3)
    plt.title("Audio with Non-Silent Intervals Highlighted")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


# Usage Example
input_file = "audio.wav"  # Replace with your audio file path
base_filename = "output_chunk"
silence_thresh = -30  # Silence threshold in dB
min_silence_len = 1.0  # Minimum length of silence in seconds


# Split the audio and get the non-silent intervals
y, sr, chunks, non_silent_intervals = split_audio_on_silence(
    input_file, silence_thresh, min_silence_len
)

# Save the individual non-silent chunks
save_audio_chunks(chunks, sr, base_filename)

# Plot the audio with non-silent intervals
# plot_audio_with_intervals(y, sr, non_silent_intervals)
