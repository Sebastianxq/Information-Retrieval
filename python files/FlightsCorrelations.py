import pandas as pd
from scipy import stats

def reader1(filename):
    tempfile = open(filename, 'r', encoding="utf-8")
    lines = tempfile.readlines()

    # Initializes dataframe to store faculty information
    flights = pd.DataFrame(columns=['date', 'city'])
    flights.set_index('date')

    for line in lines:
        data = line.split(', ')
        if data[7] == '0.00':
            date = data[0].strip()
            city = data[4].strip()

            flight = pd.Series([date, city],
                                index=flights.columns)
            flights = flights.append(flight, ignore_index=True)

    return flights

def reader2(filename):
    tempfile = open(filename, 'r', encoding="utf-8")
    lines = tempfile.readlines()

    covid_ep = []
    # Gets El Paso COVID data
    templine1 = lines[0].split(',')
    templine2 = lines[2768].split(',') # El Paso's COVID time series
    covid_ep.append(templine1[11:])
    covid_ep.append(list(map(int, templine2[13:])))

    for i in range(len(covid_ep[0])):
        if i > 0:
            covid_ep[1][i] -= covid_ep[1][i-1]

    # Truncate series to include only data for March and July
    short_covid_ep = []
    for i, day in enumerate(covid_ep[0]):
        if day == '3/1/20' or day == '7/1/20':
            # Get data with 6 days delay to account for incubation period
            short_covid_ep += covid_ep[1][i+6: i+37]



    return short_covid_ep

def correlate(all_flights, covid_ep):
    # Gets daily total number of incoming flights number
    daily_flights_df = all_flights.groupby(['date']).size().reset_index(name='flights')
    daily_flights = list(daily_flights_df['flights'])

    covid_cities = []
    # Gets daily number of incoming filghts per city
    cities = list(set(all_flights['city']))
    temp_df = all_flights.groupby(['date', 'city']).size().reset_index(name='flights')

    writer = open('flight_correlations.txt', 'w+')

    # Store all dates for March and July
    tempdates = list(temp_df[temp_df['city'] == 'Houston']['date'])

    corr_city = {}
    for city in cities:
        covid_city_df = temp_df[temp_df['city'] == city]

        # Impute 0s in missing values for flight data
        covid_city = [0] * 62
        for i, date in enumerate(tempdates):
            if date in list(covid_city_df['date']):
                covid_city[i] = int(covid_city_df[covid_city_df['date'] == date]['flights'])

        corr_city[city] = stats.pearsonr(covid_ep, covid_city)[0]
        print(city, corr_city[city])

    sorted_corr_city = {name: corr_city[name] for name in
                        sorted(corr_city, key=corr_city.get, reverse=True)}


    for city, corr in sorted_corr_city.items():
        writer.write(city + "   " + str(corr) + '\n')


    # Calculates correlation between total incoming flights to EP and COVID cases
    corr_total = stats.pearsonr(covid_ep, daily_flights)[0]

    writer.write('TOTAL DAILY FLIGHTS   ' + str(corr_total))

    return corr_city, corr_total



# Gets flight data from csv file
flights1 = reader1('elp_flights_datasaset1_march.txt')
flights2 = reader1('elp_flights_datasaset1_july.txt')
all_flights = pd.concat([flights1, flights2])

# Gets COVID data from csv file
covid_ep = reader2('COVIDdataset.txt')

correlations = correlate(all_flights, covid_ep)







