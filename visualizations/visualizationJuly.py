#!/usr/bin/python3

import csv
import numpy as np
from matplotlib import pyplot as plt

with open("./Cleaned COVID Dataset/julyInfections.csv", mode="r") as file:

    # reading the CSV file
    csvFile = csv.reader(file)
    plt.title("July Infections")
    plt.xlabel("Month: July")
    plt.ylabel("Infection Numbers")

    # displaying the contents of the CSV file
    x = []
    y = []
    for lines in csvFile:
        if lines[0] != "Date" or lines[1] != "Infections":
            x.append(lines[0].split("/")[1])  # Dates
            y.append(int(lines[1]))  # Infection Numbers
    plt.plot(x, y)
plt.show()
