import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
from pylab import *
import sys
import datetime
import seaborn
from matplotlib import dates


def printStockDataGraphsAndCSVFile(stockDataType, equityNameSymbolPrompt):
    stockTimeStampValues = []
    stockOpenPriceValues = []
    stockHighPriceValues = []
    stockLowPriceValues = []
    stockClosePriceValues = []
    stockVolumeValues = []

    stockTimeSeriesAPIUrl = ""

    try:
        mostRecentStockClosePriceValues, mostRecentStockHighPriceValues, mostRecentStockLowPriceValues, mostRecentStockOpenPriceValues, mostRecentStockTimeStampValues, mostRecentStockVolumeValues \
            = getStockInfoFromAPI(equityNameSymbolPrompt, stockClosePriceValues, stockDataType, stockHighPriceValues,
                                  stockLowPriceValues,
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
        plot_price.legend(bbox_to_anchor=(1, 1), loc='upper left')

        plot_volume.barh(XAxisCoordinateLocations + width, pandasDataFrame.volume, width, color='purple', label='Volume',
                         align='center')
        plot_volume.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                        ylim=[2 * width - 1, len(pandasDataFrame)])
        plot_volume.legend(bbox_to_anchor=(1, 1), loc='upper left')
        figure.tight_layout()

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

        centralTendencyMeasures = pandasDataFrame.describe()

        pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'], figsize=(15, 5), grid=True,
                                ax=box_plot_price)
        pandasDataFrame.boxplot(column=['Volume'], figsize=(15, 5), grid=True, ax=box_plot_volume)

        if (stockDataType == "intraday"):
            print("\nIntraday Stock Central Tendency Measures: \n", centralTendencyMeasures)

            box_plot_price.set_title('Stock Price Trends Intraday Box Plot')
            box_plot_volume.set_title('Stock Volume Trends Intraday Box Plot ')
        elif (stockDataType == "daily"):
            print("\nDaily Stock Central Tendency Measures: \n", centralTendencyMeasures)

            box_plot_price.set_title('Stock Price Trends Daily Box Plot')
            box_plot_volume.set_title('Stock Volume Trends Daily Box Plot ')
        elif (stockDataType == "weekly"):
            print("\nWeekly Stock Central Tendency Measures: \n", centralTendencyMeasures)

            box_plot_price.set_title('Stock Price Trends Weekly Box Plot')
            box_plot_volume.set_title('Stock Volume Trends Weekly Box Plot')
        elif (stockDataType == "monthly"):
            print("\nMonthly Stock Central Tendency Measures: \n", centralTendencyMeasures)

            box_plot_price.set_title('Stock Price Trends Monthly Box Plot')
            box_plot_volume.set_title('Stock Volume Trends Monthly Box Plot')

        pythonPlot.show()

        csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

        if (csvDownloadPrompt == 'y'):
            try:
                stockTrendsCSVHeader = ['TimeStamp', 'Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']

                currentTime = datetime.datetime.now()

                fileNameToSave = ''

                if (stockDataType == "intraday"):
                    fileNameToSave = 'stockTrends_Intraday_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (stockDataType == "daily"):
                    fileNameToSave = 'stockTrends_Daily_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (stockDataType == "weekly"):
                    fileNameToSave = 'stockTrends_Weekly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (stockDataType == "monthly"):
                    fileNameToSave = 'stockTrends_Monthly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

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
                        "All files are successfully saved. Please check your Downloads folder or your default download path.")
            except:
                print("An exception occurred with file download")
    except IndexError:
        print("\nInvalid stock symbol. Please try again.")
    except Exception as e:
        print(e)


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
    mostRecentStockOpenPriceValues = [float(x) for x in stockOpenPriceValues[:5]]
    mostRecentStockHighPriceValues = [float(x) for x in stockHighPriceValues[:5]]
    mostRecentStockLowPriceValues = [float(x) for x in stockLowPriceValues[:5]]
    mostRecentStockClosePriceValues = [float(x) for x in stockClosePriceValues[:5]]
    mostRecentStockVolumeValues = [int(x) for x in stockVolumeValues[:5]]
    return mostRecentStockClosePriceValues, mostRecentStockHighPriceValues, mostRecentStockLowPriceValues, mostRecentStockOpenPriceValues, mostRecentStockTimeStampValues, mostRecentStockVolumeValues


