import mido
from mido import Message, MidiFile, MidiTrack
import subprocess
import numpy as np
from pychord import find_chords_from_notes
from process_screen_data import clean_screen_data, process_screentime, intervalize_screentime

# List of note names (C, C#, D, D#, ..., B)
NOTE_LIST = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Convert MIDI note number to note name and octave, based on 60 = C4
def midi_to_note(midi_number):
    note_name = NOTE_LIST[midi_number % 12]  
    octave = (midi_number // 12) - 1   
    return note_name, octave

# Map screentime value to a MIDI pitch between 36 (C2) and 84 (C6),
# normalized to the range [0, max] where max is the maximum of the max recorded screentime and a benchmark value based on the interval
def map_screentime_to_pitch(screen_time, max_screentime, interval='day'):
    min_pitch, max_pitch = 36, 84
    
    # Set a benchmark value based on the interval
    if interval == 'day':
        benchmark = 300
    elif interval == 'week':
        benchmark = 2100
    elif interval == 'month':
        benchmark = 9000
    else:
        benchmark = 60
    return int(np.interp(screen_time, [0, max(max_screentime, benchmark)], [max_pitch, min_pitch])) 

def sonify_screentime(df, target_screentime, interval='day', bpm=120, note_duration=2, output_midi="screentime.mid", output_wav="screentime.wav", soundfont="Grand_Piano.sf2"):
    """
    Map screentime data to chords and generate a MIDI and WAV file from this data. 
    
    Parameters:
    - df: intervalized dataframe containing screentime totals per interval
    - target_screentime: threshold (in minutes) determining major/minor chords
    - interval: interval represented by screentime (default: 'day')
    - bpm: tempo for generated MIDI file (default: 120)
    - note_duration: duration of each note in seconds (default: 2)
    - output_midi: name of output MIDI file (default: "screentime.mid")
    - output_wav: name of output WAV file (default: "screentime.wav")
    - soundfont: path to soundfont file for FluidSynth (default: "Grand_Piano.sf2")

    Returns:
    - A new dataframe with added 'Chord' and 'Octave' columns showing the chords and octaves used for each datapoint
    """
    
    # Print each parameter
    print("Sonifying screentime...")
    print(f"Target Screentime: {target_screentime}")
    print(f"Interval: {interval}")
    print(f"BPM: {bpm}")
    print(f"Note Duration: {note_duration}")
    print(f"Output MIDI: {output_midi}")
    print(f"Output WAV: {output_wav}")
    print(f"Soundfont: {soundfont}")
    print()
    
    # Create a new MIDI file and track
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    # Set tempo
    tempo = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Create lists to store chords and octaves
    chords = []
    chord_octaves = []

    # Get max screentime across the data
    max_screentime = df['Screen Time (Mins)'].max()
    
    for _, row in df.iterrows():
        screentime = row['Screen Time (Mins)']
        
        # Determine base note
        base_note = map_screentime_to_pitch(screentime, max_screentime, interval=interval)

        # Select chord type: major if screentime < target, minor if screentime >= target
        if screentime < target_screentime:
            chord_notes = [base_note, base_note + 4, base_note + 7]
        else:
            chord_notes = [base_note, base_note + 3, base_note + 7]
        
        # Convert notes' MIDI numbers to note names and their octaves
        note_names = [] 
        octaves = []   
        for n in chord_notes:
            note_name, octave = midi_to_note(n)
            note_names.append(note_name)
            octaves.append(octave)
            
        chord_octave = octaves[0]  # Consider base note's octave as the chord octave

        # Get chord name using pychord and store it, along with the constituent notes and octave
        chord_matches = find_chords_from_notes(note_names)
        chord_name = chord_matches[0] if chord_matches else "Unknown"
        chords.append(f"{chord_name} ({', '.join(note_names)})")
        chord_octaves.append(chord_octave)

        # Build the chord
        for note in chord_notes:
            track.append(Message('note_on', note=note, velocity=64, time=0))

        # Release chord after 2 seconds
        track.append(Message('note_off', note=chord_notes[0], velocity=64, time=mido.second2tick(note_duration, midi.ticks_per_beat, tempo)))
        track.append(Message('note_off', note=chord_notes[1], velocity=64, time=0))
        track.append(Message('note_off', note=chord_notes[2], velocity=64, time=0))

    # Save MIDI file
    midi.save(output_midi)

    # Convert MIDI to WAV using FluidSynth
    subprocess.run(["fluidsynth", "-ni", soundfont, output_midi, "-F", output_wav, "-r", "44100"])

    # Add 'Chord' and 'Octave' columns to the dataframe
    df['Chord'] = chords
    df['Octave'] = chord_octaves

    # Print message confirming completion and outputted files
    print(f"Generated {output_wav} from {output_midi}")
    
    # Return dataframe with added 'Chord' and 'Octave' columns
    return df  


# Function to implement the entire pipeline
def sonify_screentime_data(file, start_time, end_time, target_screentime, interval, bpm, note_duration, output_midi="screentime.mid", output_wav="screentime.wav", soundfont="Grand_Piano.sf2"):
    """
    Clean, process, intervalize, and sonify screentime data.
    
    Parameters:
    - file: csv file containing screentime data
    - start_time: start time for the interval (inclusive)
    - end_time: end time for the interval (non-inclusive)
    - target_screentime: target screentime in minutes
    - interval: interval by which to group the data by ('hour', 'day', 'week', 'month')
    - bpm: tempo for generated MIDI file
    - note_duration: duration of each note in seconds
    """
    # Clean the screentime data
    clean_df = clean_screen_data(file)

    # Process the screentime data
    processed_df = process_screentime(clean_df)

    # Intervalize the screentime data
    intervalized_df = intervalize_screentime(processed_df, start_time, end_time, interval)

    # Sonify the screentime data
    df = sonify_screentime(intervalized_df, target_screentime, interval, bpm, note_duration, output_midi, output_wav, soundfont)
    
    # Return final dataframe
    return df