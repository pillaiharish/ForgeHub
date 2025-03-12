import re
import time
import pygame
import numpy as np

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

# Mapping of Sanskrit letters to Indian Classical Notes
sanskrit_to_notes = {
    'अ': 'Sa', 'आ': 'Re', 'इ': 'Ga', 'ई': 'Ma', 'उ': 'Pa', 'ऊ': 'Dha', 'ऋ': 'Ni',
    'ए': 'Sa', 'ऐ': 'Re', 'ओ': 'Ga', 'औ': 'Ma', 'क': 'Pa', 'ख': 'Dha', 'ग': 'Ni',
    'घ': 'Sa', 'च': 'Re', 'ज': 'Ga', 'झ': 'Ma', 'न': 'Pa', 'त': 'Dha', 'द': 'Ni',
    'ध': 'Sa', 'प': 'Re', 'ब': 'Ga', 'म': 'Ma', 'य': 'Pa', 'र': 'Dha', 'ल': 'Ni',
    'व': 'Sa', 'श': 'Re', 'स': 'Ga', 'ह': 'Ma',

    # Romanized Sanskrit
    'a': 'Sa', 'aa': 'Re', 'i': 'Ga', 'ii': 'Ma', 'u': 'Pa', 'uu': 'Dha', 'ri': 'Ni',
    'e': 'Sa', 'ai': 'Re', 'o': 'Ga', 'au': 'Ma', 'ka': 'Pa', 'kha': 'Dha', 'ga': 'Ni',
    'cha': 'Sa', 'ja': 'Re', 'na': 'Ga', 'ta': 'Ma', 'da': 'Pa', 'dha': 'Dha', 'pa': 'Ni',
    'ba': 'Sa', 'ma': 'Re', 'ya': 'Ga', 'ra': 'Ma', 'la': 'Pa', 'va': 'Dha', 'sha': 'Ni',
    'sa': 'Sa', 'ha': 'Re'
}

# Indian Classical Notes to Frequencies (C4-based)
note_frequencies = {
    'Sa': 261.63,  # C4
    'Re': 293.66,  # D4
    'Ga': 329.63,  # E4
    'Ma': 349.23,  # F4
    'Pa': 392.00,  # G4
    'Dha': 440.00, # A4
    'Ni': 493.88   # B4
}

def generate_sine_wave(frequency, duration=0.5, sample_rate=44100):
    """Generate a sine wave for a given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = np.int16(wave * 32767)
    return pygame.sndarray.make_sound(audio)

def sanskrit_to_music(text):
    """
    Convert Sanskrit text (Devanagari or Romanized) into musical notes and play them.
    """
    notes = []
    if re.search("[\u0900-\u097F]", text):  # If Devanagari characters found
        notes = [sanskrit_to_notes.get(char, '-') for char in text]
    else:  # For Romanized Sanskrit
        words = text.split()
        notes = [sanskrit_to_notes.get(word.lower(), '-') for word in words]

    print(f"Generated Notes: {' '.join(notes)}")
    
    # Play each note if it has a valid frequency
    for note in notes:
        if note in note_frequencies:
            sound = generate_sine_wave(note_frequencies[note])
            sound.play()
            time.sleep(0.5)  # Delay between notes

# Example inputs
sanskrit_word_1 = "संगीत"  # Sanskrit word for "Music"
sanskrit_word_2 = "shanti"  # Romanized Sanskrit word for "Peace"

# Convert & Play
sanskrit_to_music(sanskrit_word_1)
time.sleep(4)
sanskrit_to_music(sanskrit_word_2)


# $ python music/music_gen.py 
# pygame 2.6.1 (SDL 2.28.4, Python 3.11.6)
# Hello from the pygame community. https://www.pygame.org/contribute.html
# Generated Notes: Ga - Ni - Dha
# Generated Notes: -