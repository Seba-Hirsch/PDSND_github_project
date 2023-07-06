import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'Udacity/Python project/chicago.csv',
              'new york': 'Udacity/Python project/new_york_city.csv',
              'washington': 'Udacity/Python project/washington.csv' }
              
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to analyze: Chicago, New York, or Washington?\n").lower()
        if city not in CITY_DATA:
            print('please choose a valid city name')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to analyze; January, February, March, April, May, or June? Otherwise, type 'all' to see the combined data\n").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print('please choose a valid month')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day of the week would you like to analyze; Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Otherwise, type 'all' to see the combined data\n").lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print('please choose a valid day')
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])


    # Remove leading and trailing spaces from column names
    df.columns = df.columns.str.strip()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', pop_start_station)

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', pop_end_station)

    # display most frequent combination of start station and end station trip
    pop_trip = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('Most popular trip is: ', pop_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_time)

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Average travel time: ", avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print("Count of user types:\n" ,user_count)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nCount of gender types:\n", gender_count)
    except KeyError:
        print("\nCount of gender types: No data available for this selection.")

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_users = df['Birth Year'].min()
        print("\nThe oldest users' year of birth is: ", oldest_users) 
    except KeyError:
        print("\nThe oldest users' year of birth is: No data available for this selection.")

    try:
        youngest_users = df['Birth Year'].max()
        print("\nThe youngest users' year of birth is: ", youngest_users)
    except KeyError:
        print("\nThe youngest users' year of birth is: No data available for this selection.")
    
    try:
        most_common_users = df['Birth Year'].mode()[0]
        print("\nThe most common year of birth is:",most_common_users)
    except KeyError:
        print("\nThe most common year of birth is: No data available for this selection.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of raw data to the user for the selected combination."""
    
    i = 0
    data = input('\nWould you like to see the first 5 rows of data?\n').lower()
    while True:
        if data == 'no':
            break
        print(df[i : i+5])
        data = input('\nWould you like to see the next 5 rows of data?\n').lower()
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nThank you for exploring this data, until next time\n")
            break


if __name__ == "__main__":
    main()