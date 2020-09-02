import logging, gensim, os

def get_raw_text(path, html=False):
    """
    Extracts text from the notes
    """
    if html:
                
    else:
        raw_text = {}
        articles = os.listdir(path)
        for number, art in enumerate(articles):
            with open(path+art) as arhivo:
                raw_text[number] = archivo.read()
        return raw_text


if __name__ =='__main__':

    logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s",
                        datefmt= '%H:%M:%S', level=logging.INFO)
                  


    TRAIN_PATH_LN = "./datos_clase_03/la_nacion_data/articles_data/"

    articles = os.listdir(TRAIN_PATH_LN)
