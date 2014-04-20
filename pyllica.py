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

#A global function to clean the text using several regex
def regex(textfile, sep1, sep2):
	file = open(textfile, 'r')
	myFile = file.read()
	chainecomplete = re.sub(r'<span class="PAG_[0-9]+_ST[0-9]+">', r'', myFile) #withdrawing the first part of span
	chainecomplete = re.sub(r'</span>', r'', chainecomplete) #withdrawing the ending part of span
	chainecomplete = re.sub(r'<br/>', r'\n', chainecomplete) #replacing <br/> with effective line feeds
	chainecomplete = re.sub(r'(\b- +\n)(\s+)', r'\2', chainecomplete) #merging the hyphens at the ending part of the column
	chainecomplete = re.sub(r'(\b- +)(\s+)', r'\2', chainecomplete) #merging the hyphens followed by a space
	chainecomplete = re.sub(r'\n(?!\n)', r'', chainecomplete) #transforming paragraphs into a single line of text
	chainecomplete = re.sub(r'<div(.+)>', r'', chainecomplete) #withdrawing remaining some html markers
	chainecomplete = re.sub(r'</div>', r'', chainecomplete) #withdrawing remaining other html markers
	chainecomplete = re.sub(r'\n', r'\n\n', chainecomplete) #single line feed becomes double line feeds for easier reading
	if sep1 in chainecomplete:
		head, sep, tail = chainecomplete.partition(sep1)
		enterfile = sep + tail
	else:
		enterfile = "BEGINNING NOT ATTAINED" + chainecomplete
	if sep2 in enterfile:
		head, sep, tail = enterfile.partition(sep2)
		globalfile = head + sep
	else:
		globalfile = enterfile + "END NOT ATTAINED"
	funfile = open(textfile, 'w') #opening the file in write mode
	funfile.write(globalfile) #replacing the content with new cleaned content

#the main function to deal with daily newspaper in the calendar mode of gallica
def textpress(url, title="paper", year=1900, month=1, day=1, item=1, rate=1, firstpage=1, lastpage=1, sep1="", sep2=""):
	firstdate = pressdate(year, month, day, rate, item)
	secondpage = firstpage+1
	lastpage+=1
	listpage = range(secondpage, lastpage)
	for date in firstdate:
		textfile = title + "-" + date + ".txt"
		firstendurl = "/f" + str(firstpage) + ".texte"
		firsturl = url + date + firstendurl
		openurl(firsturl, textfile)
		if (len(listpage)>0):
			for page in listpage:
				endurl = "/f" + str(page) + ".texte"
				otherurl = url + date + endurl
				appendurl(otherurl, textfile)
		regex(textfile, sep1, sep2)

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
	regex(textfile, sep1, sep2)
