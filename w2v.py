import logging, gensim, os, pickle
from nltk.tokenize import sent_tokenize, word_tokenize


def get_raw_text(html=False):
    """
    Extracts text from the notes from pickle files or .txt files.
    """
    if html:
        raw_text = []
        for i in range(1,5):    
            with open(f'notas_{i}.p', 'rb') as archivo:
                text = pickle.load(archivo)
                raw_text.append(text)
    else:
        raw_text = {}
        path = "./datos_clase_03/la_nacion_data/articles_data/"
        articles = os.listdir(path)
        for number, art in enumerate(articles):
            with open(path+art, encoding='utf-8') as archivo:
                raw_text[number] = archivo.read()
            if number % 1000 == 0:
                print(f'Successfully printed note number {number}')
        return raw_text


def tokenize_newspaper_news(text):
    """
    Tokenization of words included in the news. Returns a list of lists,
    with the words tokenized. The first lists includes every note in the 
    newspaper
    """
    tokens_list = []
    for n, value in text.items():
        sentences = sent_tokenize(value)
        sentences = [word_tokenize(e) for e in sentences if (e != ',') | (e != '.')]
        tokens_list.append(sentences)
        if n % 500 == 0:
            print(f'Sucessfully stored note number {n}')

    sentence_list = []
    for note in tokens_list:
        for sent in note:
            sentence_list.append(sent)
        
    return sentence_list


def word_2_vec_model(raw_sentences, win=5):
    """
    Performs the W2V model with the predeteremined parameters. I left the
    window size of the context as the only parameter of the model to change.
    """
    ### Defining parameters
    model = gensim.models.Word2Vec(size=50,
                                   window=win,
                                   min_count=5,
                                   negative=5,
                                   sample=0.01,
                                   workers=4,
                                   sg=1)
    ### Creating vocabulary
    model.build_vocab(raw_sentences, 
                      progress_per=10000)
    ### Training the model
    model.train(raw_sentences, 
                total_examples=model.corpus_count,
                epochs=20,
                report_delay=1)
    ### Saving model
    model.save('W2V_project.model')
    return model


if __name__ =='__main__':
    logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s",
                        datefmt= '%H:%M:%S', level=logging.INFO)
                  
    train_path_ln = "./datos_clase_03/la_nacion_data/articles_data/"

    ### Collecting data
    data = get_raw_text()
    tokens = tokenize_newspaper_news(data)
    
    ### W2V model - 5 windows
    w2v_model = word_2_vec_model(tokens)
    # Vectores
    w2v_model.__getitem__(['gato'])
    w2v_model.__getitem__(['blanco'])
    # Similarity between words
    w2v_model.wv.similarity('blanco', 'negro')
    w2v_model.wv.similarity('plata', 'negro')
    w2v_model.wv.similarity('Macri', 'presidente')
    w2v_model.wv.similarity('Cristina', 'presidenta')
    # More similar words
    w2v_model.wv.most_similar(positive=['Macri'], topn=10)
    w2v_model.wv.most_similar(positive=['tecnología'], topn=10)
    w2v_model.wv.most_similar(positive=['felicidad'], topn=10)
    w2v_model.wv.most_similar(positive=['miedo'], topn=10)
    w2v_model.wv.most_similar(positive=['trabajo'], topn=10)
    w2v_model.wv.most_similar(positive=['Libre'], topn=10)
    # Analogies
    w2v_model.wv.most_similar(positive=['Queen'], negative=['música'], topn=5)
    w2v_model.wv.most_similar(positive=['Queen', 'música'], topn=5)
    w2v_model.wv.most_similar(positive=['Maradona'], negative=['fútbol'], topn=5)
    # Out of context word
    w2v_model.wv.doesnt_match(['Galicia', 'Frances', 'casa'])
    w2v_model.wv.doesnt_match(['Bolsonaro', 'Trump', 'Biden'])
    

    ### W2V model - 10 windows
    w2v_model_large = word_2_vec_model(tokens, 10)
    # Vectores
    w2v_model_large.__getitem__(['gato'])
    w2v_model_large.__getitem__(['blanco'])
    # Similarity between words
    w2v_model_large.wv.similarity('blanco', 'negro')
    w2v_model_large.wv.similarity('plata', 'negro')
    w2v_model_large.wv.similarity('Macri', 'presidente')
    w2v_model_large.wv.similarity('Cristina', 'presidenta')
    # More similar words
    w2v_model_large.wv.most_similar(positive=['Macri'], topn=10)
    w2v_model_large.wv.most_similar(positive=['tecnología'], topn=10)
    w2v_model_large.wv.most_similar(positive=['felicidad'], topn=10)
    w2v_model_large.wv.most_similar(positive=['miedo'], topn=10)
    w2v_model_large.wv.most_similar(positive=['trabajo'], topn=10)
    w2v_model_large.wv.most_similar(positive=['Libre'], topn=10)
    # Analogies
    w2v_model_large.wv.most_similar(positive=['Queen'], negative=['música'], topn=5)
    w2v_model_large.wv.most_similar(positive=['Queen', 'música'], topn=5)
    w2v_model_large.wv.most_similar(positive=['Maradona'], negative=['fútbol'], topn=5)
    # Out of context word
    w2v_model_large.wv.doesnt_match(['Galicia', 'Frances', 'casa'])
    w2v_model_large.wv.doesnt_match(['Bolsonaro', 'Trump', 'Biden'])
    