from sonify_screentime import sonify_screentime_data

# # Generate day tune for 2/4/2022-- somewhat high screentime day (207 mins)
# start_time = "2022-02-04 00:00:00"
# end_time = "2022-02-05 00:00:00"
# df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=20, interval='hour', note_duration=1.3, 
#                        output_midi="sound/feb_04_2022.mid", output_wav="sound/feb_04_2022.wav", soundfont="Grand_Piano.sf2")

# # Save df to a new file
# df.to_csv("data/feb_04_2022.csv", index=False)

# # Generate month tune for 2/2022
# start_time = "2022-02-02 00:00:00"
# end_time = "2022-03-02 00:00:00"
# df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=180, interval='day', note_duration=1.3, 
#                        output_midi="sound/feb_2022.mid", output_wav="sound/feb_2022.wav", soundfont="Grand_Piano.sf2")

# # Save df to a new file
# df.to_csv("data/feb_2022.csv", index=False)

# # Generate day tune for 5/25/2022-- very high screentime day (687 mins)
# start_time = "2022-05-25 00:00:00"
# end_time = "2022-05-26 00:00:00"
# df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=20, interval='hour', note_duration=1.3, 
#                        output_midi="sound/may_25_2022.mid", output_wav="sound/may_25_2022.wav", soundfont="Grand_Piano.sf2")

# # Save df to a new file
# df.to_csv("data/may_25_2022.csv", index=False)


# # Generate tune for 4/22/2022-- moderate screentime day (87 mins)
# start_time = "2022-04-22 00:00:00"
# end_time = "2022-04-23 00:00:00"
# df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=20, interval='hour', note_duration=1.3, 
#                        output_midi="sound/apr_22_2022.mid", output_wav="sound/apr_22_2022.wav", soundfont="Grand_Piano.sf2")

# # Save df to a new file
# df.to_csv("data/apr_22_2022.csv", index=False)

# # Generate tune for 2/2/2022-- low screentime day (22 mins)
# start_time = "2022-02-02 00:00:00"
# end_time = "2022-02-03 00:00:00"
# df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=20, interval='hour', note_duration=1.3, 
#                        output_midi="sound/feb_02_2022.mid", output_wav="sound/feb_02_2022.wav", soundfont="Grand_Piano.sf2")
# # Save df to a new file
# df.to_csv("data/feb_02_2022.csv", index=False)

# Generate tune for 6/26/2022-- median screentime day (191 mins)
start_time = "2022-06-26 00:00:00"
end_time = "2022-06-27 00:00:00"
df = sonify_screentime_data("data/screen.csv", start_time=start_time, end_time=end_time, target_screentime=20, interval='hour', note_duration=1.3, 
                       output_midi="sound/jun_26_2022.mid", output_wav="sound/jun_26_2022.wav", soundfont="Grand_Piano.sf2")

# Save df to a new file
df.to_csv("data/jun_26_2022.csv", index=False)
