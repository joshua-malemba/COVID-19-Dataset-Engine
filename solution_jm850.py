import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import warnings 
# question 1 and 2 are satisfactory

# add try exceptions 
def question1(link1, link2, link3):
    confirmed = pd.read_csv(link1)
    recovered = pd.read_csv(link2)
    deaths = pd.read_csv(link3)

    dataframes = [confirmed, recovered, deaths]
    for dataframe in dataframes: 
        first5 = dataframe.head(5)
        missing_values = first5.isnull().sum()
        print(first5.describe(), missing_values)

link1 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
link2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
link3 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
#question1(link1, link2, link3)


def question2a(dataframes):
    for dataframe in dataframes:
        # group each dataframe by country / region column
        grouped = dataframe.groupby(by=['Country/Region']).sum()
        # return dataframe in descending order (according to last column index
        # that denotes the most recent date ! )
        sorted_grouped_conf = grouped.sort_values(by=grouped.columns[-1], ascending=False)
        sorted_grouped_conf.head(10)
        print(sorted_grouped_conf)
        
confirmed = pd.read_csv(link1)
recovered = pd.read_csv(link2)
deaths = pd.read_csv(link3)

dataframes = [confirmed, recovered, deaths]
#question2a(dataframes)

def barplot(nb_countries):
    
    link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

    conf = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/\
    csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    data = pd.read_csv(link)
    grouped_deaths = data.groupby(by=['Country/Region']).sum()    
    sorted_grouped_deaths = grouped_deaths.sort_values(by=grouped_deaths.columns[-1], ascending=False)

    last_col = data.iloc[-1]
    last_day = last_col.index[-1]
    plt.figure(figsize=(12, 8))
    plt.title('Top 10 countries with highest deaths', fontsize=14)
    plt.barh(sorted_grouped_deaths[last_day].index[:nb_countries], sorted_grouped_deaths[last_day].head(nb_countries))
    plt.xlabel('Total deaths by '+last_day)
    plt.grid()
    plt.show()

#barplot(10)

def utility_function(URL, country):
    # this function is designed to identify the row of a given country
    # and return it's data in a neat format
    data = pd.read_csv(URL)
    
    info = data[data['Country/Region'].str.contains(country)]
    country_data = info.tail(1)
    
    return country_data

def utility_function_USA_Data():
    # USA Data is quite unique in style so i had to write
    # a specialized function on handling USA Data.
    # it's purpose is the same as the first utility function.
    
    US_link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    US_data = pd.read_csv(US_link)
    info = US_data.groupby(by=['Country_Region']).sum()

    US_data = info.tail(1)
    return US_data

def get_total_death_of(country):

    data = utility_function(link3, country)
    
    country_total = data.iloc[:, 4:].apply(sum, axis=0)
    country_total.index = pd.to_datetime(country_total.index)
    return country_total 

#print(get_total_death_of('Armenia'))

def line_plot_of_death_of(country, col):
    if country == 'United States':
        country_data = utility_function_USA_Data()
        country_total = country_data.iloc[:, 7:].apply(sum, axis=0)
    else:
        country_data = utility_function(link3, country)
        country_total = country_data.iloc[:, 4:].apply(sum, axis=0)
    
    country_total.index = pd.to_datetime(country_total.index)
    plt.figure(figsize=(12, 8))
    plt.title('Total deaths reported in ' + country + " over the last year", fontsize=14)
    plt.plot(country_total, col)        
    plt.ylabel('Country Deaths')
    plt.grid()
    plt.show()
#print(line_plot_of_death_of('United States', 'red'))

def line_plot_of_death_of_US_UK_France():

    UK_data = utility_function(link3, 'United Kingdom')
    France_data = utility_function(link3, 'France')
    US_data = utility_function_USA_Data()
        
    UK_Total = UK_data.iloc[:, 4:].apply(sum, axis=0)
    France_Total = France_data.iloc[:, 4:].apply(sum, axis=0)
    US_Total = US_data.iloc[:, 7:].apply(sum, axis=0)

    UK_Total.index = pd.to_datetime(UK_Total.index)
    France_Total.index = pd.to_datetime(France_Total.index)
    US_Total.index = pd.to_datetime(US_Total.index)

    countries = [UK_Total, US_Total, France_Total]
    
    plt.figure(figsize=(12, 8))
    plt.title('Total deaths reported in USA, UK, France', fontsize=14)
    for country in countries:
        plt.plot(country)      
    plt.ylabel('Deaths')
    plt.grid()
    plt.show()
