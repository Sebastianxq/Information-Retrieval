from scipy import spatial
from scipy import stats
import csv

def reader(filename):
    tempfile = open(filename, 'r', encoding="utf-8")
    lines = tempfile.readlines()
    covid_cities = {}

    for i, line in enumerate(lines):
        templine = line.split(',')

        # Store El Paso's list of cases
        if i == 2768:
            # Parse string values to integer values for COVID cases
            covid_ep = list(map(int, templine[13:]))

        # Store the rest of US cities' cases (exclude heaader line 1)
        elif i != 0:
            city_name = templine[5] + " - " + templine[6]
            # Parse string values to integer values for COVID cases
            covid_cities[city_name] = list(map(int, templine[13:]))

    for i in range(len(covid_ep)):
        if i > 0:
            covid_ep[i] -= covid_ep[i-1]

    for name, cases in covid_cities.items():
        for i in range(len(cases)):
            if i > 0:
                cases[i] -= cases[i-1]


    return [covid_ep, covid_cities]


def cos_similarity(covid_ep, covid_cities):
    similarities = {}
    correlations= {}

    # Iterate through all cities
    for name, values in covid_cities.items():

        # Fill out smaller list of cases (El Paso) with 0s to make vectors have the same length
        if len(covid_ep) < len(values):
            for i in range(len(values) - len(covid_ep)):
                covid_ep.append(0)

        # Fill out smaller list of cases (Other city) with 0s to make vectors have the same length
        if len(covid_ep) > len(values):
            for i in range(len(covid_ep) - len(values)):
                values.append(0)

        # Calculate cosine similarity
        similarity = 1 - spatial.distance.cosine(covid_ep, values)
        similarities[name] = similarity

        #Calculate Pearon correlation
        correlation = stats.pearsonr(covid_ep, values)[0]
        correlations[name] = correlation

        print('Computing similarity for: ', name)

    # Sort cosine similarities
    sorted_similarities = {name: similarities[name] for name in
                           sorted(similarities, key = similarities.get, reverse=True)}

    # Sort cosine correlations
    sorted_correlations = {name: correlations[name] for name in
                           sorted(correlations, key=correlations.get, reverse=True)}

    # Store contents in a csv file
    with open('cosine_sims.csv', 'w+', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for name, sim in sorted_similarities.items():
            writer.writerow([name, sim])

    with open('correlations_covid.csv', 'w+', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for name, corr in sorted_correlations.items():
            writer.writerow([name, corr])




    return sorted_similarities, sorted_correlations



cases = reader('COVIDdataset.txt')
# El Paso COVID time series in a list
el_paso = cases[0]

# All US cities COVID time seires in a dictionary
other_cities = cases[1]

# Computes cosine similarity and correlation between EP's time series
# and every other city in the US
metrics = cos_similarity(el_paso, other_cities)

# Stores cosine similarities in a dictionary
similarities = metrics[1]

# Stores correlations in a dictionary
correlations = metrics[0]





