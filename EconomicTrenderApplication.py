import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
from pylab import *
import sys


def printStockDataGraphsAndCSVFile(stockDataType, equityNameSymbolPrompt):
    stockTimeStampValues = []
    stockOpenPriceValues = []
    stockHighPriceValues = []
    stockLowPriceValues = []
    stockClosePriceValues = []
    stockVolumeValues = []

    stockTimeSeriesAPIUrl = ""

    mostRecentStockClosePriceValues, mostRecentStockHighPriceValues, mostRecentStockLowPriceValues, mostRecentStockOpenPriceValues, mostRecentStockTimeStampValues, mostRecentStockVolumeValues \
        = getStockInfoFromAPI(
        equityNameSymbolPrompt, stockClosePriceValues, stockDataType, stockHighPriceValues, stockLowPriceValues,
        stockOpenPriceValues, stockTimeSeriesAPIUrl, stockTimeStampValues, stockVolumeValues)

    pandasDataFrame = pandas.DataFrame(dict(graph=mostRecentStockTimeStampValues,
                                            openingPrice=mostRecentStockOpenPriceValues,
                                            highPrice=mostRecentStockHighPriceValues,
                                            lowPrice=mostRecentStockLowPriceValues,
                                            closingPrice=mostRecentStockClosePriceValues,
                                            volume=mostRecentStockVolumeValues))
    margin = 0.03
    numberColumns = 5
    XAxisCoordinateLocations = numpy.arange(numberColumns)
    width = (1 - (margin * numberColumns)) / numberColumns

    figure, (plot_price, plot_volume) = pythonPlot.subplots(2)
    plot_price.barh(XAxisCoordinateLocations, pandasDataFrame.openingPrice, width, color='red', label='Opening Price',
                    align='center')
    plot_price.barh(XAxisCoordinateLocations - width, pandasDataFrame.highPrice, width, color='green',
                    label='High Price', align='center')
    plot_price.barh(XAxisCoordinateLocations + width, pandasDataFrame.lowPrice, width, color='blue', label='Low Price',
                    align='center')
    plot_price.barh(XAxisCoordinateLocations + width * 2, pandasDataFrame.closingPrice, width, color='yellow',
                    label='Closing Price', align='center')
    plot_price.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                   ylim=[2 * width - 1, len(pandasDataFrame)])
    plot_price.legend()

    plot_volume.barh(XAxisCoordinateLocations + width, pandasDataFrame.volume, width, color='purple', label='Volume',
                     align='center')
    plot_volume.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                    ylim=[2 * width - 1, len(pandasDataFrame)])
    plot_volume.legend()

    if (stockDataType == "intraday"):
        plot_price.set_title('Stock Price Trends Intraday Horizontal Bar Chart')
        plot_volume.set_title('Stock Volume Trends Intraday Horizontal Bar Chart')
    elif (stockDataType == "daily"):
        plot_price.set_title('Stock Price Trends Daily Horizontal Bar Chart')
        plot_volume.set_title('Stock Volume Trends Daily Horizontal Bar Chart')
    elif (stockDataType == "weekly"):
        plot_price.set_title('Stock Price Trends Weekly Horizontal Bar Chart')
        plot_volume.set_title('Stock Volume Trends Weekly Horizontal Bar Chart')
    elif (stockDataType == "monthly"):
        plot_price.set_title('Stock Price Trends Monthly Horizontal Bar Chart')
        plot_volume.set_title('Stock Volume Trends Monthly Horizontal Bar Chart')

    pythonPlot.show()

    boxPlotFigure, (box_plot_price, box_plot_volume) = pythonPlot.subplots(2)

    pandasDataFrame = pandas.DataFrame({'Open Price': list(map(float, stockOpenPriceValues)),
                                        'High Price': list(map(float, stockHighPriceValues)),
                                        'Low Price': list(map(float, stockLowPriceValues)),
                                        'Close Price': list(map(float, stockClosePriceValues)),
                                        'Volume': list(map(float, stockVolumeValues))})

    pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'], figsize=(15, 5), grid=True,
                            ax=box_plot_price)
    pandasDataFrame.boxplot(column=['Volume'], figsize=(15, 5), grid=True, ax=box_plot_volume)

    if (stockDataType == "intraday"):
        box_plot_price.set_title('Stock Price Trends Intraday Box Plot')
        box_plot_volume.set_title('Stock Volume Trends Intraday Box Plot ')
    elif (stockDataType == "daily"):
        box_plot_price.set_title('Stock Price Trends Daily Box Plot')
        box_plot_volume.set_title('Stock Volume Trends Daily Box Plot ')
    elif (stockDataType == "weekly"):
        box_plot_price.set_title('Stock Price Trends Weekly Box Plot')
        box_plot_volume.set_title('Stock Volume Trends Weekly Box Plot')
    elif (stockDataType == "monthly"):
        box_plot_price.set_title('Stock Price Trends Monthly Box Plot')
        box_plot_volume.set_title('Stock Volume Trends Monthly Box Plot')

    # axisCoordinates[0].plot()
    pythonPlot.show()

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            stockTrendsCSVHeader = ['TimeStamp', 'Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (stockDataType == "intraday"):
                fileNameToSave = 'stockTrends_Intraday_' + str(currentTime) + '.csv'
            elif (stockDataType == "daily"):
                fileNameToSave = 'stockTrends_Daily_' + str(currentTime) + '.csv'
            elif (stockDataType == "weekly"):
                fileNameToSave = 'stockTrends_Weekly_' + str(currentTime) + '.csv'
            elif (stockDataType == "monthly"):
                fileNameToSave = 'stockTrends_Monthly_' + str(currentTime) + '.csv'

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

                print(
                    "All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")
        except:
            print("An exception occurred")


def getStockInfoFromAPI(equityNameSymbolPrompt, stockClosePriceValues, stockDataType, stockHighPriceValues,
                        stockLowPriceValues, stockOpenPriceValues, stockTimeSeriesAPIUrl, stockTimeStampValues,
                        stockVolumeValues):
    if (stockDataType == "intraday"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + equityNameSymbolPrompt + '&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "daily"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + equityNameSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "weekly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + equityNameSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (stockDataType == "monthly"):
        stockTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + equityNameSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    stockDataFeedResponse = requests.get(stockTimeSeriesAPIUrl)
    stockData = stockDataFeedResponse.json()

    try:
        timeSeriesJSONArray = stockData[list(stockData.keys())[1]]
    except IndexError:
        print("Invalid stock symbol. Please try again.")
        sys.exit(1)
    except Exception as e:
        print(e)

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
    return mostRecentStockClosePriceValues, mostRecentStockHighPriceValues, mostRecentStockLowPriceValues, mostRecentStockOpenPriceValues, mostRecentStockTimeStampValues, mostRecentStockVolumeValues


def printCryptoDataGraphsAndCSVFile(cryptoDataType, equityNameSymbolPrompt, exchangeMarketPrompt):
    cryptoTimeStampValues = []
    cryptoOpenPriceValues = []
    cryptoHighPriceValues = []
    cryptoLowPriceValues = []
    cryptoClosePriceValues = []
    cryptoVolumeValues = []

    cryptoTimeSeriesAPIUrl = ""

    if (cryptoDataType == "intraday"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=' + equityNameSymbolPrompt + '&market=' + exchangeMarketPrompt + '&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "daily"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=' + equityNameSymbolPrompt + '&market=' + exchangeMarketPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "weekly"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=' + equityNameSymbolPrompt + '&market=' + exchangeMarketPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (cryptoDataType == "monthly"):
        cryptoTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=' + equityNameSymbolPrompt + '&market=' + exchangeMarketPrompt + '&apikey=J4RQ2HAVH7OZNSRM'

    cryptoDataFeedResponse = requests.get(cryptoTimeSeriesAPIUrl)
    cryptoData = cryptoDataFeedResponse.json()

    try:
        timeSeriesJSONArray = cryptoData[list(cryptoData.keys())[1]]
    except IndexError:
        print("Invalid cryptocurrency symbol. Please try again.")
        sys.exit(1)
    except Exception as e:
        print(e)

    for timeSeriesKey in timeSeriesJSONArray:
        timeSeriesJSONObject = timeSeriesJSONArray[timeSeriesKey]

        cryptoTimeStampValues.append(timeSeriesKey)

        if (cryptoDataType == "intraday"):

            cryptoOpenPriceValues.append(timeSeriesJSONObject["1. open"])

            cryptoHighPriceValues.append(timeSeriesJSONObject["2. high"])

            cryptoLowPriceValues.append(timeSeriesJSONObject["3. low"])

            cryptoClosePriceValues.append(timeSeriesJSONObject["4. close"])

            cryptoVolumeValues.append(timeSeriesJSONObject["5. volume"])

        elif (cryptoDataType == "daily"):
            cryptoOpenPriceValues.append(timeSeriesJSONObject["1a. open (" + exchangeMarketPrompt + ")"])

            cryptoHighPriceValues.append(timeSeriesJSONObject["2a. high (" + exchangeMarketPrompt + ")"])

            cryptoLowPriceValues.append(timeSeriesJSONObject["3a. low (" + exchangeMarketPrompt + ")"])

            cryptoClosePriceValues.append(timeSeriesJSONObject["4a. close (" + exchangeMarketPrompt + ")"])

            cryptoVolumeValues.append(timeSeriesJSONObject["5. volume"])


        elif (cryptoDataType == "weekly"):
            cryptoOpenPriceValues.append(timeSeriesJSONObject["1a. open (" + exchangeMarketPrompt + ")"])

            cryptoHighPriceValues.append(timeSeriesJSONObject["2a. high (" + exchangeMarketPrompt + ")"])

            cryptoLowPriceValues.append(timeSeriesJSONObject["3a. low (" + exchangeMarketPrompt + ")"])

            cryptoClosePriceValues.append(timeSeriesJSONObject["4a. close (" + exchangeMarketPrompt + ")"])

            cryptoVolumeValues.append(timeSeriesJSONObject["5. volume"])


        elif (cryptoDataType == "monthly"):
            cryptoOpenPriceValues.append(timeSeriesJSONObject["1a. open (" + exchangeMarketPrompt + ")"])

            cryptoHighPriceValues.append(timeSeriesJSONObject["2a. high (" + exchangeMarketPrompt + ")"])

            cryptoLowPriceValues.append(timeSeriesJSONObject["3a. low (" + exchangeMarketPrompt + ")"])

            cryptoClosePriceValues.append(timeSeriesJSONObject["4a. close (" + exchangeMarketPrompt + ")"])

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

    margin = 0.03
    numberColumns = 5
    XAxisCoordinateLocations = numpy.arange(numberColumns)
    width = (1 - (margin * numberColumns)) / numberColumns

    figure, (plot_price, plot_volume) = pythonPlot.subplots(2)
    plot_price.barh(XAxisCoordinateLocations, pandasDataFrame.openingPrice, width, color='red', label='Opening Price',
                    align='center')
    plot_price.barh(XAxisCoordinateLocations - width * 2, pandasDataFrame.highPrice, width, color='green',
                    label='High Price', align='center')
    plot_price.barh(XAxisCoordinateLocations - width, pandasDataFrame.lowPrice, width, color='blue', label='Low Price',
                    align='center')
    plot_price.barh(XAxisCoordinateLocations + width, pandasDataFrame.closingPrice, width, color='yellow',
                    label='Closing Price', align='center')
    plot_price.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                   ylim=[2 * width - 1, len(pandasDataFrame)])
    plot_price.legend()
    plot_volume.barh(XAxisCoordinateLocations, pandasDataFrame.volume, .5, color='purple', label='Volume',
                     align='center')
    plot_volume.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                    ylim=[2 * width - 1, len(pandasDataFrame)])
    plot_volume.legend()

    if (cryptoDataType == "intraday"):
        plot_price.set_title('Crypto Price Trends Intraday Horizontal Bar Chart')
        plot_volume.set_title('Crypto Volume Trends Intraday Horizontal Bar Chart')
    elif (cryptoDataType == "daily"):
        plot_price.set_title('Crypto Price Trends Daily Horizontal Bar Chart')
        plot_volume.set_title('Crypto Volume Trends Daily Horizontal Bar Chart')
    elif (cryptoDataType == "weekly"):
        plot_price.set_title('Crypto Price Trends Weekly Horizontal Bar Chart')
        plot_volume.set_title('Crypto Volume Trends Weekly Horizontal Bar Chart')
    elif (cryptoDataType == "monthly"):
        plot_price.set_title('Crypto Price Trends Monthly Horizontal Bar Chart')
        plot_volume.set_title('Crypto Volume Trends Monthly Horizontal Bar Chart')
    pythonPlot.show()

    boxPlotFigure, (boxplot_price, boxplot_volume) = pythonPlot.subplots(2)

    pandasDataFrame = pandas.DataFrame({'Open Price': list(map(float, cryptoOpenPriceValues)),
                                        'High Price': list(map(float, cryptoHighPriceValues)),
                                        'Low Price': list(map(float, cryptoLowPriceValues)),
                                        'Close Price': list(map(float, cryptoClosePriceValues)),
                                        'Volume': list(map(float, cryptoVolumeValues))})

    pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'], figsize=(15, 5), grid=True,
                            ax=boxplot_price)
    pandasDataFrame.boxplot(column=['Volume'], figsize=(15, 5), grid=True, ax=boxplot_volume)

    if (cryptoDataType == "intraday"):
        boxplot_price.set_title('Crypto Price Trends Intraday Box Plot')
        boxplot_volume.set_title('Crypto Volume Trends Intraday Box Plot')
    elif (cryptoDataType == "daily"):
        boxplot_price.set_title('Crypto Price Trends Daily Box Plot')
        boxplot_volume.set_title('Crypto Volume Trends Daily Box Plot')
    elif (cryptoDataType == "weekly"):
        boxplot_price.set_title('Crypto Price Trends Weekly Box Plot')
        boxplot_volume.set_title('Crypto Volume Trends Weekly Box Plot')
    elif (cryptoDataType == "monthly"):
        boxplot_price.set_title('Crypto Price Trends Monthly Box Plot')
        boxplot_volume.set_title('Crypto Volume Trends Monthly Box Plot')

    pythonPlot.show()

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            cryptoTrendsCSVHeader = ['TimeStamp', 'Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (cryptoDataType == "intraday"):
                fileNameToSave = 'cryptoTrends_Intraday_' + str(currentTime) + '.csv'
            elif (cryptoDataType == "daily"):
                fileNameToSave = 'cryptoTrends_Daily_' + str(currentTime) + '.csv'
            elif (cryptoDataType == "weekly"):
                fileNameToSave = 'cryptoTrends_Weekly_' + str(currentTime) + '.csv'
            elif (cryptoDataType == "monthly"):
                fileNameToSave = 'cryptoTrends_Monthly_' + str(currentTime) + '.csv'

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

                print(
                    "All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")
        except Exception as e:
            print("Exception: " + e)


def printForexGraphsAndCSVFile(forexDataType, fromSymbolPrompt, toSymbolPrompt):
    forexTimeStampValues = []
    forexOpenPriceValues = []
    forexHighPriceValues = []
    forexLowPriceValues = []
    forexClosePriceValues = []

    forexTimeSeriesAPIUrl = ""

    if (forexDataType == "intraday"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=' + fromSymbolPrompt + '&to_symbol=' + toSymbolPrompt + '&interval=5min&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "daily"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=' + fromSymbolPrompt + '&to_symbol=' + toSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "weekly"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=' + fromSymbolPrompt + '&to_symbol=' + toSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'
    elif (forexDataType == "monthly"):
        forexTimeSeriesAPIUrl = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=' + fromSymbolPrompt + '&to_symbol=' + toSymbolPrompt + '&apikey=J4RQ2HAVH7OZNSRM'

    forexDataFeedResponse = requests.get(forexTimeSeriesAPIUrl)
    forexData = forexDataFeedResponse.json()

    try:
        timeSeriesJSONArray = forexData[list(forexData.keys())[1]]
    except IndexError:
        print("Invalid currency symbol. Please try again.")
        sys.exit(1)
    except Exception as e:
        print(e)

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
    axis.barh(XAxisCoordinateLocations + 0.2, pandasDataFrame.closingPrice, width, color='yellow',
              label='Closing Price')

    axis.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
             ylim=[2 * width - 1, len(pandasDataFrame)])
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

    axisCoordinates = pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'],
                                              figsize=(15, 5), grid=True)

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
            forexTrendsCSVHeader = ['TimeStamp', 'Opening Price', 'High Price', 'Low Price', 'Closing Price']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (forexDataType == "intraday"):
                fileNameToSave = 'forexTrends_Intraday_' + str(currentTime) + '.csv'
            elif (forexDataType == "daily"):
                fileNameToSave = 'forexTrends_Daily_' + str(currentTime) + '.csv'
            elif (forexDataType == "weekly"):
                fileNameToSave = 'forexTrends_Weekly_' + str(currentTime) + '.csv'
            elif (forexDataType == "monthly"):
                fileNameToSave = 'forexTrends_Monthly_' + str(currentTime) + '.csv'

            with open(fileNameToSave, 'w', encoding="utf-8") as forexTrendsCSVFile:
                forexCSVWriter = csv.writer(forexTrendsCSVFile, delimiter='\t')

                forexCSVWriter.writerow(forexTrendsCSVHeader)

                for forexItem in zip(forexTimeStampValues,
                                     forexOpenPriceValues,
                                     forexHighPriceValues,
                                     forexLowPriceValues,
                                     forexClosePriceValues):
                    forexCSVWriter.writerow(forexItem)

                print(
                    "All files are successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")
        except:
            print("An exception occurred")


