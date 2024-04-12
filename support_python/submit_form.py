contact=request.form['mobile_num']
    venue = request.form['venue']
    second_venue = request.form['venue_second']
    event_name=request.form['event_name']
    purpose = request.form['purpose']
    capacity=request.form['capacity']
    datep = request.form['date']
    time = request.form['time']

    print(time)
    print(type(time))

    # Original datetime string
    original_datetime = datep

    # Convert the string to a datetime object
    dt_object = datetime.strptime(original_datetime, "%Y-%m-%dT%H:%M")

    # Extract date and time components
    date_component = dt_object.strftime("%d/%m/%Y")
    time_component = dt_object.strftime("%H:%M:%S")

    print("Date:", date_component)
    print("Time:", time_component)

    data = {
        # 'fullname': [fullname],
        'Name' : session.get('username', 'Unknown'),
        # 'email': [email],
        'College_Email' : session.get('email', 'Unknown'),
        'Contact_Number': contact,
        'Event_Name': event_name,
        'Event_Date': date_component,
        'Capacity': capacity,
        'Event_Time' : time_component,
        'Event_Duration': time,
        'Venue_Selection': venue,
        'Purpose': purpose,
        'Status' : 'Pending',
        '2nd Choice': second_venue
    }
    # data = {
    #     'Name': [session.get('username', 'Unknown')],
    #     'College_Email': [session.get('email', 'Unknown')],
    #     'Contact_Number': [contact],
    #     'Event_Name': [event_name],
    #     'Event_Date': [date_component],
    #     'Capacity': [capacity],
    #     'Event_Time': [time_component],
    #     'Event_Duration': [time],
    #     'Venue_Selection': [venue],
    #     'Purpose': [purpose],
    #     'Status': ['Pending'],
    #     '2nd Choice': [second_venue]
    # }

    # Create a DataFrame using the dictionary
    df = pd.DataFrame(data,index=[0])
    print('--------------------------')
    print(df)

    # Construct file path for booking based on venue selection
    file_path_booking =str(venue) + "_booking.csv"


    if os.path.exists(file_path_booking) and os.path.getsize(file_path_booking) > 0:
        # Read existing booking DataFrame
        booking_df = pd.read_csv(file_path_booking)
        if ((booking_df['Event_Name'] == session.get('username', 'Unknown')) & (booking_df['Event_Date'] == date_component)).any():
            print("Booking with the same Name and Date already exists. Skipping...")
            return
    else:
        # Create an empty booking DataFrame if the file doesn't exist or is empty
        booking_df = pd.DataFrame()

    
    
    # booking_df
    # new_row_data = response_last_row

    conn = mysql.connector.connect(
    host="localhost",
    user="arnav-rppoop1",
    password="Guitar@123",
    database="db_2"
    )   

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the username for which you want to retrieve the role
    desired_username = session.get('username', 'Unknown')

    # Define your SQL query
    sql_query = "SELECT role FROM accounts WHERE username = %s"

    # Execute the SQL query
    cursor.execute(sql_query, (desired_username,))

    # Fetch the result
    role = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    conn.close()

    print('--------------------------------------------------')
    match_found = False
    if (role == 'User'):
        for index, row in booking_df.iterrows():
            # Check if event dates match
            if row['Event_Date'] == date_component:
                # Convert event times to datetime objects for comparison
                event_time = pd.to_datetime(row['Event_Time'])
                new_event_time = pd.to_datetime(time_component)

                # Calculate end time of existing event
                end_time = event_time + pd.Timedelta(hours=row['Event_Duration'])

                # Check if the new event time falls within the existing event slot
                if new_event_time >= event_time and new_event_time < end_time:
                    print('Cannot add the slot, as it overlaps with an existing booking.')
                    match_found = True
                    break
        
    if (match_found == False):

        # Append the new row to the booking DataFrame
        booking_df = booking_df._append(data, ignore_index=True)

        # Drop duplicate rows if any
        booking_df = booking_df.drop_duplicates()
        print(booking_df)

        # Save the booking DataFrame to CSV file
        booking_df.to_csv(file_path_booking, index=False)

        print("Booking processed and saved successfully.")


    name_arr.append(session.get('username', 'Unknown'))
    email_arr.append(session.get('email', 'Unknown'))
    contact_arr.append(contact)
    event_name_arr.append(event_name)
    event_date_arr.append(date_component)
    capacity_arr.append(capacity)
    event_time_arr.append(time_component)
    event_duration_arr.append(time)
    venue_selection_arr.append(venue)
    purpose_arr.append(purpose)
    status_arr.append('Pending')
    second_choice_arr.append(second_venue)
