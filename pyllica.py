from bs4 import BeautifulSoup
import urllib2
import re
import os

#Defining the main old french newspaper (so that we don't need to search their url on gallica)
lesdebats = "http://gallica.bnf.fr/ark:/12148/cb39294634r/date" #The "Journal des debats"
lapresse = "http://gallica.bnf.fr/ark:/12148/cb34448033b/date" #The "Presse"
letemps = "http://gallica.bnf.fr/ark:/12148/cb34431794k/" #The "Temps"
lefigaro = "http://gallica.bnf.fr/ark:/12148/cb34355551z/date" #The "Figaro"
leconstitutionnel = "http://gallica.bnf.fr/ark:/12148/cb32747578p/date" #The "Constitutionnel"
lesiecle = "http://gallica.bnf.fr/ark:/12148/cb32868136g/date" #The "Siecle"
lematin = "http://gallica.bnf.fr/ark:/12148/cb328123058/date" #The "Matin"
lepetitjournal = "http://gallica.bnf.fr/ark:/12148/cb32895690j/date" #The "Petit Journal"

#Initiating the function to retrieve the date id of gallica
def pressdate(year, month, day, ranging, item):
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
			day+=ranging
			counting+=1
			if day>monthbissex[curmonth]:
				day = day-monthbissex[curmonth]
				curmonth+=1
			finalmonday = '%02d' % day
			finalmonth = curmonth+1
			finalmonth = '%02d' % finalmonth
			finalresult = str(year) + str(finalmonth) + str(finalmonday)
			finallist.append(finalresult)
	else:
		while(counting<item):
			day+=ranging
			counting+=1
			if day>monthunbissex[curmonth]:
				day = day-monthunbissex[curmonth]
				curmonth+=1
			finalmonday = '%02d' % day
			finalmonth = curmonth+1
			finalmonth = '%02d' % finalmonth
			finalresult = str(year) + str(finalmonth) + str(finalmonday)
			finallist.append(finalresult)
	return finallist

#A function to get the content of an url and publishing it in a new file
def openurl(url, textfile):
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	pressyear=soup.find('div',{'id':'modeTexte'})
	pressbottom=str(pressyear)
	with open(textfile, 'w') as myFile:
		myFile.write(pressbottom)

#A function to get the content of an url and appending it in to an existent file
def appendurl(url, textfile):
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	pressyear=soup.find('div',{'id':'modeTexte'})
	pressbottom=str(pressyear)
	with open(textfile, 'a') as myFile:
		myFile.write(pressbottom)

#A function to clean the text using several regex
def regex(textfile):
	file = open(textfile, 'r')
	myFile = file.read()
	chaineTriee = re.sub(r'<span class="PAG_[0-9]+_ST[0-9]+">', r' ', myFile) #withdrawing the first part of span
	chainebientriee = re.sub(r'</span>', r' ', chaineTriee) #withdrawing the ending part of span
	chaineclarifiee = re.sub(r'<br/>', r'\n', chainebientriee) #replacing <br/> with effective line feeds
	chaineparfaite = re.sub(r'\b-( +)\n\s+', r'', chaineclarifiee) #merging the hyphens at the ending part of the column
	chaineachevee = re.sub(r'\n(?!\n)', r'', chaineparfaite) #transforming paragraphs into a single line of text
	chainerelevee = re.sub(r'<div(.+)>', r'', chaineachevee) #withdrawing remaining some html markers
	chaineaboutie = re.sub(r'</div>', r'', chainerelevee) #withdrawing remaining other html markers
	chainecomplete = re.sub(r'\n', r'\n\n', chaineaboutie) #single line feed becomes double line feeds for easier reading
	funfile = open(textfile, 'w') #opening the file in write mode
	funfile.write(chainecomplete) #replacing the content with new cleaned content

#the main function to deal with daily newspaper in the calendar mode of gallica
def textpress(url, title, year, month, day, item, ranging, firstpage, lastpage):
	firstdate = pressdate(year, month, day, ranging, item)
	secondpage = firstpage+1
	lastpage+=1
	listpage = range(secondpage, lastpage)
	for date in firstdate:
		textfile = title + "-" + date + ".txt"
		firstendurl = "/f" + str(firstpage) + ".texte"
		firsturl = url + date + firstendurl
		openurl(firsturl, textfile)
		if (len(listpage)>1):
			for page in listpage:
				endurl = "/f" + str(page) + ".texte"
				otherurl = url + date + endurl
				appendurl(otherurl, textfile)
		regex(textfile)

#the main function to deal with ordinary books or works
def textbook(url, title, firstpage, lastpage):
	secondpage = firstpage+1
	lastpage+=1
	listpage = range(secondpage, lastpage)
	textfile = title + ".txt"
	endurl3 = "/f" + str(firstpage) + ".texte"
	firsturl = url + endurl3
	openurl(firsturl, textfile)
	if (len(listpage)>1):
		for page in listpage:
			endurl = "/f" + str(page) + ".texte"
			otherurl = url + endurl
			appendurl(otherurl, textfile)
	regex(textfile)
