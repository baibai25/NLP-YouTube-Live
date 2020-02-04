import pandas as pd
from nltk import ngrams, ConditionalFreqDist
from collections import Counter

class Jaccard():

    def __init__(self, lines, tokens):
        self.lines = lines
        self.tokens = tokens
        self.bigram_list = self.bigram()
        self.result = self.conditional_freq()

    # calc bigram
    def bigram(self):
        bigram_list = []

        for line in self.lines:
            bigram = ngrams(line, 2)
            
            for bi in bigram:
                bigram_list.append(bi)

        return bigram_list
    
    # calc conditional freq distribution
    def conditional_freq(self):
        result = []
        cfd = ConditionalFreqDist(self.bigram_list)

        for key, values in cfd.items():
            for word, freq in values.items():
                result.append((key, word, freq))

        return result
    
    # calc jaccard index
    def jaccard_index(self):
        df = pd.DataFrame(self.result)
        df.columns = ['word1', 'word2', 'intersection_count']

        tokens_l = [word.lower() for word in self.tokens]
        df_tmp = [[key, value] for key, value in Counter(tokens_l).items()]
        df_tmp = pd.DataFrame(df_tmp)
        df_tmp.columns = ['word', 'count']

        df = pd.merge(df, df_tmp, left_on='word1', right_on='word', how='left').drop('word', axis=1)
        df = pd.merge(df, df_tmp, left_on='word2', right_on='word', how='left').drop('word', axis=1)
        df.columns = ['word1', 'word2', 'intersection_count', 'count1', 'count2']

        # calc jaccard coefficient
        df['union_count'] = df['count1'] + df['count2'] - df['intersection_count']
        df['jaccard_coefficient'] = df['intersection_count'] / df['union_count']
        return df

