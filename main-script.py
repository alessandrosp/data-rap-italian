from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    #Specify the author(s)
    author = "marracash"
    
    #Get the main HTML page
    txt = getAuthor(author)
    
    #Parse the HTML page and extract links
    links = getLinks(txt, author)