def printCryptoDataGraphsAndCSVFile(cryptoDataType, equityNameSymbolPrompt, exchangeMarketPrompt):
    cryptoTimeStampValues = []
    cryptoOpenPriceValues = []
    cryptoHighPriceValues = []
    cryptoLowPriceValues = []
    cryptoClosePriceValues = []
    cryptoVolumeValues = []

    cryptoTimeSeriesAPIUrl = ""

    try:
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

        timeSeriesJSONArray = cryptoData[list(cryptoData.keys())[1]]

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

        mostRecentCryptoOpenPriceValues = [float(x) for x in cryptoOpenPriceValues[:5]]

        mostRecentCryptoHighPriceValues = [float(x) for x in cryptoHighPriceValues[:5]]

        mostRecentCryptoLowPriceValues = [float(x) for x in cryptoLowPriceValues[:5]]

        mostRecentCryptoClosePriceValues = [float(x) for x in cryptoClosePriceValues[:5]]

        mostRecentCryptoVolumeValues = [float(x) for x in cryptoVolumeValues[:5]]

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
        plot_price.legend(bbox_to_anchor=(1, 1), loc='upper left')
        plot_volume.barh(XAxisCoordinateLocations, pandasDataFrame.volume, .5, color='purple', label='Volume',
                         align='center')
        plot_volume.set(yticks=XAxisCoordinateLocations + width, yticklabels=pandasDataFrame.graph,
                        ylim=[2 * width - 1, len(pandasDataFrame)])
        plot_volume.legend(bbox_to_anchor=(1, 1), loc='upper left')
        figure.tight_layout()

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

        centralTendencyMeasures = pandasDataFrame.describe()

        pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'], figsize=(15, 5), grid=True,
                                ax=boxplot_price)
        pandasDataFrame.boxplot(column=['Volume'], figsize=(15, 5), grid=True, ax=boxplot_volume)

        if (cryptoDataType == "intraday"):
            print("\nIntraday Crypto Price Central Tendency Measures = \n", centralTendencyMeasures)
            boxplot_price.set_title('Crypto Price Trends Intraday Box Plot')
            boxplot_volume.set_title('Crypto Volume Trends Intraday Box Plot')
        elif (cryptoDataType == "daily"):
            print("\nDaily Crypto Price Central Tendency Measures = \n", centralTendencyMeasures)
            boxplot_price.set_title('Crypto Price Trends Daily Box Plot')
            boxplot_volume.set_title('Crypto Volume Trends Daily Box Plot')
        elif (cryptoDataType == "weekly"):
            print("\nWeekly Crypto Price Central Tendency Measures = \n", centralTendencyMeasures)
            boxplot_price.set_title('Crypto Price Trends Weekly Box Plot')
            boxplot_volume.set_title('Crypto Volume Trends Weekly Box Plot')
        elif (cryptoDataType == "monthly"):
            print("\nMonthly Crypto Price Central Tendency Measures =\n", centralTendencyMeasures)
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
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (cryptoDataType == "daily"):
                    fileNameToSave = 'cryptoTrends_Daily_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (cryptoDataType == "weekly"):
                    fileNameToSave = 'cryptoTrends_Weekly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (cryptoDataType == "monthly"):
                    fileNameToSave = 'cryptoTrends_Monthly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

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
                        "All files are successfully saved. Please check your Downloads folder or your default download path.")
            except:
                print("An exception occurred with file download")
    except IndexError:
        print("\nInvalid cryptocurrency and/or market symbol. Please try again.")
    except Exception as e:
        print(e)