if __name__ == '__main__':
    dataFeedOptionInput = input("\nWelcome to Economic Trender application! We will display data for the " +
                                "following 3 categories of data:"
                                "\nOption 1 - Stock Time Series" +
                                "\nOption 2 - Foreign Exchange Rate"
                                "\nOption 3 - Cryptocurrencies" +
                                "\nPlease enter a number between 1-3 to choose an option from the 3 categories above or press 0 to end the program: ")

    if int(dataFeedOptionInput) == 1:
        equityNameSymbolPrompt = input("Please enter the Stock symbol of the equity you want to see information for: ")

        typeOfData = input(
            "Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printStockDataGraphsAndCSVFile("intraday", equityNameSymbolPrompt)
        elif (typeOfData == "d"):
            printStockDataGraphsAndCSVFile("daily", equityNameSymbolPrompt)
        elif (typeOfData == "w"):
            printStockDataGraphsAndCSVFile("weekly", equityNameSymbolPrompt)
        elif (typeOfData == "m"):
            printStockDataGraphsAndCSVFile("monthly", equityNameSymbolPrompt)

    elif (int(dataFeedOptionInput) == 2):
        fromSymbolPrompt = input("Please enter the currency symbol converting from (from currency): ")

        toSymbolPrompt = input("Please enter the currency symbol converting to (to currency): ")

        typeOfData = input(
            "Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printForexGraphsAndCSVFile("intraday", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "d"):
            printForexGraphsAndCSVFile("daily", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "w"):
            printForexGraphsAndCSVFile("weekly", fromSymbolPrompt, toSymbolPrompt)
        if (typeOfData == "m"):
            printForexGraphsAndCSVFile("monthly", fromSymbolPrompt, toSymbolPrompt)


    elif (int(dataFeedOptionInput) == 3):
        equityNameSymbolPrompt = input(
            "Please enter the Cryptocurrency symbol of the equity you want to see information for: ")

        exchangeMarketPrompt = input("Please enter the exchange market symbol you want to see the equity value in: ")

        typeOfData = input(
            "Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

        if (typeOfData == "i"):
            printCryptoDataGraphsAndCSVFile("intraday", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "d"):
            printCryptoDataGraphsAndCSVFile("daily", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "w"):
            printCryptoDataGraphsAndCSVFile("weekly", equityNameSymbolPrompt, exchangeMarketPrompt)
        if (typeOfData == "m"):
            printCryptoDataGraphsAndCSVFile("monthly", equityNameSymbolPrompt, exchangeMarketPrompt)

    else:
        print("End of Program")
