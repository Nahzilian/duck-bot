import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import numpy
from collections import Counter

stopwords = stopwords.words('english')
stemmer = LancasterStemmer()

def sentence_processing(sentence):
    tokenized = word_tokenize(sentence)
    tokenized = [stemmer.stem(x) for x in tokenized if x not in r" \"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~" and x != '' and x not in stopwords]
    print(tokenized)
    return tokenized

def define_tag(msg):
    docs_no = 2
    msg_counts = Counter(msg)
    print(res_counts)
    print(msg_counts)

def test():
    # Load in the knowledge base of a conversation
    define_tag(a)


test()