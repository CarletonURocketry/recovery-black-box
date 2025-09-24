from machine import Pin, PWM
import time

"""
This library allows you to play a given melody on a piezo buzzer

@Author: Nicolas Vargas & Polina Ilinykh
Last Updated: March 2, 2025
"""
#TODO!!!!!: Error handling, to avoid potential crashes or infinite loops


#buzzer = PWM(Pin(20))

tones = {
"B0": 31,
"C1": 33,
"C#1": 35,
"D1": 37,
"D#1": 39,
"E1": 41,
"F1": 44,
"F#1": 46,
"G1": 49,
"G#1": 52,
"A1": 55,
"A#1": 58,
"B1": 62,
"C2": 65,
"C#2": 69,
"D2": 73,
"D#2": 78,
"E2": 82,
"F2": 87,
"F#2": 93,
"G2": 98,
"G#2": 104,
"A2": 110,
"A#2": 117,
"B2": 123,
"C3": 131,
"C#3": 139,
"D3": 147,
"D#3": 156,
"E3": 165,
"F3": 175,
"F#3": 185,
"G3": 196,
"G#3": 208,
"A3": 220,
"A#3": 233,
"B3": 247,
"C4": 262,
"C#4": 277,
"D4": 294,
"D#4": 311,
"E4": 330,
"F4": 349,
"F#4": 370,
"G4": 392,
"G#4": 415,
"A4": 440,
"A#4": 466,
"B4": 494,
"C5": 523,
"C#5": 554,
"D5": 587,
"D#5": 622,
"E5": 659,
"F5": 698,
"F#5": 740,
"G5": 784,
"G#5": 831,
"A5": 880,
"A#5": 932,
"B5": 988,
"C6": 1047,
"C#6": 1109,
"D6": 1175,
"D#6": 1245,
"E6": 1319,
"F6": 1397,
"F#6": 1480,
"G6": 1568,
"G#6": 1661,
"A6": 1760,
"A#6": 1865,
"B6": 1976,
"C7": 2093,
"C#7": 2217,
"D7": 2349,
"D#7": 2489,
"E7": 2637,
"F7": 2794,
"F#7": 2960,
"G7": 3136,
"G#7": 3322,
"A7": 3520,
"A#7": 3729,
"B7": 3951,
"C8": 4186,
"C#8": 4435,
"D8": 4699,
"D#8": 4978,
}

# Change this to make the song slower or faster
tempo = 132;

# Calculate the duration of a whole note in ms
wholenote = (60000 * 2) / tempo

# Format of the melody array: notes of the melody followed by the duration of the note.
# A 4 indicates a quarter note, 8 an eighth , 16 sixteenth and so on.
# Negative numbers are used to represent dotted notes,
# so -4 represents a dotted quarter note (a quarter plus an eighth).
# A 0 indicates a note slide to the next note, with the next note's duration
# indicating the duration of the note slide
melody = [
  
#   Cantina Band - Star wars
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("REST",8), ("D5",8), ("REST",8),   ("A4",8), ("REST",8),   ("D5",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("D5",8),   ("REST",8), ("A4",8),   ("REST",8), ("G#4",8),  ("A4",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |     
     ("A4",8), ("G#4",8),  ("A4",8),  ("G4",8),    ("REST",8), ("G4",8),   ("A4",8), ("G4",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |          
     ("F4",-4),            ("REST",16), ("D4",16), ("D4",-8),  ("REST",16),("REST",4),
     
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("REST",8), ("D5",8), ("REST",8),   ("A4",8), ("REST",8),   ("D5",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("D5",8),   ("REST",8), ("A4",8),   ("REST",8), ("G#4",8),  ("A4",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("G4",8),("REST",8),  ("G4",4),               ("REST",8), ("F#4",8),  ("G4",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |     
     ("C5",8), ("A#4",8),  ("REST",8), ("A4",8),   ("REST",8), ("G4",8),   ("G4",16), ("REST",-8),
    
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("REST",8), ("D5",8), ("REST",8),   ("A4",8), ("REST",8),   ("D5",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",8), ("D5",8),   ("REST",8), ("A4",8),   ("REST",8), ("G#4",8),  ("A4",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("C5",8), ("REST",8), ("C5",4),               ("C5",8), ("A4",8),     ("G4",8), ("REST",8),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |   
     ("E4",0), ("F4",2),                           ("D4",4),               ("REST",4),
 
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("D4",2),                                     ("F4",2),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("A4",2),                                     ("C5",2),
#   |		1/4			  |			1/4			  |			1/4			  |			1/4			  |
     ("D#5",8),("REST",8), ("D5",8), ("REST",8),   ("G#4",8), ("A4",8),    ("REST",8), ("F4",4),
     
     ("REST",8),
]

melody2 = [
    #   |		1/4			  |			1/4			  |			1/4			  |			1/4			  | |			1/4			
         ("B5",8), ("REST",8), ("A5",8), ("REST",8),   ("C#5",4), ("REST",8),   ("E5",4), ("REST",8),   ("A5",4), ("REST",8),
    ]


# Function to play a note
def play_tone(pitch, duration, buzzer):
    if pitch == "REST":
        buzzer.duty_u16(0)
    else:
        buzzer.duty_u16(2000)    # Volume of Buzzer
        buzzer.freq(tones[pitch])
    time.sleep(duration / 1000)  # Convert ms to seconds

# Function to play a note slide
def play_slide(start_note, end_note, duration, buzzer):
    # Get the frequencies for the start and end notes 
    start_freq = tones[start_note]
    end_freq = tones[end_note]

    # Number of steps for the slide (adjust for smoother or quicker slides)
    steps = 10
    step_duration = duration / steps  # Duration of each step in milliseconds
    
    slide_range = end_freq - start_freq
    frequency_step = abs(slide_range) / steps  # Frequency change per step
    stepDir = int(slide_range / abs(slide_range)) # Direction of slide (slide down or up)

    
    # Slide from start note to end note
    for i in range(steps):
        current_freq = start_freq + (frequency_step * i * stepDir)
        buzzer.duty_u16(2000)             # Volume of Buzzer
        buzzer.freq(int(current_freq))
        time.sleep(step_duration / 1000)  # Convert to seconds

# Calculate the note duration
def note_duration(divider):
    if divider > 0:
        note_duration = wholenote / divider
    elif divider < 0:
        note_duration = wholenote / abs(divider)
        note_duration *= 1.5  # Dotted notes have 1.5x the duration
    return note_duration

# Iterate over the melody
def play_melody(buzzer, melody):
    isSlide = 0
    slide_start = 0
    for i in range(len(melody)):   
        pitch, divider = melody[i]
        
        if divider == 0:
            slide_start = pitch
            isSlide = 1
            continue
        
        if isSlide:
            slide_end = pitch
            slide_length = note_duration(divider)
            play_slide(slide_start, slide_end , slide_length, buzzer)
            isSlide = 0
            
        else:
            note_length = note_duration(divider)
            play_tone(pitch, note_length, buzzer)

            
    buzzer.duty_u16(0)

#play_melody(buzzer)

