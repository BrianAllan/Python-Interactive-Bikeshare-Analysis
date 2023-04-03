import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_dictionary =  {'c': 'chicago',
                    'n': 'new york city',
                    'w': 'washington'}
month_dictionary = {'1': 'january',
                    '2': 'february',
                    '3': 'march',
                    '4': 'april',
                    '5': 'may',
                    '6': 'june'}
day_dictionary =   {'1': 'monday',
                    '2': 'tuesday',
                    '3': 'wednesday',
                    '4': 'thursday',
                    '5': 'friday',
                    '6': 'saturday',
                    '7': 'sunday'}

separator = '-'*40



def get_month():
    """
    Requests  user to select which month by which to filter the data.

    Returns:
        (str) month - name of the month to filter by
    """
    # get user input for month (january, february, ... , june)
    while True:
        print('Which month\'s data would you like to analyze?')

        month = input('Enter the number corresponding to the desired month: \n(1) January, (2) February, (3) March, (4) April, (5) May, (6) June:  ').lower()

        if month in month_dictionary:
            month = month_dictionary[month]
            break
        else:
            print('\nYour response was not one of the options.  Let\'s try again!\n')

    print(separator)
    return(month)


def get_day():
    """
    Requests user to select which day of the week by which to filter the data.

    Returns:
        (str) day - name of the day of the week to filter by
    """
    # get user input for day of week (monday, tuesday, ... sunday)
    while True:
        print('Which day of the week would you like to use for your data analysis?')

        day = input('Enter the number corresponding to the desired day: \n(1) Monday, (2) Tuesday, (3) Wednesday, (4) Thursday, (5) Friday, (6) Saturday, (7) Sunday:  ').lower()

        if day in day_dictionary:
            break
        else:
            print('\nYour response was not one of the options.  Let\'s try again!\n')

    print(separator)
    return(day)



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    print('The data is provided by the bikeshare system provider Motivate for three large cities: Chicago, New York City, and Washington DC.')
    print('The data sets consist of randomly selected data for the first six months (January through June) of 2017.')
    bike_string = """

          /-/    ___
        ____|=====|=____
       /    \      /    \\
       \____/      \____/

    """
    print(bike_string)

    # get user input for city (chicago, new york city, washington).
    while True:
        print('Which city\'s bikeshare data would you like to analyze?')

        city = input('Enter \'c\' for Chicago, \'n\' for New York City, or \'w\' for Washington DC:  ').lower()

        if city in city_dictionary:
            city = city_dictionary[city]
            break
        else:
            print('\nYour response was not one of the options.  Let\'s try again!\n')

    print(separator)

    # get user input for time filter -- month, day, both, or none
    while True:
        print('You can filter the {} data by month (\'m\'), by day of week (\'d\'), by both month and day of week (\'b\'), \nor you can choose not to use any time filter, thereby selecting all months and days of the week (\'a\').'.format(city.title()))
        time_filter = input('Please make your selection: ').lower()

        if time_filter == 'a':
            month = 'all'
            day = 'all'
            break
        elif time_filter == 'm':
            month = get_month()
            day = 'all'
            break
        elif time_filter == 'd':
            month = 'all'
            day = get_day()
            break
        elif time_filter == 'b':
            month = get_month()
            day = get_day()
            break
        else:
            print('\nYour response was not one of the options.  Let\'s try again!\n')

    return city, month, day



def check_input(city, month, day):
    """
    Checks with user that the selection was as intended.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (bool) True if selection was as user intended, False if otherwise
    """

    while True:
        print('\nYour selection was...\nCity: {}\nMonth: {}\nDay of Week: {}\n'.format(city.title(), month.title(), day.title()))
        response = input('Is this correct? Enter the letter \'y\' for Yes or \'n\' for No: ').lower()

        if response == 'y' or response == 'n':
            break
        else:
            print('\nYour response was not one of the options.  Let\'s try again!\n')


    print(separator)

    return response == 'y'


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
    df = pd.read_csv(CITY_DATA[city],
                     header=0,
                     index_col=0)
    
    df = df.convert_dtypes()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = (df['Start Time'].dt.dayofweek + 1).astype('string')


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df



def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Arguments:
        df - Pandas DataFrame containing the selected city data, possibly filter by month and day of week
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nThe Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month under the condition that all months were chosen
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('The most popular month is: ', month_dictionary[str(popular_month)].title())

    # display the most common day of week under the condition that all days of the week were chosen
    if day == 'all':
        popular_day_of_week = df['day_of_week'].mode()[0]
        print('The most popular day of the week is: ', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour to start is: {}:00 (24-hr clock)'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print(separator)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combo_start_end'] = df['Start Station'] + ',' + df['End Station']
    popular_combo_start, popular_combo_end = df['combo_start_end'].mode()[0].split(',')
    print('The most popular combination of start and end stations consists in...')
    print('Start: {}    End: {}'.format(popular_combo_start, popular_combo_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(separator)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum().round()
    total_minutes = total_travel_time // 60
    remaining_tot_seconds = total_travel_time % 60
    print(f"The total bikeshare travel time was: {total_travel_time:,.0f} seconds ({total_minutes:,.0f} minutes, {remaining_tot_seconds:,.0f} seconds)")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_minutes = mean_travel_time // 60
    remaining_mean_seconds = mean_travel_time % 60
    print('The mean bikeshare travel time was: {} seconds ({} minutes, {} seconds)'.format(int(mean_travel_time), int(mean_minutes), int(remaining_mean_seconds)))

    # display percentage of trips under an hour
    total_num_trips = df['Trip Duration'].count()
    trips_under_hour = df.loc[df['Trip Duration'] < 3600, 'Trip Duration'].count()
    print(f"The percentage of trips under one hour was: {trips_under_hour/total_num_trips:.2%}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(separator)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas dataframe
        (str) city - name of the city to analyze
    """

    print('\nUser Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type     Counts')
    df_user_types = df['User Type'].value_counts()
    print(df_user_types)

    # Display statistics about gender and birth year only for Chicago and New York, not Washington
    if city != 'washington':
        # Display counts of gender
        print('\nGender     Counts')
        df_gender = df['Gender'].value_counts()
        print(df_gender)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest year of birth of users: ', int(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent year of birth of users: ', int(most_recent_birth_year))

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most common year of birth of users: ', int(most_common_birth_year))

    else:
        print('\nData and statistics concerning gender and birth year are not available for Washington DC.')

    time_diff = time.time() - start_time
    print(f"\nThis took {time_diff} seconds.")

    print(separator)


def raw_data_prompt(df):
    """
    Prompt user if they would like to see rows of raw data from the dataframe, 5 at a time.

    Args:
        df - Pandas dataframe
    """

    while True:
        print('\nWould you like to see 5 lines of raw data from the dataframe your selection created?')
        raw_data = input('Enter the letter \'y\' for Yes or \'n\' for No:  ').lower()
        i = 0
        if raw_data == 'y':
            print(df.iloc[i:i+5, :])
            print(separator)

            while True:
                raw_data = input('\nWould you like to see more raw data? Enter \'y\' for Yes or \'n\' for No:  ').lower()
                if raw_data == 'y':
                    i += 5
                    print('\n', df.iloc[i:i+5, :])
                    print(separator)
                else:
                    break
            break
        else:
            break

    print(separator)


def main():
    while True:
        ready = False
        while not ready:
            city, month, day = get_filters()
            ready = check_input(city, month, day)

        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_prompt(df)

        # Ask user if they would like to restart
        restart = input('\nWould you like to start over for a fresh analysis? Enter the letter \'y\' for Yes or \'n\' for No:  ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
