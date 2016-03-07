# -*- coding: utf-8 -*-
import pandas
import numpy
import matplotlib.pyplot as plt
import csv
import time

from HouseModel import HouseModel


csvName = 'houseList_1457298702.57.csv'
print('csvName:' + csvName)

def adjustPrice(row):
    if(row['isPro'] == True):
        return row['price'] - (row['price']*7.5/100.0)
    else:
        return row['price']

def m2AdjustPrice(row):
    if(row['surface'] != 0):
        return row['adjustPrice']/row['surface']
    else:
        return 0

dataFrame = pandas.read_csv(csvName, sep=',', header='infer', encoding='utf-8')
dataFrame = dataFrame[pandas.notnull(dataFrame['city'])]
dataFrame['adjustPrice'] = dataFrame.apply (lambda row: adjustPrice(row),axis=1)
dataFrame['m2adjustPrice'] = dataFrame.apply (lambda row: m2AdjustPrice(row),axis=1)
dataFrame = dataFrame[pandas.notnull(dataFrame['m2price'])]
dataFrame = dataFrame[dataFrame['m2adjustPrice']>0]
dataFrame = dataFrame[dataFrame['adjustPrice']<270000]
dataFrame = dataFrame[dataFrame['surface']>80]
dataFrame = dataFrame.groupby(as_index=False, by=['city']).agg({'m2adjustPrice': numpy.mean}).sort('m2adjustPrice')
dataFrame.plot(kind='bar', x='city', y='m2adjustPrice')
plt.show()