print(line_plot_of_death_of_US_UK_France())


# get daily deaths WORKS ! 
def get_daily_deaths_of(country, death):
    # death is a dataframe
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    if country == 'United States':
        country_data = utility_function_USA_Data()
        deaths = country_data.iloc[:, 7:].apply(sum, axis=0)
        dates = pd.to_datetime(deaths.index)
        frame = {'Dates':dates, 'Deaths':deaths}
        df = pd.DataFrame(frame)
        df['Lag'] = df.Deaths.shift(1).fillna(0)
        df['Daily Deaths'] = df.Deaths - df.Lag
        return df[['Dates', 'Daily Deaths']]
    else: 
        df_country = death['Country/Region']==country
        deaths = death[df_country].iloc[:,4: ].apply(lambda x: x.sum())
        dates = pd.to_datetime(deaths.index)
        frame = {'Dates':dates, 'Deaths':deaths}
        df = pd.DataFrame(frame)
        df['Lag'] = df.Deaths.shift(1).fillna(0)
        df['Daily Deaths'] = df.Deaths - df.Lag
        return df[['Dates', 'Daily Deaths']]

US_data = utility_function_USA_Data()
country_data = utility_function(link3, 'Armenia')
print(get_daily_deaths_of('Armenia', country_data))
print(get_daily_deaths_of('United States', US_data))

def hist_daily_deaths_of(country):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    if country == 'United States':
        country_data = utility_function_USA_Data()
        daily = get_daily_deaths_of(country, country_data)
    else:
        country_data = utility_function(link3, country)
        daily = get_daily_deaths_of(country, country_data)

    plt.figure(figsize=(12, 8))
    plt.title('Histogram for daily ' + country + ' deaths', fontsize=14)
    plt.hist(daily['Daily Deaths'], bins=50)
    plt.ylabel('Daily Deaths')
    plt.grid()
    plt.show()
hist_daily_deaths_of('United States')

def hist_daily_deaths_of_india_brazil():

    India_data = utility_function(link3, 'India')
    Brazil_data = utility_function(link3, 'Brazil')
    
    ind_daily = get_daily_deaths_of('India', India_data)
    braz_daily = get_daily_deaths_of('Brazil', Brazil_data)
    
    dataframes = [ind_daily['Daily Deaths'], braz_daily['Daily Deaths']]
    
    plt.figure(figsize=(12, 8))
    plt.title('Histogram for india and brazil daily deaths ', fontsize=14)
    plt.hist(dataframes, bins=25)
    plt.ylabel('Daily Deaths')
    plt.grid()
    plt.show()
    
hist_daily_deaths_of_india_brazil()

def moving_averages(country, n):
    
    warnings.filterwarnings("ignore")

    if country == 'United States':
        country_data = utility_function_USA_Data()
        daily_deaths = get_daily_deaths_of(country, country_data)
    else:
        country_data = utility_function(link3, country)

        daily_deaths = get_daily_deaths_of(country, country_data)
    
    last_n_days = daily_deaths.tail(n)
    last_n_days['Moving Avg'] = last_n_days['Daily Deaths'].rolling(window=3).mean()
    return last_n_days

print(moving_averages('Armenia', 10))
print(moving_averages('United States', 10))


def plot_daily_deaths_and_avg_of(country):

    if country == 'United States':
        country_data = utility_function_USA_Data()
        daily_Deaths = get_daily_deaths_of(country, country_data)
    else:
        country_data = utility_function(link3, country)
    
        daily_Deaths = get_daily_deaths_of(country, country_data)
    
    AvgSeven = moving_averages(country, 7)
    
    dataframes = [daily_Deaths, AvgSeven]
    
    plt.figure(figsize=(12, 8))
    plt.title('Daily Deaths and 7 Day Average ', fontsize=14)
    for dataframe in dataframes:
        plt.plot(dataframe)
    plt.ylabel('Daily Deaths')
    plt.grid()
    plt.show()
    
plot_daily_deaths_and_avg_of('India')
plot_daily_deaths_and_avg_of('United Kingdom')
plot_daily_deaths_and_avg_of('United States')


