# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import pandas
import numpy
import matplotlib.pyplot as plt
import csv
import time

from HouseModel import HouseModel


def getBeautifulSoupFromUrl(url):
    sock = urllib.urlopen('http:'+url)
    htmlSource = sock.read()
    sock.close()
    return BeautifulSoup(htmlSource, 'html.parser', fromEncoding='latin-1')

def getNextPageUrl(housesListPageHtml):
    pagingHTML = housesListPageHtml.find('a', id='next')
    if (pagingHTML):
        return pagingHTML.get('href')
    else:
        return ''

def toDataFrame(arrayOfHouses):
       variables = arrayOfHouses[0].keys()
       return pandas.DataFrame([[getattr(i,j) for j in variables] for i in arrayOfHouses], columns = variables)

def writeCsv(csvName, houseList):
    with open(csvName, 'w') as csvfile:
        csvfile.write(u'\ufeff'.encode('utf8'))
        writer = csv.DictWriter(csvfile, fieldnames=houseList[0].item().keys())
        writer.writeheader()
        for house in houseList:
            writer.writerow(house.item())




pageToAnalyzeUrl = "//www.leboncoin.fr/ventes_immobilieres/offres/midi_pyrenees/haute_garonne/?o=1&ret=1"

pageNum = 1
pagelimit = 1000
housesList = []
csvName = 'houseList_'+str(time.time())+'.csv'
print('csvName:' + csvName)

while((not pageToAnalyzeUrl == '') & (not pageNum == pagelimit)):
    print('pageNum:' + str(pageNum))
    print('pageToAnalyzeUrl:' + pageToAnalyzeUrl)

    housesListPageHtml = getBeautifulSoupFromUrl(pageToAnalyzeUrl)
    housesHtml = housesListPageHtml.find(class_='tabsContent')
    for summaryHtml in housesHtml.find_all('li'):
        #print('------------------------------')
        moreDetailLink = summaryHtml.find('a').get('href')
        house = HouseModel(moreDetailLink)
        oneHousePageHtml = getBeautifulSoupFromUrl(moreDetailLink)
        house.parseSummaryHtml(summaryHtml.find('a'))
        house.parseHouseHtml(oneHousePageHtml)
        housesList.append(house)
      #  print(house.toStr())
       # print('------------------------------')
    pageToAnalyzeUrl = getNextPageUrl(housesListPageHtml)
    pageNum +=1

writeCsv(csvName,housesList)