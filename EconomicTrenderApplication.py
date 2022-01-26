import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
import datetime
from pylab import *


def printStockDataGraphsAndCSVFile(stockDataType):

    stockTimeStampValues = []
    stockOpenPriceValues = []
    stockHighPriceValues = []
    stockLowPriceValues = []
    stockClosePriceValues = []
    stockVolumeValues = []

    stockTimeSeriesAPIUrl = ""
    
    if (stockDataType == "intraday"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "daily"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "weekly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "monthly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=J4RQ2HAVH7OZNSRM'
        
        
    stockDataFeedResponse = requests.get(stockTimeSeriesAPIUrl)
    stockData = stockDataFeedResponse.json()

    timeSeriesJSONArray = stockData[list(stockData.keys())[1]]
    for timeSeriesKey in timeSeriesJSONArray:
        timeSeriesJSONObject = timeSeriesJSONArray[timeSeriesKey]

        stockTimeStampValues.append(timeSeriesKey)
        
        stockOpenPriceValues.append(timeSeriesJSONObject["1. open"])

        stockHighPriceValues.append(timeSeriesJSONObject["2. high"])

        stockLowPriceValues.append(timeSeriesJSONObject["3. low"])

        stockClosePriceValues.append(timeSeriesJSONObject["4. close"])

        stockVolumeValues.append(timeSeriesJSONObject["5. volume"])

    mostRecentStockTimeStampValues = stockTimeStampValues[:5]

    mostRecentStockOpenPriceValues = stockOpenPriceValues[:5]

    mostRecentStockHighPriceValues = stockHighPriceValues[:5]

    mostRecentStockLowPriceValues = stockLowPriceValues[:5]

    mostRecentStockClosePriceValues = stockClosePriceValues[:5]

    mostRecentStockVolumeValues = stockVolumeValues[:5]
        
    pandasDataFrame = pandas.DataFrame(dict(graph=mostRecentStockTimeStampValues,
                           openingPrice=mostRecentStockOpenPriceValues,
                                            highPrice=mostRecentStockHighPriceValues,
                                            lowPrice=mostRecentStockLowPriceValues,
                                            closingPrice=mostRecentStockClosePriceValues,
                                            volume=mostRecentStockVolumeValues))

    XAxisCoordinateLocations = numpy.arange(5)
    width = 0.2

    figure, axis = pythonPlot.subplots()
    axis.barh(XAxisCoordinateLocations, pandasDataFrame.openingPrice, width, color='red', label='Opening Price')
    axis.barh(XAxisCoordinateLocations - 0.4, pandasDataFrame.highPrice, width, color='green', label='High Price')
    axis.barh(XAxisCoordinateLocations - 0.2, pandasDataFrame.lowPrice, width, color='blue', label='Low Price')
    axis.barh(XAxisCoordinateLocations + 0.2, pandasDataFrame.closingPrice, width, color='yellow', label='Closing Price')
    axis.barh(XAxisCoordinateLocations + 0.4, pandasDataFrame.volume, width, color='purple', label='Volume')

    axis.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph, ylim=[2*width - 1, len(pandasDataFrame)])
    axis.legend()

    if (stockDataType == "intraday"):
        pythonPlot.title('Stock Trends Intraday Horizontal Bar Chart')
    elif (stockDataType == "daily"):
        pythonPlot.title('Stock Trends Daily Horizontal Bar Chart')
    elif (stockDataType == "weekly"):
        pythonPlot.title('Stock Trends Weekly Horizontal Bar Chart')
    elif (stockDataType == "monthly"):
        pythonPlot.title('Stock Trends Monthly Horizontal Bar Chart')


    pythonPlot.show()

    
    stockTrendsCSVHeader = ['TimeStamp','Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']

    currentTime = datetime.datetime.now()

    fileNameToSave = ''
    if (stockDataType == "intraday"):
        fileNameToSave = 'stockTrends_Intraday_'+str(currentTime)+'.csv'
    elif (stockDataType == "daily"):
        fileNameToSave = 'stockTrends_Daily_'+str(currentTime)+'.csv'
    elif (stockDataType == "weekly"):
        fileNameToSave = 'stockTrends_Weekly_'+str(currentTime)+'.csv'
    elif (stockDataType == "monthly"):
        fileNameToSave = 'stockTrends_Monthly_'+str(currentTime)+'.csv'
    
        

    with open(fileNameToSave, 'w', encoding="utf-8") as stockTrendsCSVFile:
        stockCSVWriter = csv.writer(stockTrendsCSVFile, delimiter='\t')

        stockCSVWriter.writerow(stockTrendsCSVHeader)

        for stockItem in zip(stockTimeStampValues,stockOpenPriceValues,stockHighPriceValues,stockLowPriceValues,stockClosePriceValues,stockVolumeValues):
            stockCSVWriter.writerow(stockItem)


    
    boxPlotFigure, axisCoordinates = pythonPlot.subplots()
    
    pandasDataFrame = pandas.DataFrame({
                                        'Open Price': list(map(float, stockOpenPriceValues)),
                        'High Price': list(map(float, stockHighPriceValues)),
                        'Low Price': list(map(float, stockLowPriceValues)),
                        'Close Price': list(map(float, stockClosePriceValues)),
                        'Volume': list(map(float, stockVolumeValues))})

    axisCoordinates = pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume'], figsize=(15,5), grid=True)

    if (stockDataType == "intraday"):
        axisCoordinates.set_title('Stock Trends Intraday Box Plot')
    elif (stockDataType == "daily"):
        axisCoordinates.set_title('Stock Trends Daily Box Plot')
    elif (stockDataType == "weekly"):
        axisCoordinates.set_title('Stock Trends Weekly Box Plot')
    elif (stockDataType == "monthly"):
        axisCoordinates.set_title('Stock Trends Monthly Box Plot')

    pythonPlot.show()    
    
  
dataFeedOptionInput = input ("Welcome to Economic Trender application! We will display data for the " +
             "following 3 categories of data: Option 1 - Stock Time Series, " +
             "Option 2 - Foreign Exchange Rate, Option 3 - Cryptocurrencies. " +
             "Please enter a number between 1-3 to choose an option from the 3 categories above: ")
    
if (int(dataFeedOptionInput) == 1):
    printStockDataGraphsAndCSVFile("intraday")
    printStockDataGraphsAndCSVFile("daily")
    printStockDataGraphsAndCSVFile("weekly")
    printStockDataGraphsAndCSVFile("monthly")
    
elif (int(dataFeedOptionInput) == 2):
  print("2")
else:
  print("3")


