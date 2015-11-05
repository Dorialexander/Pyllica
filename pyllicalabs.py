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


#A global function to clean the text using several regex
def regex(textfile):
	file = open(textfile, 'r')
	myFile = file.read()
	chainecomplete = re.sub(r'Rappel de votre demande.*%\. ', r'', myFile) #withdrawing the first part of span
	chainecomplete = re.sub(r'</span>', r'', chainecomplete) #withdrawing the ending part of span
	chainecomplete = re.sub(r'<br/>', r'\n', chainecomplete) #replacing <br/> with effective line feeds
	chainecomplete = re.sub(r'(\b- +\n)(\s+)', r'\2', chainecomplete) #merging the hyphens at the ending part of the column
	chainecomplete = re.sub(r'(\b- +)(\s+)', r'\2', chainecomplete) #merging the hyphens followed by a space
	chainecomplete = re.sub(r'\n(?!\n)', r'', chainecomplete) #transforming paragraphs into a single line of text
	chainecomplete = re.sub(r'<div(.+)>', r'', chainecomplete) #withdrawing remaining some html markers
	chainecomplete = re.sub(r'</div>', r'', chainecomplete) #withdrawing remaining other html markers
	chainecomplete = re.sub(r'\n', r'\n\n', chainecomplete) #single line feed becomes double line feeds for easier reading
	funfile = open(textfile, 'w') #opening the file in write mode
	funfile.write(chainecomplete) #replacing the content with new cleaned content
	
#A function to get the content of an url and publishing it in a new file
def openurl(url, textfile):
        page=urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        pressyear=soup.get_text()
        pressbottom=str(pressyear)
        with open(textfile, 'w') as myFile:
                myFile.write(pressbottom)

#the main function to deal with daily newspaper in the calendar mode of gallica
def textpress(url, title="titre", year=1900, month=1, day=1, item=5, rate=1, lastpage=1):
        firstdate = pressdate(year, month, day, rate, item)
        for date in firstdate:
                textfile = title + "_" + date + ".txt"
                firsturl = url + date
            #get the real url after the redirection
                response = urllib.request.urlopen(firsturl)
                endurl = "/f1n" + str(lastpage) + ".texteBrut"
                realurl = response.geturl()
                finalurl = realurl + endurl
            #get the file with bs4
                try:
                        openurl(finalurl, textfile)
                except urllib.error.URLError as e:
                    if hasattr(e, 'reason'):
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                    elif hasattr(e, 'code'):
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                else:
                        openurl(finalurl, textfile)
                        regex(textfile)
