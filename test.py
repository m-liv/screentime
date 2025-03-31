from sonify_screentime import sonify_screentime_data

start_time = "2022-02-02 00:00:00"
end_time = "2022-03-02 00:00:00"
df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=180, interval='day', bpm=120, note_duration=2, 
                       output_midi="sound/feb_2022.mid", output_wav="sound/feb_2022.wav", soundfont="Grand_Piano.sf2")

# Save df to a new file
df.to_csv("data/feb_2022.csv", index=False)