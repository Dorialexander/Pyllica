from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import re
import os

#Initiating the function for retrieving the date id of gallica
def pressdate(year, month, day, rate, item):
        finallist=[]
        monthbissex=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        monthunbissex=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        counting=1
        curmonth=month-1
        initialday = '%02d' % day
        initialmonth = curmonth+1
        initialmonth = '%02d' % initialmonth
        initialresult = str(year) + str(initialmonth) + str(initialday)
        finallist.append(initialresult)
        if year%4==0 and not year%100==0:
                while(counting<item):
                        day+=rate
                        counting+=1
                        if day>monthbissex[curmonth]:
                                day = day-monthbissex[curmonth]
                                curmonth+=1
                        if curmonth==12:
                                year+=1
                                curmonth=0
                        finalmonday = '%02d' % day
                        finalmonth = curmonth+1
                        finalmonth = '%02d' % finalmonth
                        finalresult = str(year) + str(finalmonth) + str(finalmonday)
                        finallist.append(finalresult)
        else:
                while(counting<item):
                        day+=rate
                        counting+=1
                        if day>monthunbissex[curmonth]:
                                day = day-monthunbissex[curmonth]
                                curmonth+=1
                        if curmonth==12:
                                year+=1
                                curmonth=0
                        finalmonday = '%02d' % day
                        finalmonth = curmonth+1
                        finalmonth = '%02d' % finalmonth
                        finalresult = str(year) + str(finalmonth) + str(finalmonday)
                        finallist.append(finalresult)
        return finallist


#the main function to deal with daily newspaper in the calendar mode of gallica
def pdfpress(url, title="titre", year=1900, month=1, day=1, item=5, rate=1):
        firstdate = pressdate(year, month, day, rate, item)
        for date in firstdate:
                pdffile = title + "_" + date + ".pdf"
                firsturl = url + date
            #request the url of the redirection
                response = urllib.request.urlopen(firsturl)
                endurl = ".pdf"
                realurl = response.geturl()
                finalurl = realurl + endurl
            #save file
                try:
                        urllib.request.urlopen(finalurl)
                except urllib.error.URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                        urllib.request.urlretrieve(finalurl, pdffile)
             
