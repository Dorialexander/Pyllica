Pyllica
=======

Pyllica est un outil écrit en Python permettant de récupérer des documents hébergés sur la bibliothèque numérique 
<a href="http://gallica.bnf.fr/">Gallica</a>. Il permet notamment de constituer rapidement de grands corpus afin d'effectuer des analyses assistées par ordinateur (statistique textuelles, text mining, reconnaissance d'image).

Initialement écrit par Pierre-Carl Langlais il a été très largement mis à jour et complété par Julien Schuh. La dernière version tire notamment partie de nouvelles fonctionnalités introduites sur Gallica, telles que l'extraction des pdf ou l'extraction des images. Auparavant, Pyllica ne fonctionnait que sur des documents <a href="https://en.wikipedia.org/wiki/Optical_character_recognition">OCRisés</a>). À l'occasion de cette mise à jour, le programme a été également réécrit en Python 3 (la version d'origine était en Python 2.7).

<h3>Installation et usage</h3>

Pyllica est un programme en Python 3, qui fait appel à l'extension <em>beautiful soup</em> (<a href="http://www.crummy.com/software/BeautifulSoup/)">plus d'informations par ici</a>). Pour l'utilisez vous devez avoir une version de Python à jour (cf. les recommandations officielles pour une installation sous <a href="https://docs.python.org/3/using/windows.html">Windows</a>, <a href="https://docs.python.org/3/using/mac.html">Mac</a> et <a href="https://docs.python.org/3/using/unix.html">Linux</a>) et télécharger Beautiful Soup.

Pyllica se compose de quatre outils:
- Pyllicalabs permet d’extraire les fichiers en texte brut de numéros de périodiques qui ont été océrisés, selon une fourchette définie par l'utilisateur;
- Pyllicalabspdf permet d’extraire les pdf de numéros de périodiques;
- Pyllicalabsjpg permet d’extraire les pages d’un document sous forme de fichier jpg, tif ou png, avec une qualité définie par l’utilisateur;
- Pyllicalabsjpgpress permet de faire la même opération pour des numéros de périodiques.

Pour chacun des outils, il y a deux fichiers: un fichier contenant le programme, et un fichier d’instruction (commençant par le mot « action »). Pour utiliser un outil, il suffit de placer les deux fichiers dans un nouveau dossier et de modifier le fichier d’instruction en fonction des livres ou périodiques que l’on veut télécharger. Sous Mac, s’il y a des problèmes d’encodage du texte au moment de l’utilisation des outils, il ne faut pas cliquer sur le fichier d’instruction pour le lancer mais démarrer IDLE depuis depuis le Terminal ($ idle3) et faire Fichier > Ouvrir pour lancer l’action.

<h3>Pyllicalabs</h3>
On modifie le contenu du fichier actionpyllicalabs:

```python
textpress(url="http://gallicalabs.bnf.fr/ark:/12148/cb32817642h/date", title="lemoderniste", year=1889, month=5, day=25, item=52, rate=7, lastpage=11)
```

La fonction comprend les commandes suivantes :<br/>
url: on indique l’adresse sur Gallica de la page du périodique indiquant toutes les années disponibles.<br/>
title: on choisit un titre qui sera indiqué dans le nom du fichier.<br/>
year, month, day: la date du premier numéro qu’on souhaite télécharger.<br/>
item: le nombre de fichiers qu’on veut récupérer.<br/>
rate: le nombre de jours entre chaque numéro.<br/>
lastpage: avec la nouvelle version de Gallica, la numérotation des pages n’est pas importante, on peut laisser cet élément tel quel.<br/>

La dernière version de Julien Schuh intègre des règles en cas d’exception: si l’outil ne trouve pas un des numéros (par exemple, si le périodique n’est pas disponible pour une des dates), un message avertit du problème mais le téléchargement des numéros suivants continue.

<h3>Pyllicalabspdf</h3>
Comme l’outil précédent, il permet de récupérer les fichiers pdf de périodiques; la méthode d’utilisation est la même.

<h3>Pyllicalabsjpg</h3>
La nouvelle version de Gallica utilise la norme IIIF, permettant de récupérer les images en haute résolution.
Pour l'utiliser avec un document unique, il suffit de récupérer l'identifiant du document dans l'adresse de gallicalabs (ce qui suit ark:), par exemple: /12148/btv1b86000454/

On insère ces chiffres (en conservant bien les slash) dans le fichier actionpyllicalabspg.py au niveau de la variable "identifier", on choisit un titre ("title") pour les fichiers de sortie et on sélectionne la première et la dernière page (attention, il faut choisir en fonction des numéros des vues et non de la pagination réelle du document). On place ce fichier et le fichier pyllicalabs3jpg.py dans le dossier de destination et on le lance avec Python.

On peut changer la résolution souhaitée en modifiant la fin de l'url dans le fichier pyllicalabsjpg.py (par exemple, full/5000/0/native.jpg au lieu de full/3000/0/native.png). On peut aussi récupérer les images au format png ou tif en remplaçant la mention « jpg » par « png » ou « tif » à la fin de l'adresse et du format de fichier créé:

```python
for page in listpage:
        jpgfile = title + "_" + str(page) + ".png"
        url = 'http://gallicalabs.bnf.fr/iiif/ark:' + identifier + '/f' + str(page) + '/full/3000/0/native.png'
        urllib.request.urlretrieve(url, jpgfile)
```

<h3>Pyllicalabsjpgpress</h3>
Pour récupérer les images d’une série de numéros de périodiques, on part de l’adresse du périodique avec les dates: http://gallicalabs.bnf.fr/ark:/12148/cb34427442r/date et on supprime la fin de l'adresse "/date" pour l'intégrer dans le fichier actionpyllicalabsjpgpress.py dans la variable « url ».

Il faut ici tenir compte de la pagination; on peut gonfler le nombre de pages au cas ou certains documents comportent plus de pages, les erreurs s'afficheront dans le shell avant que le programme ne continue avec le numéro suivant du périodique. Par exemple, pour un journal de 8 pages, il vaut mieux indiquer 12 pages pour être certain que des numéros plus longs seront entièrement téléchargés.
