import urllib
import requests
from random import randrange
from bs4 import BeautifulSoup

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter

def html_code(n_notes):    
    codes = {}
    for note in range(2400001,2400001+n_notes):
        try:
            url = f'https://www.lanacion.com.ar/{note}'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
            req_result = urllib.request.urlopen(req)
            raw = req_result.read().decode('utf-8')
            clean_url = req_result.geturl()
            codes[str(note)] = raw
            if note % 10 == 0:
                print(f'Printing note number: {note-240000}')
        except:
            pass
    return codes


def get_text(html_dictionary):
    content = {}
    for n, code in html_dictionary.items():
        soup = BeautifulSoup(code, 'lxml')
        try:
            text = soup.find_all('section',id='cuerpo')
            text = text[0].find_all('p') 
        except:
            text = soup.find_all('section', class_='cuerpo__nota')
            text = text[0].find_all('p') 
        text = [texto.text.strip() for texto in text]
        text = ','.join(text).strip()
        text = text.replace('\r\n', ' ')
        text = text.replace('(...)',".")
        text = text.replace('.,', '.')
        text = text.replace(' , ', '')        
        text = ' '.join(text.split())
        content[str(n)] = text            
    return content


if __name__ == "__main__":
    last_note_number = 2436886    # Ultimo ID de nota de LN
    number_pages = 2000
    htmls = html_code(number_pages)
    # test note number: 188160
    textos = get_text(htmls)
