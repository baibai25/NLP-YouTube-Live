import argparse
from polyglot.detect import Detector
import pandas as pd
from collections import Counter

class Lang_Detector():
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.load_data()
    
    def load_data(self):
        with open(self.data_path, 'r', encoding='utf_8') as f:
            data = [i.rstrip('\n') for i in f]

        return data

    def detect_lang(self):
        result = []
        for line in self.data:
            lang = Detector(line, quiet=True).language.name
            result.append([line, lang])

        self.save(result)
    
    def save(self, result):
        result = pd.DataFrame(result)
        print(Counter(result[1]))
        result.to_csv('lang.csv', index=False, header=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='Dataset path')
    args = parser.parse_args()
    data_path = args.data
    data = Lang_Detector(data_path)
    data.detect_lang()
