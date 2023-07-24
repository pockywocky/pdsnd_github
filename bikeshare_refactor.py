import sys
import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    
    The following try-except statement checks for errors in city's input
    """

    cities = ['chicago', 'new york city', 'washington']
    
    while True:
        city = input("Good day! Welcome to US bikeshare data service! Let's start with a city from the following list:\n(Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            break
        else:
            error_name = input("Oops, looks like your input wasn't one of the three cities! Would you like to try again? Type y or n: ").strip().lower()
            if error_name != "y":
                print("Thanks for checking us out! See you next time!")
                sys.exit()
            
    filtering_1 = input("Looks like it's {}! Would you like to filter by month, day or none at all? Type all for no filter: ".format(city)).strip().lower()  

    if filtering_1 == 'all':
        return city, 'all', 'all'
    
    elif filtering_1 == 'month':
        return city, input_month(city), 'all'
    
    elif filtering_1 == 'day':
        return city, 'all', input_day(city, 'all')
    
    else:
        return city, 'all', 'all' 

"""The following try-except statement checks for errors in month's input"""

def input_month(city):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    
    while True:
        month = input("We have information from January 2017 up to June 2017, please enter all or your desired month to proceed:\n(January, February, March, April, May, June): ").strip().lower()
        if month in months:
            print("You\'ve selected '{}' to proceed, we're digging through for you now!".format(month))
            return month
        else:
            error_month = input("Ooppss, either your month wasn't spelled in full, or you have entered something I don't understand! Would you like to try again? Type y or n: ").strip().lower()
            if error_month != "y":
                print("No problem! Check us out again next time!")
                sys.exit()
            
"""The following try-except statement checks for errors in day's input"""

def input_day(city, month):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    while True:
        day = input("Thanks! You can choose either all or enter a day of the week to proceed:\n(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").strip().lower()
        if day in days:
            print("You\'ve selected '{}' to proceed, we're digging through for you now!".format(day))
            return day
            
        else:
            error_day = input("Ooppss, either your day wasn't spelled in full, or you have entered something I don't understand! Would you like to try again? Type y or n: ").strip().lower()
            if error_day != "y":
                print("No problem! Check us out again next time!")
                sys.exit()
        
print('-' * 40)

CITY_DATA = { 'chicago': '/Users/danomano/Desktop/DataScience/RMIT project/Python/bikeshare-2/chicago.csv',
              'new york city': '/Users/danomano/Desktop/DataScience/RMIT project/Python/bikeshare-2/new_york_city.csv',
              'washington': '/Users/danomano/Desktop/DataScience/RMIT project/Python/bikeshare-2/washington.csv' }    
    
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
    print('Gathering your requested information! While it loads, remember to hydrate yourself daily! :-D ')
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month and month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        df = df[df['month'] == month]

    if day and day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df 


def topfive_info(df, city):

    """ 
    Load popular travel day and month information based on load_data. 
    
    Returns: 
        print information on what users may want to know
        Ability to restart program for a new filter
    """
    
    print('Loading...')
    print('Thanks for waiting! Here are some information we have gathered for you!')
    
    daymode = df['day_of_week'].mode()[0]
    print('\nCommon Travel Day:', daymode)
        
    monthmode = df['month'].mode()[0]
    print('\nCommon Travel Month:', monthmode)

    startendtimemode = df.groupby(['Start Time', 'End Time']).size().idxmax()
    print('\nMost Common Start and End Time:\n', startendtimemode)
    
    startendstation = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nMost users prefer this route to begin and end!:\n', startendstation)
   
    tripmax = df['Trip Duration'].max()
    print('\nThe longest trip ever took was (in secs):\n', tripmax)
    
    tripmin = df['Trip Duration'].min()
    print('\nAnd the shortest trip ever took was (in secs):\n', tripmin)
    
    if 'Birth Year' not in df.columns:
        print('\nPeople of this Birth Year uses the most bikeshare service!:')
        print('\n...ooppss... we don\'t have data for this city\'s Birth Year group')
    else:
        birthyearcount = df['Birth Year'].value_counts().idxmax()
        print('\nPeople of this Birth Year uses the most bikeshare service!:\n', birthyearcount)
        
    usertypecount = df['User Type'].value_counts()
    print('\nHere\'s a quick breakdown of our user types!:\n', usertypecount)

    if 'Gender' not in df.columns:
        print('\nAnd a quick breakdown of the gender count!:')
        print('\n...ooppss... we don\'t have data for this city\'s Gender group\n')
    else:
        gendercount = df['Gender'].value_counts()
        print('\nAnd a quick breakdown of the gender count!:\n', gendercount)
        
def startenddf(df):
    
    """To load next five rows of data from df"""

    startdf = 0
    enddf = 5

    continuefive = input("That's it! Would you like to see the next five rows? Type y or n: ")

    while continuefive == 'y':
        print(df[startdf:enddf])
        startdf += 5
        enddf += 5
        continuefive = input("Would you like to see the next five rows? Type y or n: ")
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        topfive_info(df, city)
        startenddf(df)

        restart = input('\nThat\'s it for this city! Would you like to do another filter? Type y or n: ')
        if restart != 'y':
            print('Okay! Thanks for using our service! See you again!')
            sys.exit()


if __name__ == "__main__":
	main()
