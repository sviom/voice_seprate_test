import librosa
import soundfile as sf
import numpy as np
import os


def separate_audio(
    input_file, output_path, silence_threshold=20, frame_length=2048, hop_length=512
):
    # Load audio file
    y, sr = librosa.load(input_file, sr=None)

    # Compute short-term energy
    energy = np.array(
        [sum(abs(y[i : i + frame_length] ** 2)) for i in range(0, len(y), hop_length)]
    )

    # Convert energy to dB
    log_energy = 10 * np.log10(energy + 1e-6)

    # Detect non-silent frames
    non_silent_frames = log_energy > -silence_threshold
    non_silent_times = librosa.frames_to_time(
        np.where(non_silent_frames)[0], sr=sr, hop_length=hop_length
    )

    # Split non-silent times into continuous intervals
    intervals = librosa.util.contiguous_regions(non_silent_frames)

    # Output non-silent and silent audio files
    os.makedirs(output_path, exist_ok=True)

    non_silent_segments = []
    silent_segments = []

    for idx, (start, end) in enumerate(intervals):
        start_sample = int(librosa.frames_to_samples(start))
        end_sample = int(librosa.frames_to_samples(end))
        non_silent_segments.append((start_sample, end_sample))

    prev_end = 0
    for start, end in non_silent_segments:
        if prev_end < start:
            silent_segments.append((prev_end, start))
        prev_end = end
    if prev_end < len(y):
        silent_segments.append((prev_end, len(y)))

    def save_segments(segments, prefix):
        for idx, (start, end) in enumerate(segments):
            segment_audio = y[start:end]
            start_time = librosa.samples_to_time(start, sr=sr)
            end_time = librosa.samples_to_time(end, sr=sr)
            sf.write(
                os.path.join(
                    output_path, f"{prefix}_{start_time:.2f}_{end_time:.2f}.wav"
                ),
                segment_audio,
                sr,
            )

    save_segments(non_silent_segments, "non_silent")
    save_segments(silent_segments, "silent")


# Example usage:
input_file = "example.wav"
output_path = "output_segments"
separate_audio(input_file, output_path)
