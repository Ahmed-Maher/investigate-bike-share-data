import time
from typing import Counter
import pandas as pd
from pandas.io.parsers import count_empty_vals

# I created a txt file to save the output into
result_file = open("bike share output.txt", "a")
result_file.write("-"*40)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('## Hello! Let\'s explore some US bikeshare data! ##')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("- Select a city:")
    cities = ["chicago", "new york city", "washington"]
    for num, value in enumerate(cities):
        print(f"     {num+1}) {value}")
    city_number = input("Enter your choice [Number]: ")
    
    cities_numbers = ["1", "2", "3"]
    while city_number not in cities_numbers:
        print("Please inter a valid answer!")
        city_number = input("Enter your choice [Number]: ")
    if city_number == cities_numbers[int(city_number)-1]:
        city = cities[int(city_number)-1]


    # get user input for month (all, january, february, ... , june)
    months = ["January",'February','March','April','May','June','All']
    print("- Select a month:")
    for index, item in enumerate(months):
        print(f"     {index+1}) {item}")  
        
    months_numbers = ["1", "2", "3", "4", "5", "6", "7"]
    month_number = input("Enter your choice [Number]: ")
    while month_number not in months_numbers:
        print("Please inter a valid answer!")
        month_number = input("Enter your choice [Number]: ")
    if month_number == months_numbers[int(month_number)-1]:
        month = months[int(month_number)-1]
  
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','All']
    print("- Select a day:")
    for n, v in enumerate(days):
        print(f"     {n+1}) {v}")
    
    days_numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
    day_number = input("Enter your choice [Number]: ")
    while day_number not in days_numbers:
        print("Please inter a valid answer!")
        day_number = input("Enter your choice [Number]: ")
    if day_number == days_numbers[int(day_number)-1]:
        day = days[int(day_number)-1]       

    print('-'*40)

    # print and save a summary of user choices
    result_file.write(f"""\n- You chose:
    city = {city}
    month = {month}
    day = {day}\n""")
    result_file.write("-"*40)

    print(f"""\n- You chose:
    city = {city}
    month = {month}
    day = {day}\n""")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # added 'month name' col to print the month name later in the most common month section
    df["month name"] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    result_file.write('\nCalculating The Most Frequent Times of Travel...\n\n')
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df["month name"].mode()[0]
    result_file.write(f"- The most popular month is: {popular_month}\n")
    print(f"- The most popular month is: {popular_month}")

    # display the most common day of week
    df['day'] = df["Start Time"].dt.day_name()
    popular_day = df["day"].mode()[0]
    result_file.write(f"- The most popular day of the week is: {popular_day}\n")
    print(f"- The most popular day of the week is: {popular_day}")

    # display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]
    result_file.write(f"- The most popular hour is: {popular_hour}\n")
    print(f"- The most popular hour is: {popular_hour}")

    result_file.write("\nThis took %s seconds." % (time.time() - start_time))
    result_file.write('\n')
    result_file.write('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    result_file.write('\nCalculating The Most Popular Stations and Trip...\n\n')
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    result_file.write(f"- The most popular Start Station is: {popular_start_station}\n")
    print(f"- The most popular Start Station is: {popular_start_station}")

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    result_file.write(f"- The most popular End Station is: {popular_end_station}\n")
    print(f"- The most popular End Station is: {popular_end_station}")

    # display most frequent combination of start station and end station trip
    start_end_station = df["start_end_station"] = df["Start Station"] + " ==> " + df["End Station"]
    start_end_station = df["start_end_station"].mode()[0]
    result_file.write(f"- The most popular trip is: {start_end_station}\n")
    print(f"- The most popular trip is: {start_end_station}")

    result_file.write("\nThis took %s seconds." % (time.time() - start_time))
    result_file.write('\n')
    result_file.write('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    result_file.write('\nCalculating Trip Duration...\n\n')
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # calculate total travel time and turn it into hours then round the num to the 4th digit
    total_travel_time = round(df["Trip Duration"].sum() / 60 / 60, 4)
    result_file.write(f"- The total travel time is: {total_travel_time} hours\n")
    print(f"- The total travel time is: {total_travel_time} hours")

    # display mean travel time
    # calculate average travel time and turn it into hours then round the num to the 4th digit
    avrg_travel_time = round(df["Trip Duration"].mean() / 60 / 60, 4)
    result_file.write(f"- The average travel time is: {avrg_travel_time} hours\n")
    print(f"- The average travel time is: {avrg_travel_time} hours")

    result_file.write("\nThis took %s seconds." % (time.time() - start_time))
    result_file.write('\n')
    result_file.write('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    result_file.write('\nCalculating User Stats...\n\n')
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    result_file.write("# User Type #\n")
    print("# User Type #")
    user_type = df['User Type'].value_counts()
    subscriber = user_type[0]
    customer = user_type[1]
    result_file.write(f"- The subscriber count is: {subscriber}\n")
    result_file.write(f"- The customer count is: {customer}\n\n")
    print(f"- The subscriber count is: {subscriber}")
    print(f"- The customer count is: {customer}\n")

    # Display counts of gender
    result_file.write("# Gender Type #\n")
    print("# Gender Type #")
    # check if the Gender col is avalible
    try:    
        gender_type = df['Gender'].value_counts()
        male = gender_type[0]
        female = gender_type[1]
        result_file.write(f"- The Male count is: {male}\n")
        result_file.write(f"- The Female count is: {female}\n")
        print(f"- The Male count is: {male}")
        print(f"- The Female count is: {female}")        
    except:
        result_file.write("Gender statistics is not available!\n")
        print("Gender statistics is not available!")

    # Display earliest, most recent, and most common year of birth
    result_file.write("\n# Year of birth #")
    print("\n# Year of birth #\n")
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        result_file.write(f"- The earliest year is: {str(earliest)[:4]}\n")
        result_file.write(f"- The most recent year is: {str(most_recent)[:4]}\n")
        result_file.write(f"- The most common year is: {str(most_common[0])[:4]}\n")
        print(f"- The earliest year is: {str(earliest)[:4]}")
        print(f"- The most recent year is: {str(most_recent)[:4]}")
        print(f"- The most common year is: {str(most_common[0])[:4]}")
    except:
        result_file.write("Birth year statistics is not available!")
        print("Birth year statistics is not available!\n")


    result_file.write("\nThis took %s seconds." % (time.time() - start_time))
    result_file.write('\n')
    result_file.write('#'*60)
    result_file.write('\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''Show five rows of the data'''
    
    print("- Would you like to view the first 5 rows of individual trip data? :")
    print("     1) Yes.")
    print("     2) No.")
    view_data = input("Enter your choice [Number]: ")
    start_loc = 0
    
    
    x = True
    while view_data == "1" and x == True:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        while True:
            print("Do you wish to view the next 5 rows?:")
            print("     1) Yes.")
            print("     2) No.")        
            view_display = input("Enter your choice [Number]: ")
            if df.iloc[start_loc:start_loc+5].empty:
                print("Ther is no more rows!")
                x = False
                break
            else:
                if view_display == "1":
                    break
                elif view_display == "2":
                    x = False
                    break
                else:
                    print("\nPlease inter a valid answer!")
                    continue

    if view_data != "1" and view_data != "2":
        print("\nPlease inter a valid answer!")
        display_data(df)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        
        print("\n## Statistics results has been saved in [bike share output.txt] ##\n")
        print("- Would you like to restart?")
        print("     1) Yes")
        print("     2) No")
        restart = input("Enter your choice [Number]: ")
        while restart != '1' and restart != "2":
            print("Please inter a valid answer!")
            restart = input("Enter your choice [Number]: ")
        if restart == "2":
            break
            
    
if __name__ == "__main__":
	main()

result_file.close()