import bcrypt

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re

app = Flask(__name__)

app.secret_key = 'Guitar'


# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'user': 'arnav-rppoop1',
    'password': 'Guitar@123',
    'database': 'db_2'
}

# Initialize MySQL connection
mysql_connection = mysql.connector.connect(**mysql_config)
print("helll")
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #     username = request.form['username']
    #     password = request.form['password']
    #     cursor = mysql_connection.cursor(dictionary=True)
    #     # cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
    #     cursor.execute('SELECT password FROM accounts WHERE username = %s', (username,))
    #     hashed_password = cursor.fetchone()
    #     account = cursor.fetchone()

    #     if account:
    #         session['loggedin'] = True
    #         session['id'] = account['id']
    #         session['username'] = account['username']
    #         session['du'] = 'Arnav Prasad'
    #         print(session)
    #         msg = 'Logged in successfully!'
    #         return render_template('index.html', msg=msg)
    #     else:
    #         msg = 'Incorrect username / password!'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            hashed_password = account['password']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Passwords match, log in the user
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['du'] = 'Arnav Prasad'
                session['email'] = account['email']
                msg = 'Logged in successfully!'
                print(session)
                return render_template('user_venue_booking_page.html', msg=msg)
            else:
                # Passwords do not match
                msg = 'Incorrect username / password!'
        else:
            # No account found for the given username
            msg = 'Incorrect username / password!'

    return render_template('login2.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash a password
            # password = b"mysecretpassword"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
            cursor.execute('INSERT INTO accounts (role,username, password, email) VALUES (%s , %s, %s, %s)', ('USER',username, hashed_password, email))
            mysql_connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register2.html', msg=msg)


#admin login and register functions: 

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'admin_password' in request.form:
        username = request.form['username']
        password = request.form['password']
        admin_password = request.form['admin_password']
        cursor = mysql_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            hashed_password = account['password']
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Passwords match, now check admin password
                if admin_password == 'hackathon':
                    # Admin login successful
                    session['admin_loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    session['loggedin'] = True
                    session['du'] = 'Arnav Prasad'
                    session['email'] = account['email']
                    msg = 'Admin logged in successfully!'
                    return render_template('admin_dashboard.html', msg=msg)
                else:
                    msg = 'Incorrect admin password!'
            else:
                # User password incorrect
                msg = 'Incorrect username / password!'
        else:
            # No account found for the given username
            msg = 'Incorrect username / password!'

    return render_template('admin_login.html', msg=msg)

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'admin_password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        admin_password = request.form['admin_password']
        cursor = mysql_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not admin_password:
            msg = 'Please fill out the form!'
        elif admin_password != 'hackathon':
            msg = 'Incorrect admin password!'
        else:
            # Hash a password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
            cursor.execute('INSERT INTO accounts (role,username, password, email) VALUES (%s , %s, %s, %s)', ('ADMIN',username, hashed_password, email))
            mysql_connection.commit()
            msg = 'Admin registered successfully!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('admin_register.html', msg=msg)


#ending of admin login and register functions.

# @app.route('/')
# def index():
#     return render_template('cards2.html')

@app.route('/display_request_form')
def requestform():
    return render_template('user_venue_request_form.html')

@app.route('/process_venue_booking_request')
def process_venue_booking_request():
    return render_template('venue_request_admin.html')


from datetime import datetime
import pandas as pd
import os

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # fullname = request.form['fullname']
    # email=request.form['email']
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


    
    # Now you have the form data in variables
    # You can process or store them as required
    # For demonstration, I'll just print them
    print(f"Fullname: {session.get('username', 'Unknown')}, email-id: {session.get('email', 'Unknown')}, Contact: {contact}, Venue: {venue},  second venue: {second_venue}, Event name: {event_name},  Purpose: {purpose}, Capacity: {capacity}, Date and start time: {datep}, Time: {time}")
    return render_template('user_venue_request_form.html')

@app.route('/display_admin_dashboard')
def display_admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/display_venue_request_admin')
def display_venue_request_admin():
    return render_template('venue_request_admin.html')

if __name__ == '__main__':
    app.run(debug=True)


print('done!!')