def printForexGraphsAndCSVFile(forexDataType, fromSymbolPrompt, toSymbolPrompt):
    forexTimeStampValues = []
    forexOpenPriceValues = []
    forexHighPriceValues = []
    forexLowPriceValues = []
    forexClosePriceValues = []

    forexTimeSeriesAPIUrl = ""

    try:
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

        timeSeriesJSONArray = forexData[list(forexData.keys())[1]]

        for timeSeriesKey in timeSeriesJSONArray:
            timeSeriesJSONObject = timeSeriesJSONArray[timeSeriesKey]

            forexTimeStampValues.append(timeSeriesKey)

            forexOpenPriceValues.append(timeSeriesJSONObject["1. open"])

            forexHighPriceValues.append(timeSeriesJSONObject["2. high"])

            forexLowPriceValues.append(timeSeriesJSONObject["3. low"])

            forexClosePriceValues.append(timeSeriesJSONObject["4. close"])

        mostRecentForexTimeStampValues = forexTimeStampValues[:5]

        mostRecentForexOpenPriceValues = [float(x) for x in forexOpenPriceValues[:5]]

        mostRecentForexHighPriceValues = [float(x) for x in forexHighPriceValues[:5]]

        mostRecentForexLowPriceValues = [float(x) for x in forexLowPriceValues[:5]]

        mostRecentForexClosePriceValues = [float(x) for x in forexClosePriceValues[:5]]

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
        axis.legend(bbox_to_anchor=(1, 1), loc='upper left')
        figure.tight_layout()

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

        centralTendencyMeasures = pandasDataFrame.describe()

        axisCoordinates = pandasDataFrame.boxplot(column=['Open Price', 'High Price', 'Low Price', 'Close Price'],
                                                  figsize=(15, 5), grid=True)

        if (forexDataType == "intraday"):
            print("\nIntraday Forex Trends Central Tendency Measures = \n", centralTendencyMeasures)
            axisCoordinates.set_title('Forex Trends Intraday Box Plot')
        elif (forexDataType == "daily"):
            print("\Daily Forex Trends Central Tendency Measures = \n", centralTendencyMeasures)
            axisCoordinates.set_title('Forex Trends Daily Box Plot')
        elif (forexDataType == "weekly"):
            print("\nWeekly Forex Trends Central Tendency Measures = \n", centralTendencyMeasures)
            axisCoordinates.set_title('Forex Trends Weekly Box Plot')
        elif (forexDataType == "monthly"):
            print("\nMonthly Forex Trends Central Tendency Measures = \n", centralTendencyMeasures)
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
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (forexDataType == "daily"):
                    fileNameToSave = 'forexTrends_Daily_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (forexDataType == "weekly"):
                    fileNameToSave = 'forexTrends_Weekly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

                elif (forexDataType == "monthly"):
                    fileNameToSave = 'forexTrends_Monthly_' + str(currentTime) + '.csv'
                    centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

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
                        "All files are successfully saved. Please check your Downloads folder or your default download path.")
            except:
                print("An exception occurred with file download")
    except IndexError:
        print("\nInvalid currency symbol. Please try again.")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while (True):
        dataFeedOptionInput = input("\nWelcome to Economic Trender application! This is section 1 of 2. We will display data for the " +
                                    "following three categories of data:"
                                    "\nOption 1 - Stock Time Series" +
                                    "\nOption 2 - Foreign Exchange Rate"
                                    "\nOption 3 - Cryptocurrencies" +
                                    "\nPlease enter a number between 1-3 to continue or 0 for the next section: ")

        if int(dataFeedOptionInput) == 1:
            equityNameSymbolPrompt = input(
                "Please enter the Stock symbol of the equity you want to see information for: ")

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
            else:
                print("\n" + typeOfData + " is not a valid timeframe. Please enter the correct timeframe symbol (i, d, w, or m)")
            continue

        elif (int(dataFeedOptionInput) == 2):
            fromSymbolPrompt = input("Please enter the currency symbol converting from (from currency): ")

            toSymbolPrompt = input("Please enter the currency symbol converting to (to currency): ")

            typeOfData = input(
                "Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

            if (typeOfData == "i"):
                printForexGraphsAndCSVFile("intraday", fromSymbolPrompt, toSymbolPrompt)
            elif (typeOfData == "d"):
                printForexGraphsAndCSVFile("daily", fromSymbolPrompt, toSymbolPrompt)
            elif (typeOfData == "w"):
                printForexGraphsAndCSVFile("weekly", fromSymbolPrompt, toSymbolPrompt)
            elif (typeOfData == "m"):
                printForexGraphsAndCSVFile("monthly", fromSymbolPrompt, toSymbolPrompt)
            else:
                print("\n" + typeOfData + " is not a valid timeframe. Please enter the correct timeframe symbol (i, d, w, or m)")
            continue

        elif (int(dataFeedOptionInput) == 3):
            equityNameSymbolPrompt = input(
                "Please enter the Cryptocurrency symbol of the equity you want to see information for: ")

            exchangeMarketPrompt = input(
                "Please enter the exchange market symbol you want to see the equity value in: ")

            typeOfData = input(
                "Do you want to see intraday (5 minute interval), daily, weekly or monthly data? Enter i for intraday, d for daily, w for weekly, and m for monthly: ")

            if (typeOfData == "i"):
                printCryptoDataGraphsAndCSVFile("intraday", equityNameSymbolPrompt, exchangeMarketPrompt)
            elif (typeOfData == "d"):
                printCryptoDataGraphsAndCSVFile("daily", equityNameSymbolPrompt, exchangeMarketPrompt)
            elif (typeOfData == "w"):
                printCryptoDataGraphsAndCSVFile("weekly", equityNameSymbolPrompt, exchangeMarketPrompt)
            elif (typeOfData == "m"):
                printCryptoDataGraphsAndCSVFile("monthly", equityNameSymbolPrompt, exchangeMarketPrompt)
            else:
                print("\n" + typeOfData + " is not a valid timeframe. Please enter the correct timeframe symbol (i, d, w, or m)")
            continue
        else:
            print("End of Economic Trender Section. We will now go the next section.")
            break


def economicIndicatorsData(dataOption):
    economicIndicatorsTimeStampValues = []
    economicIndicatorsDataValues = []

    economicIndicatorsAPIUrl = ''

    if (dataOption == 1):
        economicIndicatorsAPIUrl = 'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=J4RQ2HAVH7OZNSRM'

    elif (dataOption == 4):
        economicIndicatorsAPIUrl = 'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=J4RQ2HAVH7OZNSRM'

    elif (dataOption == 2):
        economicIndicatorsAPIUrl = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=J4RQ2HAVH7OZNSRM'

    elif (dataOption == 3):
        economicIndicatorsAPIUrl = 'https://www.alphavantage.co/query?function=INFLATION&apikey=demo'

    economicIndicatorsDataFeedResponse = requests.get(economicIndicatorsAPIUrl)
    economicIndicatorsData = economicIndicatorsDataFeedResponse.json()

    economicIndicatorsJSONArray = economicIndicatorsData["data"]

    for economicIndicatorsJSONObject in economicIndicatorsJSONArray:
        economicIndicatorsTimeStampValues.append(economicIndicatorsJSONObject["date"])

        economicIndicatorsDataValues.append(float(economicIndicatorsJSONObject["value"]))

    economicIndicatorsTimeStampValues.reverse()
    economicIndicatorsDataValues.reverse()
    pythonPlot.plot(economicIndicatorsTimeStampValues[-10:], economicIndicatorsDataValues[-10:], color='green',
                    marker='o')  # retrieve last 10 elements of list

    if (dataOption == 1):
        pythonPlot.title(
            'Line Graph of Annual Real GDP of US per year for last 10 years (Download the CSV file at the end to see complete data of all the years in the past)',
            fontsize=10)

    elif (dataOption == 4):
        pythonPlot.title(
            'Line Graph of Monthly Unemployment Rate Of US for last 10 months (Download the CSV file at the end to see complete data of all the years in the past)',
            fontsize=10)

    elif (dataOption == 2):
        pythonPlot.title(
            'Line Graph of Monthly Interest Rate Of US for last 10 months (Download the CSV file at the end to see complete data of all the years in the past)',
            fontsize=10)

    elif (dataOption == 3):
        pythonPlot.title(
            'Line Graph of Annual Inflation Rate Of US per year for last 10 years (Download the CSV file at the end to see complete data of all the years in the past)',
            fontsize=10)

    pythonPlot.xlabel('Date', fontsize=10)
    pythonPlot.ylabel('Value', fontsize=10)
    pythonPlot.grid(True)
    pythonPlot.show()

    pandasDataFrame = pandas.DataFrame({
        'date': pandas.to_datetime(economicIndicatorsTimeStampValues),
        'Date': dates.datestr2num(economicIndicatorsTimeStampValues),
        'Value': economicIndicatorsDataValues
    })

    @pythonPlot.FuncFormatter
    def formattedDateValues(dateInput, position):
        return dates.num2date(dateInput).strftime('%Y-%m-%d')

    figure, axis = pythonPlot.subplots()
    seaborn.regplot('Date', 'Value', data=pandasDataFrame, ax=axis)

    if (dataOption == 1):
        axis.set_title(
            'Scatter Plot For Annual Real GDP of US per year (With 95% Confidence Interval Linear Regression Model Fit)')

    elif (dataOption == 4):
        axis.set_title(
            'Scatter Plot For Monthly Unemployment rates of US (With 95% Confidence Interval Linear Regression Model Fit)')

    elif (dataOption == 2):
        axis.set_title(
            'Scatter Plot For Monthly Interest rates of US (With 95% Confidence Interval Linear Regression Model Fit)')

    elif (dataOption == 3):
        axis.set_title(
            'Scatter Plot For Annual Inflation rates of US (With 95% Confidence Interval Linear Regression Model Fit)')

    axis.xaxis.set_major_formatter(formattedDateValues)

    axis.tick_params(labelrotation=45)

    boxPlotFigure, axisCoordinates = pythonPlot.subplots()

    pandasDataFrame = pandas.DataFrame({'Value': economicIndicatorsDataValues})

    axisCoordinates = pandasDataFrame.boxplot(column=['Value'], figsize=(15, 5), grid=True)

    if (dataOption == 1):
        axisCoordinates.set_title('Box Plot For Annual Real GDP of US per year')

    elif (dataOption == 4):
        axisCoordinates.set_title('Box Plot For Monthly Unemployment rates of US')

    elif (dataOption == 2):
        axisCoordinates.set_title('Box Plot For Monthly Interest rates of US')

    elif (dataOption == 3):
        axisCoordinates.set_title('Box Plot For Annual Inflation rates of US')

    pythonPlot.show()

    centralTendencyMeasures = pandasDataFrame.describe()
    if (dataOption == 1):
        print('Central Tendency Measures of Annual Real GDP of US per year= \n', centralTendencyMeasures)

    elif (dataOption == 4):
        print('Central Tendency Measures of Monthly Unemployment Rate Of US= \n', centralTendencyMeasures)


    elif (dataOption == 2):
        print('Central Tendency Measures of Monthly Interest Rate Of US= \n', centralTendencyMeasures)

    elif (dataOption == 3):
        print('Central Tendency Measures of Annual Inflation Rate Of US per year= \n', centralTendencyMeasures)

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            economicIndicatorsCSVHeader = ['Date', 'Value']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (dataOption == 1):
                fileNameToSave = 'Annual_US_GDP_' + str(currentTime) + '.csv'
                centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

            elif (dataOption == 4):
                fileNameToSave = 'Monthly_Unemployment_Data_' + str(currentTime) + '.csv'
                centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

            elif (dataOption == 2):
                fileNameToSave = 'Monthly_Interest_Rate_' + str(currentTime) + '.csv'
                centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

            elif (dataOption == 3):
                fileNameToSave = 'Annual_Inflation_Rate_' + str(currentTime) + '.csv'
                centralTendencyMeasures.to_csv("CentralTendencyMeasures_" + fileNameToSave)

            with open(fileNameToSave, 'w', encoding="utf-8") as economicIndicatorsCSVFile:
                economicIndicatorsCSVWriter = csv.writer(economicIndicatorsCSVFile, delimiter='\t')

                economicIndicatorsCSVWriter.writerow(economicIndicatorsCSVHeader)

                for economicIndicatorItem in zip(economicIndicatorsTimeStampValues, economicIndicatorsDataValues):
                    economicIndicatorsCSVWriter.writerow(economicIndicatorItem)

            print(
                "All files are successfully saved. Please check your Downloads folder or your default download path.")
        except:
            print("An exception occurred with file download")


while (True):
    dataFeedOptionInput = input(
        "\nWelcome to Economic Indicators Section. This is section 2 of 2. This program shows the data containing the following options: " +
        "\n1) Annual Real GDP of US" +
        "\n2) Monthly interest rates of US" +
        "\n3) Annual Inflation rates of US" +
        "\n4) Monthly Unemployment data of US" +
        "\nEnter a number between 1-4 to continue or 0 to end the program: ")

    if (int(dataFeedOptionInput) == 1):
        economicIndicatorsData(1)
        continue
    elif (int(dataFeedOptionInput) == 2):
        economicIndicatorsData(2)
        continue
    elif (int(dataFeedOptionInput) == 3):
        economicIndicatorsData(3)
        continue
    elif (int(dataFeedOptionInput) == 4):
        economicIndicatorsData(4)
        continue
    else:
        print("End Of Program")
        break