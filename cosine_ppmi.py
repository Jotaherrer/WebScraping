import urllib, requests
import numpy as np
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
            if note % 100 == 0:
                print(f'Printing note number: {note}')
        except:
            continue
    return codes


def get_text(html_dictionary):
    """
    Gets text from HTML code which is the interview posted on the newspaper.
    """
    content = {}
    for n, code in html_dictionary.items():
        soup = BeautifulSoup(code, 'lxml')
        try:
            print(f'Begin printing {n}')
            text = soup.find_all('section',id='cuerpo')
            text = text[0].find_all('p') 
            print(f'succesfully processed {n} with id == cuerpo')
        except IndexError:
            try:
                print(f'Begin printing {n}')
                text = soup.find_all('div', class_='cuerpo__nota')
                text = text[0].find_all('p') 
                print(f'succesfully processed {n} with class == cuerpo__nota')
            except:
                continue
        text = [texto.text.strip() for texto in text]
        text = ','.join(text).strip()
        text = text.replace('\r\n', ' ')
        text = text.replace("\'","")
        text = text.replace('[R]','')
        text = text.replace('(...)',".")
        text = text.replace('.,', '.')
        text = text.replace(' , ', '')        
        text = ' '.join(text.split())
        content[str(n)] = text            
    return content


def tokenize(text):
    """
    Tokenizes a text that is included as an argument in the function.
    """
    sentence = sent_tokenize(text)
    tokens = []
    for e in sentence:
        for w in word_tokenize(e):
            if (w == '.') | (w == ',') | (w == '(') | (w == ')') | (w == '...') | (w == '....') | (w == '-') | (w == ';') | (w == '?') | (w == "''") | (w == "..") | (w == "%") | (w == "!") | (w == ".....") | (w == "+") | (w == "$") | (w == ":") | (w == '10') | (w == '1') | (w == '100') | (w == '15') | (w == '2') | (w == '20') | (w == '3') | (w == '4') | (w == '5') | (w == '40') | (w == '6') | (w == '30'):
                pass
            else:
                tokens.append(w)
    return tokens


def gen_co_ocurrencies_matrix(all_texts, window):
    """
    Generates a co-ocurrencies matrix to determine how many times a word of the context
    appears near a target word. Params:
    - all_texts: dictionary with keys with note number and value with text.
    - window: range for which I'll compute the window size
    """
    matrix = {}

    for i, text in enumerate(all_texts.values()):
        tokens = tokenize(text)
        for j in range(len(tokens)):
            target = tokens[j]
            if target not in matrix:
                matrix[target] = {}
            for t in tokens[max(0, j-window):(min(j+window, len(tokens)-1)+1)]:
                matrix[target][t] = matrix[target].get(t, 0) + 1
            matrix[target][target] -= 1

        row_sums = {text: sum(matrix[text].values()) for text in matrix}
        total_sum = sum(row_sums.values())

    final_dict = {'co_ocurrencies': matrix,
                  'row_sums': row_sums,
                  'total_sum': total_sum}
    
    return final_dict


def cosine_dist(t1,t2,matrix):
    '''
    Calculates cosine distance or similarity between words.
    '''
    tokens = list(matrix['co_ocurrencies'].keys())
    v1 = np.array([matrix['co_ocurrencies'][t1].get(e, 0) for e in tokens])
    v2 = np.array([matrix['co_ocurrencies'][t2].get(e, 0) for e in tokens])
    res = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return res


def estimate_ppmi(t1,t2,matrix):
    '''
    Estimates PPMI (Positive Pointwise Mutual Information)
    '''
    num = matrix["co_ocurrencies"][t1].get(t2, 0)
    den1 = matrix["row_sums"].get(t1, 0)
    den2 = matrix["row_sums"].get(t2, 0)
    total = matrix["total_sum"]  
    result = 0 if not num else max(np.log2(num * total / (den1 * den2)), 0)
    return result


if __name__ == "__main__":
    ### DESCARGA DE DATOS - DIARIO LA NACION
    last_note_number = 2436886    # Ultimo ID de nota de LN
    number_pages = 10
    htmls = html_code(number_pages)
    textos = get_text(htmls)

    ### TOKENS & CO-OCURRENCIES MATRIX
    texto_prueba = textos['2400002']
    token_prueba = tokenize(texto_prueba)
    token_matrix = gen_co_ocurrencies_matrix(textos, window=6)
    
    ### COSINE-DISTANCE & PPMI
    cosine_dist("amor", "soledad", token_matrix)
    estimate_ppmi('amor', 'soledad', token_matrix)
    cosine_dist("amor", "sexo", token_matrix)
    estimate_ppmi('amor', 'sexo', token_matrix)
    cosine_dist("novia", "Cristiano", token_matrix)
    estimate_ppmi('novia', 'Cristiano', token_matrix)
    cosine_dist("Cristiano", "Georgina", token_matrix)
    estimate_ppmi('Cristiano', 'Georgina', token_matrix)