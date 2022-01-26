import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
import datetime
from pylab import *

def gdpData():
    gdpTimeStampValues = []
    gdpDataValues = []

    gdpAPIUrl = 'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=J4RQ2HAVH7OZNSRM'
    gdpDataFeedResponse = requests.get(gdpAPIUrl)
    gdpData = gdpDataFeedResponse.json()

    gdpJSONArray = gdpData["data"]

    for gdpJSONObject in gdpJSONArray:
        gdpTimeStampValues.append(gdpJSONObject["date"])

        gdpDataValues.append(float(gdpJSONObject["value"]))



    print(gdpTimeStampValues)
    print(gdpDataValues)
    
    xAxisCoordinates = numpy.array([ x for x in range(5) ])
    yAxisCoordinates = numpy.array(gdpDataValues[:5])

    bestFitLine1, bestFitLine2 = np.polyfit(xAxisCoordinates, yAxisCoordinates, 1)

    pythonPlot.scatter(xAxisCoordinates, yAxisCoordinates, color='red')

    pythonPlot.plot(xAxisCoordinates, bestFitLine1*xAxisCoordinates+bestFitLine2, color='green', linestyle ='--', linewidth = 3)

    pythonPlot.text(1, 17, 'y = ' + '{:.2f}'.format(bestFitLine2) + ' + {:.2f}'.format(bestFitLine1) + 'x', size=14)




dataFeedOptionInput = input ("This program shows the data containing the annual and quarterly Real GDP of US, Monthly interest rates of US, Annual Inflation rates of US and Monthly Unemployment data of US. Do you want to see it? 1 or 0: ")
    
if (int(dataFeedOptionInput) == 1):
    gdpData()
else:
  print("End Of Program")    
