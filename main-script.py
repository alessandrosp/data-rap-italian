from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from collections import Counter
import json
import unicodedata
import random
import time

tic = time.clock()
print(tic)

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
    author = author.replace("+","_")
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
    print("Step 1")
    authors = ["baby+k",
               "caparezza",
               "emis+killa",
               "noyz+narcos",
               "club+dogo",
               "kaos",
               "gemitaiz",
               "madman",
               "canesecco",
               "fabri+fibra",
               "coez",
               "gue+pequeno",
               "jake+la+furia",
               "er+costa",
               "clementino",
               "fedez",
               "marracash",
               "lowlow",
               "rocco+hunt",
               "salmo",
               "nitro",
               "truceboys",
               "bassi+maestro",
               "gemelli+diversi",
               "mondo+marcio",
               "articolo+31",
               "j+ax",
               "ensi",
               "raige",
               "lord+madness",
               "huga+flame",
               "caneda",
               "ghemon",
               "space+one",
               "briga",
               "dj+gruff",
               "sottotono",
               "metal+carter",
               "lucci",
               "mezzosangue",
               "inoki",
               "nesli",
               "colle+der+formento",
               "piotta",
               "luche",
               "santo+trafficante",
               "moreno",
               "two+fingerz",
               "entics",
               "babaman",
               "jesto",
               "danti",
               "achille+lauro",
               "joe+cassano",
               "maxi+b",
               "gente+de+borgata",
               "duke+montana",
               ]
    print("Step 2")
    results = {}
    total_words = {}
    print("Step 3")
    for author in authors:
        print("Step 4")
        #Get the main HTML page
        txt = getAuthor(author)
        print("Step 5")
        #Parse the HTML page and extract links
        links = getLinks(txt, author)
        print("Step 6")
        #Iterate the links and extract lyrics
        lyrics = ''
        for link in links:
            lyrics = getLyrics(link)+" "+lyrics
        print("Step 7")    
        words = lyrics.split(" ")
        #while len(words) < 35000:
        #    lyrics = lyrics+" "+lyrics
        #    words = lyrics.split(" ")
        if len(words) >= 10000:
            sampled_words = random.sample(words, 10000)     
            count_words = Counter(sampled_words)
            results[author] = len(count_words)
            total_words[author] = len(words)
        else:
            results[author] = "NA"
            total_words[author] = len(words)
        print("Just completed: "+author.replace("+"," ").title())
    #print(json.dumps(results, sort_keys = True, indent = 4, ensure_ascii=False))
    #print(json.dumps(sorted(results.items(), key=lambda item: item[1]), indent = 4, ensure_ascii=False))
    #print(len(words))
    #print(len(sampled_words))
    #print(len(results))
    print("Last Step")
    print("")
    print("Unique words:") #PLEASE FIND A WAY TO SORT!
    for key, value in results.items():
        print(key.replace("+"," ").title()+" : "+str(value))
    
    print("")
    print("Total words:")    
    for key, value in total_words.items():
            print(key.replace("+"," ").title()+" : "+str(value))        
        
    toc = time.clock()
    ex_time = toc - tic
    print(ex_time)