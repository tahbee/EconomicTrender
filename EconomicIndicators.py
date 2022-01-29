import requests
import pandas
import matplotlib.pyplot as pythonPlot
import numpy
import csv
import datetime
import seaborn
from pylab import *
from matplotlib import dates


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
    pythonPlot.plot(economicIndicatorsTimeStampValues[-10:], economicIndicatorsDataValues[-10:], color='green', marker='o') #retrieve last 10 elements of list

    if (dataOption == 1):
        pythonPlot.title('Line Graph of Annual Real GDP of US per year for last 10 years (Download the CSV file at the end to see complete data of all the years in the past)', fontsize=10)
        
    elif (dataOption == 4):
        pythonPlot.title('Line Graph of Monthly Unemployment Rate Of US for last 10 months (Download the CSV file at the end to see complete data of all the years in the past)', fontsize=10)
        
    elif (dataOption == 2):
        pythonPlot.title('Line Graph of Monthly Interest Rate Of US for last 10 months (Download the CSV file at the end to see complete data of all the years in the past)', fontsize=10)

    elif (dataOption == 3):
        pythonPlot.title('Line Graph of Annual Inflation Rate Of US per year for last 10 years (Download the CSV file at the end to see complete data of all the years in the past)', fontsize=10)

        
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
        axis.set_title('Scatter Plot For Annual Real GDP of US per year (With 95% Confidence Interval Linear Regression Model Fit)')
        
    elif (dataOption == 4):
        axis.set_title('Scatter Plot For Monthly Unemployment rates of US (With 95% Confidence Interval Linear Regression Model Fit)')
        
    elif (dataOption == 2):
        axis.set_title('Scatter Plot For Monthly Interest rates of US (With 95% Confidence Interval Linear Regression Model Fit)')
        
    elif (dataOption == 3):
        axis.set_title('Scatter Plot For Annual Inflation rates of US (With 95% Confidence Interval Linear Regression Model Fit)')

    axis.xaxis.set_major_formatter(formattedDateValues)

    axis.tick_params(labelrotation=45)


    boxPlotFigure, axisCoordinates = pythonPlot.subplots()
    
    pandasDataFrame = pandas.DataFrame({'Value': economicIndicatorsDataValues})

    axisCoordinates = pandasDataFrame.boxplot(column=['Value'], figsize=(15,5), grid=True)

    if (dataOption == 1):
        axisCoordinates.set_title('Box Plot For Annual Real GDP of US per year')
        
    elif (dataOption == 4):
        axisCoordinates.set_title('Box Plot For Monthly Unemployment rates of US')
        
    elif (dataOption == 2):
        axisCoordinates.set_title('Box Plot For Monthly Interest rates of US')
        
    elif (dataOption == 3):
        axisCoordinates.set_title('Box Plot For Annual Inflation rates of US')

    pythonPlot.show()

    csvDownloadPrompt = input("Do you want to download the entire dataset? (y/n): ")

    if (csvDownloadPrompt == 'y'):
        try:
            economicIndicatorsCSVHeader = ['Date','Value']

            currentTime = datetime.datetime.now()

            fileNameToSave = ''

            if (dataOption == 1):
                fileNameToSave = 'Annual_US_GDP_'+str(currentTime)+'.csv'

            elif (dataOption == 4):
                fileNameToSave = 'Monthly_Unemployment_Data_'+str(currentTime)+'.csv'

            elif (dataOption == 2):
                fileNameToSave = 'Monthly_Interest_Rate_'+str(currentTime)+'.csv'

            elif (dataOption == 3):
                fileNameToSave = 'Annual_Inflation_Rate_'+str(currentTime)+'.csv'
    
            with open(fileNameToSave, 'w', encoding="utf-8") as economicIndicatorsCSVFile:
                economicIndicatorsCSVWriter = csv.writer(economicIndicatorsCSVFile, delimiter='\t')

                economicIndicatorsCSVWriter.writerow(economicIndicatorsCSVHeader)

                for economicIndicatorItem in zip(economicIndicatorsTimeStampValues,economicIndicatorsDataValues):
                    economicIndicatorsCSVWriter.writerow(economicIndicatorItem)

            print("File successfully saved. Please check your Documents, Downloads or any other folders in C drive or Finder where you set the default download path.")        
        except:
            print("An exception occurred")
            
while (True):
    dataFeedOptionInput = input ("\nThis program shows the data containing the following options: 1) Annual Real GDP of US, 2) Monthly interest rates of US, 3) Annual Inflation rates of US and 4) Monthly Unemployment data of US. Enter an option number to continue or 0 to end the program: ")
    
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
