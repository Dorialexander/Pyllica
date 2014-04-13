Pyllica
=======

Pyllica is a small python tool to retrieve the text-version of newspapers in gallica (it works also for books and other single documents)

<h3>Installation and requirements</h3>

It is based on python 2.7.5 and requires the "beautiful soup" module (<href="http://www.crummy.com/software/BeautifulSoup/)">more info</hfre>).

To initiate pyllica, put pyllica.py in the directory where you want to archive the texts and open a new python file (you can also write directly your commands into pyllica.py, but it is much practical this way). It should begins with "from pyllica import *".

A typical command file would look like this :
  from pyllica import *
  textpress(url="http://gallica.bnf.fr/ark:/12148/cb39294634r/date", title="debats", year=1900, month=2, day=28, ranging=1, item=1, firstpage=2, lastpage=2)

On my computer, the download rates was approximately 10-15 pages per minute for newspapers (much quicker for usual books, as pages are lighter and there is less calculus involved). The rate could go higher or lower depending on the efficiency of your laptop the quality of the internet connection.

The tool currently includes two functions, texpress and textbook.

<h3>Textpress</h3>

textpress(url, title, year, month, day, item, ranging, firstpage, lastpage) is an advanced function to deal with newspapers in gallica. It allows to fetch a given number of newspaper, from a startdate. The rate of fetching (one newspaper out of 7, for example) ou the number of pages retrieved can also be customised. 

To use textpress, you have to specify the following information:
*url = url id for the newspaper (for instance, "http://gallica.bnf.fr/ark:/12148/cb34431794k/" for "Le Temps"). The information must be a string (and put into brackets).
*title = title of the retrieved file (preferably the name of the newspaper, but it can be anything). The information must be a string (and put into brackets).
*year = year of the startdate file
*month = month of the startdate file
*day = day of the stardate file
*item = number of newspapers retrieved 
*ranging = rate of fetching. For instance, a ranging of 7, will give you a newspaper every week. This is especially useful if you look for journalistic texts that appears on a non-daily basis (a weekly chronicle…).
*firstpage = the first page you are looking for.
*lastpage = the last page you are looking for. If you only fetch one page, put the same number as firstpage. Till the end of the XIXth century, french newspapers usually cormprises 4 pages: if you are looking for the whole newspaper lastapage=4 should do the trick.

If I want to get the first two pages of all the issues published on monday of the "journal des débats" of the year 1862, you can use the following :

textpress(url="http://gallica.bnf.fr/ark:/12148/cb39294634r/date", title="lesdebats", year=1862, month=1, day=6, ranging=7, item=52, firstpage=1, lastpage=2)

pyllica also provindes you an index of the gallica url of the mains french newspaper archived in gallica.

<h3>Textbook</h3>

textbook(url, title, firstpage, lastpage) is a much simpler function than textpress. It allows you to get a set of pages from any document on gallica.

To use textbook, you have to specify the following information:
*url = url id for the book. The information must be a string (and put into brackets).
*title = title of the retrieved file (preferably the name of the book, but it can be anything). The information must be a string (and put into brackets).
*firstpage = the first page you are looking for.
*lastpage = the last page you are looking for. If you only fetch one page, put the same number as firstpage.

<h3>Future development</h3>

I'm planning to do the following things:
*Rewriting the code for older version of python (and using regex to avoid the installation of beautiful soup).
*Adding a new function to retrieve a predefined number of issues of periodicals (like this one : ).
*Adding a set of functions to deal with image and pdf versions (an adaptation of the fine script of Phe for Wikisource for python might seem nice).
*Adding gallica metadata to the retrieved files (authors, editors and so forth…).
*Developing of repository of section separators for several old french newspapers, so that the content of a specific section can be retrieved. I've made up a function to fetch all the business sections of the "Journal des débats" in the 1860s: the results were not perfect (one issue out of two were properly retrieved), as this function relies on excellent OCR recognition. This is still an improvement from all-manual processes.
