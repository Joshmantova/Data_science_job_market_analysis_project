from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import pandas as pd

def init_cleanning_classes():
    stopWords = set(stopwords.words('english'))
    tokenizer_remove_punc = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
    return stopWords, tokenizer_remove_punc, lemmatizer

# stopWords = set(stopwords.words('english'))

# tokenizer_punc = RegexpTokenizer(r'\w+')
# lemmatizer = WordNetLemmatizer()

def get_list_of_descriptions(df, descrip_col_name):
    raw_description = df[descrip_col_name].values
    return raw_description

# raw_description = df_all['Description'].values
# no_punct_descrip_list = [tokenizer_punc.tokenize(descrip) for descrip in raw_description]

def take_out_stopwords_punct(descrip_list, stop_words):
    no_punct_descrip_list = [tokenizer_remove_punc.tokenize(descrip) for descrip in descrip_list]
    word_list_no_stopwords_or_punct = []
    for descrip in no_punct_descrip_list:
        for word in descrip:
            if word.lower() not in stop_words:
                word_list_no_stopwords_or_punct.append(word.lower())
    return word_list_no_stopwords_or_punct

# word_list_no_punc_stopwords = []

# for descrip in no_punct_descrip_list:
#     for word in descrip:
#         if word.lower() not in stopWords:
#             word_list_no_punc_stopwords.append(word.lower())

def lemmatize_word_list(word_list):
    return [lemmatizer.lemmatize(word) for word in word_list]

# lemmatized_cleaned_word_list = [lemmatizer.lemmatize(word) for word in word_list_no_punc_stopwords]

#

def get_wordfreq_dict(word_list):
    freq_dict = dict()
    for word in word_list:
        if word in freq_dict.keys():
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict

# freq = dict()
# for word in lemmatized_cleaned_word_list:
#     if word in freq:
#         freq[word] += 1
#     else:
#         freq[word] = 1

#

def get_term_and_freq_lists(freq_dict):
    sorted_freq_words = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    terms = []
    freq_counts = []
    for term, freq_count in sorted_freq_words:
        terms.append(term)
        freq_counts.append(freq_count)
    return terms, freq_counts

# sorted_freq_words = sorted(freq.items(), key=lambda item: item[1], reverse=True)
# terms = []
# freq_counts = []
# for term, freq_count in sorted_freq_words:
#     terms.append(term)
#     freq_counts.append(freq_count)

#

if __name__ == '__main__':
    df_all = pd.read_csv('../Datasets/df_all_linkedin.csv')
    stopWords, tokenizer_remove_punc, lemmatizer = init_cleanning_classes()
    descrip_list = get_list_of_descriptions(df_all, 'Description')
    word_list_no_stopwords_or_punct = take_out_stopwords_punct(descrip_list, stopWords)
    lemmatized_cleaned_word_list = lemmatize_word_list(word_list_no_stopwords_or_punct)
    word_freq_dict = get_wordfreq_dict(lemmatized_cleaned_word_list)
    terms, freq_counts = get_term_and_freq_lists(word_freq_dict)

    print(terms.index('sql'))
