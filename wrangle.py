# Imports: 
import numpy as np
import pandas as pd

# environment:
import env
import os


#----------------------Acquire Functions-------------------------#
# get connection url:
def get_db_url(db, user=env.username, host=env.host, password=env.password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# acquire the data from sql: 
def acquire_logs(): 
    '''
    This function will request the curriculum logs data from sql and return a pandas df
    '''
    sql_query = '''
SELECT name, start_date, end_date, program_id, date, time, path, user_id, cohort_id, ip
FROM cohorts
LEFT JOIN logs
    on cohorts.id = logs.cohort_id'''
    df = pd.read_sql(sql_query, get_db_url('curriculum_logs'))
    return df

# create csv file based on data: 
def get_logs():
    '''
    This function will read in curriculum logs and write it into a csv file if a local file does not exist. 
    Returns a dataframe.
    '''
    if os.path.isfile('curriculum.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('curriculum.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = acquire_logs()
        
        # Write DataFrame to a csv file.
        df.to_csv('curriculum.csv')
        
    return df  

#--------------------Preperation Functions-----------------------#
# clean data without making a datetime index
def prep_logs_plain():
    '''
    This function will prepare the dataframe by: 
    - Remoing null values
    - Droping unnecessary columns
    - create a datetime that can be used for an index
    '''
    df = acquire_logs()
    # drop nulls
    df = df.dropna()
    # create datetime: 
    df['datetime'] = df['date'] + " " + df['time']
    # set the date time to a dataframe: 
    df.datetime = pd.to_datetime(df.datetime)
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    # drop columns: 
    df = df.drop(columns = ['date','time'])
    
    return df

#clean the data and make a datetime index: 
def prep_logs_time():
    '''
    This function will prepare the dataframe by: 
    - Remoing null values
    - Droping unnecessary columns
    - create a datetime that can be used for an index
    - make the index the datetime
    '''
    df = acquire_logs()
    # drop nulls
    df = df.dropna()
    # create datetime: 
    df['datetime'] = df['date'] + " " + df['time']
    # set the date time to a dataframe: 
    df.datetime = pd.to_datetime(df.datetime)
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    # drop columns: 
    df = df.drop(columns = ['date','time'])
    
    # set the index to datetime: 
    df = df.set_index(df.datetime)
    # create the weekday: 
    df['weekday'] = df.index.day_name()
    # want the month: 
    df['month'] = df.index.month_name()
    
    return df


#--------------------------------Acessory Functions---------------------#
# find the top lessons in a datafame
def top_lesson(df): 
    '''
    This function will specifically find the top lessons for a database:
    - It will first group by name and path and count the number of times they happen
    - It will exclude the / path
    - It will then sort them by name and count in descending order
    - It will select the top two lessons for each cohort and then reset the index
    ''' 
    return df[df['path'] != '/'].groupby(['name', 'path']).size().reset_index(name='count').sort_values(['count'], 
    ascending=[ False]).groupby('name').head(1).reset_index(drop=True)

              
#find the leat common lesson:
def least_lesson(df): 
    '''
    This function will specifically find the least common lessons for a database:
    - It will first group by name and path and count the number of times they happen
    - It will exclude the / path
    - It will then sort them by name and count in ascending order (least common first)
    - It will select the least common lesson for each cohort and then reset the index
    ''' 
    return df[df['path'] != '/'].groupby(['name', 'path']).size().reset_index(name='count').sort_values(['count'], 
    ascending=[True]).groupby('name').head(1).reset_index(drop=True)


#--------------Anomaly Functions--------#
def one_user_df_prep(df, user):
    '''
    This function returns a dataframe consisting of data for only a single defined user
    '''
    df = df[df.user_id == user]
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index(df.datetime)
    pages_one_user = df['path'].resample('d').count()
    return pages_one_user

def compute_pct_b(pages_one_user, span, weight, user):
    '''
    This function adds the %b of a bollinger band range for the page views of a single user's log activity
    '''
    # Calculate upper and lower bollinger band
    midband = pages_one_user.ewm(span=span).mean()
    stdev = pages_one_user.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    
    # Add upper and lower band values to dataframe
    bb = pd.concat([ub, lb], axis=1)
    
    # Combine all data into a single dataframe
    my_df = pd.concat([pages_one_user, midband, bb], axis=1)
    my_df.columns = ['pages_one_user', 'midband', 'ub', 'lb']
    
    # Calculate percent b and relevant user id to dataframe
    my_df['pct_b'] = (my_df['pages_one_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def compute_pct_b(pages_one_user, span, weight, user):
    '''
    This function adds the %b of a bollinger band range for the page views of a single user's log activity
    '''
    # Calculate upper and lower bollinger band
    midband = pages_one_user.ewm(span=span).mean()
    stdev = pages_one_user.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    
    # Add upper and lower band values to dataframe
    bb = pd.concat([ub, lb], axis=1)
    
    # Combine all data into a single dataframe
    my_df = pd.concat([pages_one_user, midband, bb], axis=1)
    my_df.columns = ['pages_one_user', 'midband', 'ub', 'lb']
    
    # Calculate percent b and relevant user id to dataframe
    my_df['pct_b'] = (my_df['pages_one_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def find_anomalies(df, user, span, weight, plot=False):
    '''
    This function returns the records where a user's daily activity exceeded the upper limit of a bollinger band range
    '''
    
    # Reduce dataframe to represent a single user
    pages_one_user = one_user_df_prep(df, user)
    
    # Add bollinger band data to dataframe
    my_df = compute_pct_b(pages_one_user, span, weight, user)
    
    # Plot data if requested (plot=True)
    if plot:
        plot_bands(my_df, user)
    
    # Return only records that sit outside of bollinger band upper limit
    return my_df[my_df.pct_b>1]