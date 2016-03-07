# -*- coding: utf-8 -*-
import re
trim = re.compile(r'\s+')
findNumber = re.compile(r'([0-9]{1,10})')

class HouseModel:
    def __init__(self, link):
        self.link = link
        self.title = ''
        self.price = 0
        self.surface = 0
        self.hasPictures = False
        self.isPro = False
        self.city = ''
        self.postalCode = 0
        self.state = ''
        self.nbrRooms = 0
        self.ges = ''
        self.ces = ''
        self.m2price = 0
        self.type = ''

    def parseHouseHtml(self, oneHouseHtml):
        itemImageHtml = oneHouseHtml.find(class_='item_image')
        if itemImageHtml:
            if 'empty' not in itemImageHtml.attrs.get('class'):
                self.hasPictures = True

        titleHtml = oneHouseHtml.find('h1')
        if titleHtml: self.title = titleHtml.get_text().strip()

        for lineHtml in oneHouseHtml.find_all(class_='line'):
            propertyHtml = lineHtml.find(class_='property')
            htmlValue = lineHtml.find(class_='value')


            if 'line_pro' in lineHtml.attrs.get('class'):
                self.isPro = True
            if propertyHtml:
                if unicode(propertyHtml.get_text().strip()) == u'Prix':
                    priceList = findNumber.findall(trim.sub('',htmlValue.get_text()))
                    if len(priceList): self.price = int(priceList[0])

                if unicode(propertyHtml.get_text().strip()) == u'Ville':
                    self.city = filter(lambda x: x.isalpha(), htmlValue.get_text()).strip()
                    postalCodeList = findNumber.findall(trim.sub('',htmlValue.get_text()))
                    self.postalCode = int(postalCodeList[0])

                if unicode(propertyHtml.get_text().strip()) == u'Description :':
                    self.description = trim.sub(' ',htmlValue.get_text())

                if unicode(propertyHtml.get_text().strip()) == u'Type de bien':
                    self.type = trim.sub(' ',htmlValue.get_text())

                if unicode(propertyHtml.get_text().strip()) == u'Pièces':
                    self.nbrRooms = int(htmlValue.get_text().strip())

                if unicode(propertyHtml.get_text().strip()) == u'Surface':
                    surfaceList = findNumber.findall(htmlValue.get_text().replace(" ", ""))
                    if(len(surfaceList)>0):
                        self.surface = int(surfaceList[0])

                if unicode(propertyHtml.get_text().strip()) == u'GES':
                    self.ges = htmlValue.get_text().strip()[0]

                if unicode(propertyHtml.get_text().strip()) == u'Classe énergie':
                    self.ces = htmlValue.get_text().strip()[0]

        if self.surface:
            if self.price:
                self.m2price = int(self.price)/int(self.surface)

    def parseSummaryHtml(self, summaryHtml):
            detailHtml = summaryHtml.find(class_='item_infos')
            titleHtml = detailHtml.find(class_='item_title')
            priceHtml = detailHtml.find(class_='item_price')

            if titleHtml:
                self.title=titleHtml.get_text().strip()

            if priceHtml:
                priceList = findNumber.findall(trim.sub('',priceHtml.get_text()))
                if len(priceList): self.price = priceList[0]

            for detailSuppHtml in detailHtml.find_all(class_='item_supp'):
                if detailSuppHtml.find(class_='isPro'):
                    if 'pro' in detailSuppHtml.find(class_='isPro').get_text():
                        self.isPro = True

                if '/' in detailSuppHtml.get_text():
                    placement = trim.sub(' ',detailSuppHtml.get_text()).split('/')
                    if(len(placement) == 1):
                        self.state = placement[0]
                    elif(len(placement) == 2):
                        self.state = placement[1]


    def toStr(self):
        if self.link: print 'link:'+self.link
        if self.title: print 'title:'+self.title
        if self.price: print 'price:'+self.price
        if self.surface: print 'surface:'+self.surface
        if self.hasPictures: print 'hasPictures:'+str(self.hasPictures)
        if self.isPro: print 'isPro:'+str(self.isPro)
        if self.city: print 'city:'+self.city
        if self.postalCode: print 'postalCode:'+self.postalCode
        if self.state: print 'state:'+self.state
        if self.nbrRooms: print 'nbrRooms:'+self.nbrRooms
        if self.ges: print 'ges:'+self.ges
        if self.ces: print 'ces:'+self.ces
        if self.m2price: print 'm2price:'+str(self.m2price)

    def keys(self):
        return ['link','title','price','surface','hasPictures','isPro','city','postalCode', 'state','nbrRooms','ges','ces','m2price']

    def item(self):
        return {'link':self.link.encode("UTF-8"),'title':self.title.encode("UTF-8"),'price':self.price,'surface':self.surface,'hasPictures':self.hasPictures,'isPro':self.isPro,'city':self.city.encode("UTF-8"),'postalCode':self.postalCode, 'state':self.state.encode("UTF-8"),'nbrRooms':self.nbrRooms,'ges':self.ges.encode("UTF-8"),'ces':self.ces.encode("UTF-8"),'m2price':self.m2price}
