from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from collections import Counter
import json
import unicodedata

def getAuthor(author):
    '''
    Get the main Raptxt page for that author (String).
    '''
    #Create a request object
    url = 'http://www.raptxt.it/testi_artista/'+author
    headers = {
        'User-Agent' : r'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    } 
    request = Request(url, None, headers)
    
    #Make the request
    data = urlopen(request).read()
    soup = BeautifulSoup(data, "html.parser")
    
    #Return the HTML page with all the links
    return soup

def isFeat(div):
    '''
    Return True if the div contains the word "feat", otherwise False.
    '''
    return 'feat' in div.get_text()

def getLinks(soup, author):
    '''
    Given a Author-soup (BeautifulSoup) extract all the non featuring songs links. Return a list.
    '''
    
    divs = soup.find_all('div')
    links = []
    
    #Only keep songs:
    # a. That are not feat
    # b. That are in author's albums
    #Then extract links and store them into an array
    for div in divs:
        if not isFeat(div):
            array_a = div.find_all('a')
            for a in array_a:
                if a.get('href')[0:6+len(author)] == 'testi/'+author:
                    links.append(a.get('href'))
                    
    return links

def cleanString(string):
    cleaned_string = string.replace('<p>','').replace('</p>','').replace('<br/>','') \
        .replace('\n',' ').replace('\r','').replace('’',' ').replace(',',' ')\
        .replace("'",' ').replace("(",'').replace(")",'').replace("!",'')\
        .replace("“",'').replace("”",'').replace("?",'').replace("‘",'')\
        .replace("#",'').replace("\"",'').replace(".",'').replace('-','')\
        .replace('*','').replace('&amp;','').replace("/","").replace("+","")\
        .replace("%","").replace("[","").replace("]","")
    return cleaned_string

def getLyrics(link):
    '''
    Given a link return the lyrics
    '''
    #Create a request object
    url = 'http://www.raptxt.it/'+link
    headers = {
        'User-Agent' : r'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
    } 
    request = Request(url, None, headers)
    
    #Make the request
    data = urlopen(request).read()
    soup = BeautifulSoup(data, "html.parser")
    lyrics = soup.find_all("section", class_="testo")[0].p
    clean_lyrics = cleanString(str(lyrics).lower())
    
    #Return the HTML page with all the links
    return clean_lyrics    

if __name__ == "__main__":
    #Specify the author(s)
    author = "marracash"
    
    #Get the main HTML page
    txt = getAuthor(author)
    
    #Parse the HTML page and extract links
    links = getLinks(txt, author)
    
    #Iterate the links and extract lyrics
    lyrics = ''
    for link in links:
        lyrics = getLyrics(link)+" "+lyrics
    
    #First link
    #lyrics = getLyrics(links[4])
    print(lyrics)
    
    results = Counter(lyrics.split(" "))
    #print(json.dumps(results, sort_keys = True, indent = 4, ensure_ascii=False))
    print(json.dumps(sorted(results.items(), key=lambda item: item[1]), indent = 4, ensure_ascii=False))