from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import pandas as pd

def init_cleanning_classes():
    """
    Initiates cleaning classes from NLTK

    :params: 
    
    None

    :returns: 

    stopWords: Set of stopwords in English

    tokenizer_remove_punc: Tokenizer object to remove punctuation from text

    lemmatizer: Lemmatizer object to reduce words to stems
    """
    stopWords = set(stopwords.words('english'))
    tokenizer_remove_punc = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
    return stopWords, tokenizer_remove_punc, lemmatizer

def get_list_of_descriptions(df, descrip_col_name):
    """
    Extracts the list of descriptions from a pandas dataframe

    :params: 

    df: Pandas dataframe that contains descriptions

    descrip_col_name: Name of column that contains descriptions

    :returns:

    raw_description: List of descriptions
    """
    raw_description = df[descrip_col_name].values
    return raw_description

def take_out_stopwords_punct(descrip_list, stop_words):
    """
    Removes stopwords and punctuation from list of descriptions

    :params:

    descrip_list: List of descriptions

    stop_words: Array-like structure containing words to be removed from text

    :returns:

    word_list_no_stopwords_or_punct: List of words with stopwords removed, punctuation removed, and all lowercase
    """
    no_punct_descrip_list = [tokenizer_remove_punc.tokenize(descrip) for descrip in descrip_list]
    word_list_no_stopwords_or_punct = []
    for descrip in no_punct_descrip_list:
        for word in descrip:
            if word.lower() not in stop_words:
                word_list_no_stopwords_or_punct.append(word.lower())
    return word_list_no_stopwords_or_punct

def lemmatize_word_list(word_list):
    """
    Reduces words in word list down to stems (lemmatizes)

    :params:

    word_list: List of words to be lemmatized

    :returns:

    lemmatized_word_list: List of words after being lemmatized
    """
    lemmatized_word_list = [lemmatizer.lemmatize(word) for word in word_list]
    return lemmatized_word_list

def get_wordfreq_dict(word_list):
    """
    Creates a dictionary from a word list in which the keys represent words and the values represent counts of those words

    :params:

    word_list: List of words to create frequency counts from

    :returns:

    freq_dict: Word frequency dictionary
    """
    freq_dict = dict()
    for word in word_list:
        if word in freq_dict.keys():
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict

def get_term_and_freq_lists(freq_dict):
    """
    Creates two linked lists. One list represents the list of terms and the other list represents the corresponding counts of occurances.
    Both lists are ordered such that the most frequently appearing words are first.

    :params:

    freq_dict: Dictionary where the keys represent words and the values represent their frequencies

    :returns:

    terms: List of terms ordered by frequency counts. Highest counts appear first.

    freq_counts: Counts of the occurances of those words
    """
    sorted_freq_words = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    terms = []
    freq_counts = []
    for term, freq_count in sorted_freq_words:
        terms.append(term)
        freq_counts.append(freq_count)
    return terms, freq_counts

if __name__ == '__main__':
    df_all = pd.read_csv('../Datasets/df_all_linkedin.csv')
    stopWords, tokenizer_remove_punc, lemmatizer = init_cleanning_classes()
    descrip_list = get_list_of_descriptions(df_all, 'Description')
    word_list_no_stopwords_or_punct = take_out_stopwords_punct(descrip_list, stopWords)
    lemmatized_cleaned_word_list = lemmatize_word_list(word_list_no_stopwords_or_punct)
    word_freq_dict = get_wordfreq_dict(lemmatized_cleaned_word_list)
    terms, freq_counts = get_term_and_freq_lists(word_freq_dict)

    print(terms.index('sql'))
