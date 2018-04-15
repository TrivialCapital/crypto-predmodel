# THIS IMPORTS THE LIBRARIES NECESSARY


from scipy.stats import norm
import numpy as np
import math
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from scipy.special import ndtri
import random 


# THIS GETS THE DATA - CHANGE FOR WHICH CRYPTO


df = web.DataReader('GOOG','yahoo', start='2015-01-01', end='2017-03-30')

df_returns = (df['Adj Close'].pct_change(1))*100
df_price = (df['Close'])


# FOLLOWING IS JUST PART OF CALCULATIONS (TAKES THE LN HERE)


def newVal():
	new = df_price.values
	kappa = []
	for i in range(len(new)):
		if i == 0:
			newVal = 0
		else:
			newVal = np.log(new[i]/new[i-1])
		kappa.append(newVal)
	return kappa


# TAKES THE LN FOR THE PREDICTVALUES() FUNCTION


def findLnData(data):
	novel = []
	for i in range(len(data)):
		if i == 0:
			a = 0
		else:
			a = np.log(data[i]/data[i-1])
		novel.append(a)
	std = np.std(novel)
	avg = np.average(novel)
	var = np.var(novel)
	return std, avg, var


# THIS FINDS ONLY TOMORROW'S PREDICTED PRICE (CODE GETS BETTER LATER)


def traditional(amountOfDays = None):

	dua = newVal()

	if(amountOfDays == None):
		amountOfDays = len(df_price)

	Data = df_price[-amountOfDays:]
	Data2 = dua[-amountOfDays:]
	stdev = np.std(Data2)
	average = np.average(Data2)
	variance = np.var(Data2)
	drift = average - (variance/2)
	latest = Data[len(Data)-1]

	answer = latest * math.exp(drift+stdev*ndtri(random.random()))

	print(Data2)
	print("")
	print("answer: "+ str(answer))


# THIS OUTPUTS PREDICTED VALUES FROM DAYS ALREADY PAST, THIS WAS MEANT
# TO MAKE IT EASIER TO SEE HOW ACCURATE THIS ALGORITHM IS (THIS FUNCTION 
# FINDS THE NOISE BASICALLY). I ADDED IT SO THAT YOU CAN THINK ABOUT FUTURE
# IMPROVEMENTS IF YOU WANT TO LOL


def group(interval = None):
	
	if(interval == None):
		interval = 100

	predict = pd.Series(index = df_price.index, name = "predictVal")
	
	dua = newVal()

	for i in range(0, len(df_price)-interval):
		if(i == 0):
			Data = df_price[-interval:]
			Data2 = dua[-interval:]
		else:
			Data = df_price[-(interval+i):-i]
			Data2 = dua[-(interval+i):-i]

		stdev = np.std(Data2)
		average = np.average(Data2)
		variance = np.var(Data2)
		drift = average - (variance/2)
		latest = Data[len(Data)-1]

		answer = latest * math.exp(drift+stdev*ndtri(random.random()))

		predict[-i-1] = answer

	print(predict)

# THE FOLLOWING IS THE IMPORTANT PART OF THE ALGORITHM, IT TAKES IN HOW MANY DAYS
# INTO THE FUTURE YOU WANT TO PREDICT PRICES FOR AND ALSO AN INTERVAL OF HOW 
# MANY PAST DAYS' WORTH OF DATA YOU WANT TO USE (LEAVE THAT PART BLANK TO JUST USE ALL 
# THE DATA). IT UPDATES ITSELF BASED ON PREVIOUS PREDICTIONS AS WELL, SO I FEEL
# THAT GIVEN THE ALGORITHM YOU SENT ME, THIS IS THE CLOSEST (ALGORITHMICALLY)
# THAT YOU CAN USE TO PREDICT FUTURE PRICES

def predictFuture(numberOfDays, interval = None):
	tempData = [] 
	predValues = []

	for i in range(len(df_price)):
		tempData.append(df_price.values[i])

	if interval == None:
		interval = len(tempData)

	for i in range(numberOfDays):
		tData = tempData[-interval:]

		print(tData)

		std, avg, var = findLnData(tData)
		drift = avg - (var/2)
		lastVal = tData[len(tData)-1]

		print(lastVal)

		predVal = lastVal * math.exp(drift+std*ndtri(random.random()))
		tempData.append(predVal)
		predValues.append(predVal)

	return tempData, predValues

# THIS ACTUALLY PRINTS OUT THE PREDICTIONS

futureDays = 100
tempDat, predV = predictFuture(numberOfDays = futureDays, interval = 100)
print("")
print("the next " + str(futureDays) + " days worth of predictions is: ")
print(predV)

# THIS MAKES THE GRAPH

def makeGraph(predictedList):
	xAxis = []
	for i in range(len(predictedList)):
		xAxis.append(i+1)
	plt.plot(xAxis, predictedList)
	plt.show()

# THIS PRINTS OUT THE GRAPH

makeGraph(predV)
