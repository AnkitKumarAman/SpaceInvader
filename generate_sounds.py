import os
import wave
import struct
import math
import random

SAMPLE_RATE = 44100

def save_wav(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # mono
        f.setsampwidth(2) # 2 bytes (16-bit)
        f.setframerate(SAMPLE_RATE)
        for val in data:
            val = max(-32768, min(32767, int(val * 32767)))
            f.writeframesraw(struct.pack('<h', val))

def gen_laser():
    duration = 0.15
    num_samples = int(SAMPLE_RATE * duration)
    data = []
    phase = 0.0
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        freq = 800 - (800 - 150) * (t / duration)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        envelope = 1.0 - (t / duration) * 0.5
        val = math.sin(phase) * envelope
        data.append(val)
    return data

def gen_rapid_laser():
    duration = 0.08
    num_samples = int(SAMPLE_RATE * duration)
    data = []
    phase = 0.0
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        freq = 1200 - (1200 - 400) * (t / duration)
        phase += 2 * math.pi * freq / SAMPLE_RATE
        envelope = 1.0 - (t / duration) * 0.7
        val = math.sin(phase) * envelope
        data.append(val)
    return data

def gen_explosion():
    duration = 0.5
    num_samples = int(SAMPLE_RATE * duration)
    data = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-6.0 * t)
        val = (random.random() * 2.0 - 1.0) * envelope
        data.append(val)
    return data

def gen_game_over():
    tones = [400, 320, 260, 180]
    tone_duration = 0.25
    data = []
    for tone in tones:
        num_samples = int(SAMPLE_RATE * tone_duration)
        phase = 0.0
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            phase += 2 * math.pi * tone / SAMPLE_RATE
            envelope = math.exp(-3.0 * t)
            val = math.sin(phase) * envelope
            data.append(val)
    return data

def gen_powerup():
    notes = [523.25, 659.25, 783.99]
    note_duration = 0.08
    data = []
    for note in notes:
        num_samples = int(SAMPLE_RATE * note_duration)
        phase = 0.0
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            phase += 2 * math.pi * note / SAMPLE_RATE
            envelope = 1.0 - (t / note_duration) * 0.4
            val = math.sin(phase) * envelope
            data.append(val)
    return data

def gen_game_music():
    bpm = 120
    beat_duration = 60.0 / bpm
    melody = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63, 0]
    bass = [130.81, 130.81, 196.00, 196.00, 220.00, 220.00, 174.61, 174.61]
    total_duration = len(melody) * beat_duration
    num_samples = int(SAMPLE_RATE * total_duration)
    data = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        beat_idx = int(t / beat_duration) % len(melody)
        t_in_beat = t % beat_duration
        freq_mel = melody[beat_idx]
        mel_val = 0.0
        if freq_mel > 0:
            mel_phase = 2 * math.pi * freq_mel * t
            mel_val = 1.0 if math.sin(mel_phase) > 0 else -1.0
            mel_val *= math.exp(-4.0 * t_in_beat) * 0.15
        freq_bass = bass[beat_idx]
        bass_val = 0.0
        if freq_bass > 0:
            bass_phase = (freq_bass * t) % 1.0
            bass_val = 4.0 * abs(bass_phase - 0.5) - 1.0
            bass_val *= 0.25
        mix_val = mel_val + bass_val
        data.append(mix_val)
    return data

if __name__ == '__main__':
    print("Generating sounds...")
    save_wav("Sound/laser.wav", gen_laser())
    save_wav("Sound/rapid_fire_sound.wav", gen_rapid_laser())
    save_wav("Sound/explosion.wav", gen_explosion())
    save_wav("Sound/game_over.wav", gen_game_over())
    save_wav("Sound/game_music.wav", gen_game_music())
    save_wav("Sound/powerup.wav", gen_powerup())
    print("All sounds generated successfully!")
