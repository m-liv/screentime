import pandas as pd

def clean_screen_data(file, new_file="None"):
    """
    Clean the given screentime data by dropping unnecessary columns, renaming columns, and converting timestamp to datetime format.
    
    Parameters:
    - file: csv file containing screentime data to be cleaned
    - new_file: csv file to which to save the cleaned data (optional)

    Returns:
    - The cleaned data as a dataframe
    """
    # Read in screen.csv
    df = pd.read_csv(file)

    # Drop the first device_id column
    df = df.drop(columns=['device_id'])

    # Rename the device_id.1 column to screen_status
    df = df.rename(columns={'device_id.1': 'screen_status'})

    # Convert timestamp to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Drop the _id columns
    df = df.drop(columns=['_id'])
    
    # Save the cleaned data to a new file if requested
    if new_file != "None":
        df.to_csv(new_file, index=False)

    return df

def process_screentime(df, new_file="None"):
    """
    Process the screentime data by calculating screentimes as times elapsed between an unlock event and the next lock.  
    
    Parameters:
    - df: dataframe containing cleaned screentime data to be processed
    - new_file: csv file to which to save the processed data (optional)

    Returns:
    - A new dataframe with a column for timestamps (of lock events) and elapsed screen times in minutes.
    """
    # Convert string timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create dictionaries to map dates to screen times and last unlock times
    screen_times = []
    last_unlock_time = {}

    # Iterate through the rows of the dataframe, keeping track of the most recent unlock time for each day
    # For each lock event, calculate the time elapsed since the last unlock time and add it to the running screen time total for the current day
    for index, row in df.iterrows():
        timestamp = pd.to_datetime(row['timestamp'])
        date = timestamp.date()
        status = row['screen_status']
        
        if status == 3:  # Unlock event
            last_unlock_time[date] = timestamp
        elif status == 2 and date in last_unlock_time:  # Lock event
            unlock_time = last_unlock_time.pop(date)
            elapsed_time = (timestamp - unlock_time).seconds / 60
            screen_times.append({'Timestamp': timestamp, 'Screen Time (Mins)': elapsed_time})

    # Save results to a new dataframe
    screen_time_df = pd.DataFrame(screen_times)

    # Save the processed data to a new CSV file if requested
    if new_file != "None":
        screen_time_df.to_csv(new_file, index=False)
    
    return screen_time_df

def intervalize_screentime(df, start_time, end_time, interval='day', new_file="None"):
    """
    Group the screentime data into the specified intervals (hours, days, weeks, or months) 
    and calculate screen time totals for each interval.
    
    Parameters:
    - df: processed dataframe containing timestamps and screen time data
    - start_time: start time for the interval (inclusive)
    - end_time: end time for the interval (non-inclusive)
    - interval: interval by which to group the data by (hour, day, week, month) (default: day)
    - new_file: csv file to which to save the intervalized data (optional)

    Returns:
    - A new dataframe with the total screen time for each interval
    """
    df = df.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Filter out rows outside specified time range
    mask = (df['Timestamp'] >= start_time) & (df['Timestamp'] < end_time)
    df = df.loc[mask]
    
    # Create column to group rows into specified intervals (hours, days, weeks, or months)
    col_name = interval.capitalize()
    if (interval == 'hour'):
        # Add Hour column where each timestamp is rounded down to the nearest full hour
        df[col_name] = df['Timestamp'].dt.floor('H')
    elif (interval == 'day'):
        # Add Day column containing only the date portion of each timestamp
        df[col_name] = df['Timestamp'].dt.date
    elif (interval == 'week'):
        # Add Week column where each timestamp is converted to a weekly period 
        # and apply lambda to get start of that week
        df[col_name]  = df['Timestamp'].dt.to_period('W').apply(lambda r: r.start_time)
    elif (interval == 'month'):
        # Add Month column where each timestamp is converted to a monthly period
        # and apply lambda to get start of that month
        df[col_name]  = df['Timestamp'].dt.to_period('M').apply(lambda r: r.start_time)
        
    # Group dataframe by specified interval and sum screentime for each interval
    intervalized_df = df.groupby(col_name, as_index=False)['Screen Time (Mins)'].sum() 
    
    # Save the intervalized data to a new CSV file if requested
    if new_file != "None":
        intervalized_df.to_csv(new_file, index=False)
    
    # Return dataframe containing total screen time for each interval
    return intervalized_df
