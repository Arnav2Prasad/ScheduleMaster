import pandas as pd

daysList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

df = pd.read_csv('sy_division1_timetable.csv')
print(df)

# Define the dimensions of the lists
rows = 8  # Corrected from 9 to 8
cols = 5  # Corrected from 7 to 6

# Create lists with zeros
l_201 = [[0] * cols for _ in range(rows)]
l_202 = [[0] * cols for _ in range(rows)]
l_203 = [[0] * cols for _ in range(rows)]

print(daysList.index('Monday'))

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access individual elements using column names
    if row['subject'] is not None:
        day = row['day']
        venue = row['venue']
        time = row['start_time']
        if 9 <= time <= 16:
            if venue == 201:  # Removed conversion to float
                l_201[time - 9][daysList.index(day)] = 1
            elif venue == 202:  # Removed conversion to float
                l_202[time - 9][daysList.index(day)] = 1
            elif venue == 203:  # Removed conversion to float
                l_203[time - 9][daysList.index(day)] = 1

df = pd.read_csv('sy_division2_timetable.csv')
print(df)

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access individual elements using column names
    if row['subject'] is not None:
        day = row['day']
        venue = row['venue']
        time = row['start_time']
        if 9 <= time <= 16:
            if venue == 201:  # Removed conversion to float
                l_201[time - 9][daysList.index(day)] = 1
            elif venue == 202:  # Removed conversion to float
                l_202[time - 9][daysList.index(day)] = 1
            elif venue == 203:  # Removed conversion to float
                l_203[time - 9][daysList.index(day)] = 1

df = pd.read_csv('ty_division1_timetable.csv')
print(df)

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access individual elements using column names
    if row['subject'] is not None:
        day = row['day']
        venue = row['venue']
        time = row['start_time']
        if 9 <= time <= 16:
            if venue == 201:  # Removed conversion to float
                l_201[time - 9][daysList.index(day)] = 1
            elif venue == 202:  # Removed conversion to float
                l_202[time - 9][daysList.index(day)] = 1
            elif venue == 203:  # Removed conversion to float
                l_203[time - 9][daysList.index(day)] = 1

df = pd.read_csv('ty_division2_timetable.csv')
print(df)

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Access individual elements using column names
    if row['subject'] is not None:
        day = row['day']
        venue = row['venue']
        time = row['start_time']
        if 9 <= time <= 16:
            if venue == 201:  # Removed conversion to float
                l_201[time - 9][daysList.index(day)] = 1
            elif venue == 202:  # Removed conversion to float
                l_202[time - 9][daysList.index(day)] = 1
            elif venue == 203:  # Removed conversion to float
                l_203[time - 9][daysList.index(day)] = 1


print(l_201)
# print(l_202)
# print(l_203)

d = pd.DataFrame(l_201)
d.index = d.index + 9
d.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
d.to_csv('AC_201.csv')
print(d)


d = pd.DataFrame(l_202)
d.index = d.index + 9
d.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
d.to_csv('AC_202.csv')
print(d)

d = pd.DataFrame(l_203)
d.index = d.index + 9
d.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
d.to_csv('AC_203.csv')
print(d)

# 0 is for empty
# 1 is not empty    