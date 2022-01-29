import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
from pylab import *


def printStockDataGraphsAndCSVFile(stockDataType, equityNameSymbolPrompt):

    stockTimeStampValues = []
    stockOpenPriceValues = []
    stockHighPriceValues = []
    stockLowPriceValues = []
    stockClosePriceValues = []
    stockVolumeValues = []

    stockTimeSeriesAPIUrl = ""
    
    if (stockDataType == "intraday"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+equityNameSymbolPrompt+'&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "daily"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+equityNameSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "weekly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+equityNameSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "monthly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+equityNameSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
        
        
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
    margin = 0.03
    numberItems=5
    width = (1-(margin*numberItems))/numberItems

    figure, axis = pythonPlot.subplots()
    axis.barh(XAxisCoordinateLocations, pandasDataFrame.openingPrice, width, color='red', label='Opening Price', align='center')
    axis.barh(XAxisCoordinateLocations - width, pandasDataFrame.highPrice, width, color='green', label='High Price',align='center')
    axis.barh(XAxisCoordinateLocations - width*2, pandasDataFrame.lowPrice, width, color='blue', label='Low Price',align='center')
    axis.barh(XAxisCoordinateLocations + width*2, pandasDataFrame.closingPrice, width, color='yellow', label='Closing Price',align='center')
    axis.barh(XAxisCoordinateLocations + width, pandasDataFrame.volume, width, color='purple', label='Volume',align='center')

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

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
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

                for stockItem in zip(stockTimeStampValues,
                                     stockOpenPriceValues,
                                     stockHighPriceValues,
                                     stockLowPriceValues,
                                     stockClosePriceValues,
                                     stockVolumeValues):
                    stockCSVWriter.writerow(stockItem)
            
                print("All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")        
        except:
            print("An exception occurred")

def printCryptoDataGraphsAndCSVFile(cryptoDataType, equityNameSymbolPrompt, exchangeMarketPrompt):

    cryptoTimeStampValues = []
    cryptoOpenPriceValues = []
    cryptoHighPriceValues = []
    cryptoLowPriceValues = []
    cryptoClosePriceValues = []
    cryptoVolumeValues = []

    cryptoTimeSeriesAPIUrl = ""
    
    if (cryptoDataType == "intraday"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol='+equityNameSymbolPrompt+'&market='+exchangeMarketPrompt+'&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "daily"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+equityNameSymbolPrompt+'&market='+exchangeMarketPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "weekly"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol='+equityNameSymbolPrompt+'&market='+exchangeMarketPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "monthly"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol='+equityNameSymbolPrompt+'&market='+exchangeMarketPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
           
    cryptoDataFeedResponse = requests.get(cryptoTimeSeriesAPIUrl)
    cryptoData = cryptoDataFeedResponse.json()

    timeSeriesJSONArray = cryptoData[list(cryptoData.keys())[1]]
    for timeSeriesKey in timeSeriesJSONArray:
        timeSeriesJSONObject = timeSeriesJSONArray[timeSeriesKey]

        cryptoTimeStampValues.append(timeSeriesKey)
        
        cryptoOpenPriceValues.append(timeSeriesJSONObject["1. open"])

        cryptoHighPriceValues.append(timeSeriesJSONObject["2. high"])

        cryptoLowPriceValues.append(timeSeriesJSONObject["3. low"])

        cryptoClosePriceValues.append(timeSeriesJSONObject["4. close"])

        cryptoVolumeValues.append(timeSeriesJSONObject["5. volume"])

    mostRecentCryptoTimeStampValues = cryptoTimeStampValues[:5]

    mostRecentCryptoOpenPriceValues = cryptoOpenPriceValues[:5]

    mostRecentCryptoHighPriceValues = cryptoHighPriceValues[:5]

    mostRecentCryptoLowPriceValues = cryptoLowPriceValues[:5]

    mostRecentCryptoClosePriceValues = cryptoClosePriceValues[:5]

    mostRecentCryptoVolumeValues = cryptoVolumeValues[:5]
        
    pandasDataFrame = pandas.DataFrame(dict(graph=mostRecentCryptoTimeStampValues,
                           openingPrice=mostRecentCryptoOpenPriceValues,
                                            highPrice=mostRecentCryptoHighPriceValues,
                                            lowPrice=mostRecentCryptoLowPriceValues,
                                            closingPrice=mostRecentCryptoClosePriceValues,
                                            volume=mostRecentCryptoVolumeValues))

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

    if (cryptoDataType == "intraday"):
        pythonPlot.title('Crypto Trends Intraday Horizontal Bar Chart')
    elif (cryptoDataType == "daily"):
        pythonPlot.title('Crypto Trends Daily Horizontal Bar Chart')
    elif (cryptoDataType == "weekly"):
        pythonPlot.title('Crypto Trends Weekly Horizontal Bar Chart')
    elif (cryptoDataType == "monthly"):
        pythonPlot.title('Crypto Trends Monthly Horizontal Bar Chart')


    pythonPlot.show()
        
    boxPlotFigure, axisCoordinates = pythonPlot.subplots()
    
    pandasDataFrame = pandas.DataFrame({
                                        'Open Price': list(map(float, cryptoOpenPriceValues)),
                        'High Price': list(map(float, cryptoHighPriceValues)),
                        'Low Price': list(map(float, cryptoLowPriceValues)),
                        'Close Price': list(map(float, cryptoClosePriceValues)),
                        'Volume': list(map(float, cryptoVolumeValues))})

    axisCoordinates = pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price', 'Volume'], figsize=(15,5), grid=True)

    if (cryptoDataType == "intraday"):
        axisCoordinates.set_title('Crypto Trends Intraday Box Plot')
    elif (cryptoDataType == "daily"):
        axisCoordinates.set_title('Crypto Trends Daily Box Plot')
    elif (cryptoDataType == "weekly"):
        axisCoordinates.set_title('Crypto Trends Weekly Box Plot')
    elif (cryptoDataType == "monthly"):
        axisCoordinates.set_title('Crypto Trends Monthly Box Plot')

    pythonPlot.show()    

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            stockTrendsCSVHeader = ['TimeStamp','Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (cryptoDataType == "intraday"):
                fileNameToSave = 'cryptoTrends_Intraday_'+str(currentTime)+'.csv'
            elif (cryptoDataType == "daily"):
                fileNameToSave = 'cryptoTrends_Daily_'+str(currentTime)+'.csv'
            elif (cryptoDataType == "weekly"):
                fileNameToSave = 'cryptoTrends_Weekly_'+str(currentTime)+'.csv'
            elif (cryptoDataType == "monthly"):
                fileNameToSave = 'cryptoTrends_Monthly_'+str(currentTime)+'.csv'
    
            with open(fileNameToSave, 'w', encoding="utf-8") as cryptoTrendsCSVFile:
                cryptoCSVWriter = csv.writer(cryptoTrendsCSVFile, delimiter='\t')

                cryptoCSVWriter.writerow(cryptoTrendsCSVHeader)

                for cryptoItem in zip(cryptoTimeStampValues,
                                     cryptoOpenPriceValues,
                                     cryptoHighPriceValues,
                                     cryptoLowPriceValues,
                                     cryptoClosePriceValues,
                                     cryptoVolumeValues):
                    cryptoCSVWriter.writerow(cryptoItem)
            
                print("All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")        
        except:
            print("An exception occurred")


def printForexGraphsAndCSVFile(forexDataType, fromSymbolPrompt, toSymbolPrompt):
    
    forexTimeStampValues = []
    forexOpenPriceValues = []
    forexHighPriceValues = []
    forexLowPriceValues = []
    forexClosePriceValues = []

    forexTimeSeriesAPIUrl = ""
    
    if (forexDataType == "intraday"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol='+fromSymbolPrompt+'&to_symbol='+toSymbolPrompt+'&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "daily"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+fromSymbolPrompt+'&to_symbol='+toSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "weekly"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol='+fromSymbolPrompt+'&to_symbol='+toSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "monthly"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol='+fromSymbolPrompt+'&to_symbol='+toSymbolPrompt+'&apikey=J4RQ2HAVH7OZNSRM'
           
    forexDataFeedResponse = requests.get(forexTimeSeriesAPIUrl)
    forexData = forexDataFeedResponse.json()

    timeSeriesJSONArray = forexData[list(forexData.keys())[1]]
    for timeSeriesKey in timeSeriesJSONArray:
        timeSeriesJSONObject = timeSeriesJSONArray[timeSeriesKey]

        forexTimeStampValues.append(timeSeriesKey)
        
        forexOpenPriceValues.append(timeSeriesJSONObject["1. open"])

        forexHighPriceValues.append(timeSeriesJSONObject["2. high"])

        forexLowPriceValues.append(timeSeriesJSONObject["3. low"])

        forexClosePriceValues.append(timeSeriesJSONObject["4. close"])

    mostRecentForexTimeStampValues = forexTimeStampValues[:5]

    mostRecentForexOpenPriceValues = forexOpenPriceValues[:5]

    mostRecentForexHighPriceValues = forexHighPriceValues[:5]

    mostRecentForexLowPriceValues = forexLowPriceValues[:5]

    mostRecentForexClosePriceValues = forexClosePriceValues[:5]
        
    pandasDataFrame = pandas.DataFrame(dict(graph=mostRecentForexTimeStampValues,
                           openingPrice=mostRecentForexOpenPriceValues,
                                            highPrice=mostRecentForexHighPriceValues,
                                            lowPrice=mostRecentForexLowPriceValues,
                                            closingPrice=mostRecentForexClosePriceValues))

    XAxisCoordinateLocations = numpy.arange(5)
    width = 0.2

    figure, axis = pythonPlot.subplots()
    axis.barh(XAxisCoordinateLocations, pandasDataFrame.openingPrice, width, color='red', label='Opening Price')
    axis.barh(XAxisCoordinateLocations - 0.4, pandasDataFrame.highPrice, width, color='green', label='High Price')
    axis.barh(XAxisCoordinateLocations - 0.2, pandasDataFrame.lowPrice, width, color='blue', label='Low Price')
    axis.barh(XAxisCoordinateLocations + 0.2, pandasDataFrame.closingPrice, width, color='yellow', label='Closing Price')

    axis.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph, ylim=[2*width - 1, len(pandasDataFrame)])
    axis.legend()

    if (forexDataType == "intraday"):
        pythonPlot.title('Forex Trends Intraday Horizontal Bar Chart')
    elif (forexDataType == "daily"):
        pythonPlot.title('Forex Trends Daily Horizontal Bar Chart')
    elif (forexDataType == "weekly"):
        pythonPlot.title('Forex Trends Weekly Horizontal Bar Chart')
    elif (forexDataType == "monthly"):
        pythonPlot.title('Forex Trends Monthly Horizontal Bar Chart')


    pythonPlot.show()
        
    boxPlotFigure, axisCoordinates = pythonPlot.subplots()
    
    pandasDataFrame = pandas.DataFrame({
                                        'Open Price': list(map(float, forexOpenPriceValues)),
                        'High Price': list(map(float, forexHighPriceValues)),
                        'Low Price': list(map(float, forexLowPriceValues)),
                        'Close Price': list(map(float, forexClosePriceValues))})

    axisCoordinates = pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'], figsize=(15,5), grid=True)

    if (forexDataType == "intraday"):
        axisCoordinates.set_title('Forex Trends Intraday Box Plot')
    elif (forexDataType == "daily"):
        axisCoordinates.set_title('Forex Trends Daily Box Plot')
    elif (forexDataType == "weekly"):
        axisCoordinates.set_title('Forex Trends Weekly Box Plot')
    elif (forexDataType == "monthly"):
        axisCoordinates.set_title('Forex Trends Monthly Box Plot')

    pythonPlot.show()    

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            forexTrendsCSVHeader = ['TimeStamp','Opening Price', 'High Price', 'Low Price', 'Closing Price']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (forexDataType == "intraday"):
                fileNameToSave = 'forexTrends_Intraday_'+str(currentTime)+'.csv'
            elif (forexDataType == "daily"):
                fileNameToSave = 'forexTrends_Daily_'+str(currentTime)+'.csv'
            elif (forexDataType == "weekly"):
                fileNameToSave = 'forexTrends_Weekly_'+str(currentTime)+'.csv'
            elif (forexDataType == "monthly"):
                fileNameToSave = 'forexTrends_Monthly_'+str(currentTime)+'.csv'
    
            with open(fileNameToSave, 'w', encoding="utf-8") as forexTrendsCSVFile:
                forexCSVWriter = csv.writer(forexTrendsCSVFile, delimiter='\t')

                forexCSVWriter.writerow(forexTrendsCSVHeader)

                for forexItem in zip(forexTimeStampValues,
                                     forexOpenPriceValues,
                                     forexHighPriceValues,
                                     forexLowPriceValues,
                                     forexClosePriceValues):
                    forexCSVWriter.writerow(forexItem)
            
                print("All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")        
        except:
            print("An exception occurred")
    
while (True):
    dataFeedOptionInput = input ("\nWelcome to Economic Trender application! We will display data for the " +
             "following 3 categories of data: Option 1 - Stock Time Series, " +
             "Option 2 - Foreign Exchange Rate, Option 3 - Cryptocurrencies. " +
             "Please enter a number between 1-3 to choose an option from the 3 categories above or press 0 to end the program: ")
    
    if (int(dataFeedOptionInput) == 1):
        equityNameSymbolPrompt = input("Please enter the Stock symbol of the equity you want to see information for: ")

        typeOfData = input("Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printStockDataGraphsAndCSVFile("intraday", equityNameSymbolPrompt)
        elif (typeOfData == "d"):
            printStockDataGraphsAndCSVFile("daily", equityNameSymbolPrompt)
        elif (typeOfData == "w"):
            printStockDataGraphsAndCSVFile("weekly", equityNameSymbolPrompt)
        elif (typeOfData == "m"):
            printStockDataGraphsAndCSVFile("monthly", equityNameSymbolPrompt)

        continue    
    
    elif (int(dataFeedOptionInput) == 2):
        fromSymbolPrompt = input("Please enter the currency symbol converting from (from currency): ")

        toSymbolPrompt = input("Please enter the currency symbol converting to (to currency): ")

        typeOfData = input("Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printForexGraphsAndCSVFile("intraday", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "d"):
            printForexGraphsAndCSVFile("daily", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "w"):
            printForexGraphsAndCSVFile("weekly", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "m"):
            printForexGraphsAndCSVFile("monthly", fromSymbolPrompt, toSymbolPrompt)

        continue    
   
    
    elif (int(dataFeedOptionInput) == 3):
        equityNameSymbolPrompt = input("Please enter the Cryptocurrency symbol of the equity you want to see information for: ")

        exchangeMarketPrompt = input("Please enter the exchange market symbol you want to see the equity value in: ")

        typeOfData = input("Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printCryptoDataGraphsAndCSVFile("intraday", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "d"):
            printCryptoDataGraphsAndCSVFile("daily", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "w"):
            printCryptoDataGraphsAndCSVFile("weekly", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "m"):
            printCryptoDataGraphsAndCSVFile("monthly", equityNameSymbolPrompt, exchangeMarketPrompt)

        continue    
   
    else:
        print("End of Program")
        break


