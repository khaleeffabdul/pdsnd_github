import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\nHello! Dear, \n\tLet\'s explore some US bikeshare data!\n')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Kindly select any city\'s data you would like to explore, from the cities listed below: \
        \n\tchicago \n\tnew york city \n\twashington\n\ncity name~> ").lower()
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("\nInvalid input! Try again!!\n")
            continue
        else:
            break


        # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nKindly select any month you would like to filter the data by, from the list below: \
        \n\tJanuary \n\tFebruary \n\tMarch \n\tApril \n\tMay \n\tJune\n\nmonth~> ").lower()
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print("\nInvalid input! Try again!!\n")
            continue
        else:
            break


        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nKindly select any day of the week you would like to filter the data by using the format listed below: \
        \n\tmonday \n\ttuesday \n\twednesday \n\tthursday \n\tfriday \n\tsaturday \n\tsunday\n\nday~> ").lower()
        if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('\nInvalid input! Try again!!')
            continue
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from Start Time
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: {}'.format(common_day))

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    start_end_combo = df.groupby(['Start Station', 'End Station'])
    most_freq_combo_count = start_end_combo['Trip Duration'].count().max()
    most_freq_start_end_trip = start_end_combo['Trip Duration'].count().idxmax()
    print('The most frequent combination of start and end station trip is: {}, {}'.format(most_freq_start_end_trip[0], most_freq_start_end_trip[-1]))
    print('With a total trip of {}'.format(most_freq_combo_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is', total_travel_time/86400, "Days")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is ', average_travel_time/60, "munites")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('The user types and thier total number are:\n {}'.format(counts_of_user_types))

    # Display counts of gender
    try:
        print('Total gender count is:')
        counts_of_gender = df['Gender'].value_counts()
        print(counts_of_gender)
    except:
        print('There is no data available for this selection')


    # Display earliest, most recent, and most common year of birth
    try:
        print('Birth year statistics:')
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('The earliest year of birth is:' + str(earliest))
        print('The most recent year of birth:' + str(most_recent))
        print('The most common year of birth is:' + str(most_common))
    except:
        print('There is no data available for this selection')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Display_raw_data
def more_data(df):
    strt = 0
    raw_data = input('\nWould you like to see the raw data? \n Enter [Yes or No]:~> ')
    while raw_data.lower() == 'yes':
        first_ten_lines = df.iloc[strt: strt+10]
        print('The first ten lines of the raw data are: \n',first_ten_lines)
        strt += 10
        raw_data = input('\nWould you like to see ten more lines of the raw data? \n Enter [Yes or No]:~> ')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        more_data(df)

        restart = input('\nWould you like to esplore the US bikeshare data again? \n Enter [Yes or No]:~> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
