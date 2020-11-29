#very specific pre-processing program intended
#to clean up a covid dataset

import csv
import os
import re
import sys
import pandas as pd 


if __name__ == '__main__':

	#Takes in csv file
	with open('covidData.csv') as f:
		reader = csv.reader(f)
		rows = list(f)

		#Takes only relevant rows (naively may I add)
		dates = rows[0]
		elPaso = rows[2768]
		dates = dates.split(',') #Convert from str to list
		elPaso = elPaso.split(',')


		#primitive data deletion
		#v1: keeps 1 value at top to confirm date
		#del dates[0:5]
		#del elPaso[0:5]
		#del dates[1:7]
		#del elPaso[1:8]

		#v2: removes city info, just dates/infections
		del dates[0:11]
		del elPaso[0:13]

		#removes everything up to march
		del dates[0:39]
		del elPaso[0:39]

		#removes everything from march to july
		del dates[31:122]
		del elPaso[31:122]

		#removes everything else
		del dates[62:]
		del elPaso[62:]

		#print(dates) #DEBUG
		#print(elPaso)

		#split the data into 2 different structs (if necessary)
		marchDates = dates[0:31]
		marchInfections = elPaso[0:31]
		julyDates = dates[31:]
		julyInfections = elPaso[31:]

	
	#Combines lists and turns them to a pandas dataFrame that has days on one row and the corresponding infections on the next row
	marchList = list(zip(marchDates,marchInfections))
	julyList = list(zip(julyDates,julyInfections))

	#Some pandas dataframe formatting
	marchDF = pd.DataFrame(marchList)
	julyDF = pd.DataFrame(julyList)
	marchDF.rename(columns={0:'Date', 1:'Infections'}, inplace=True)
	julyDF.rename(columns={0:'Date', 1:'Infections'}, inplace=True)

	#print(marchDF) #DEBUG

	#store lists into their respective CSV files.
	marchDF.to_csv('marchInfections.csv', sep = ',', encoding = 'cp1251', index = False)
	#marchDF.to_csv('marchInfections.csv')
	julyDF.to_csv('julyInfections.csv', sep = ',', encoding = 'cp1251', index = False)

	#print(marchDF) #DEBUG

	#combine lists into key:value dict (key is date, value is num infections)
	#Not sure if this will ever be needed but leaving it here anyways
	marchDict = {} 
	julyDict = {}
	for key in marchDates: 
		for value in marchInfections: 
			marchDict[key] = value 
			marchInfections.remove(value) 
			break 
	for key in julyDates: 
		for value in julyInfections: 
			julyDict[key] = value 
			julyInfections.remove(value) 
			break 

	#print(infectionsPerDay) #DEBUG
	#print(dates)
	#print(elPaso)