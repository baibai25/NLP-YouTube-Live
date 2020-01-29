# Ref.
# http://watagassy.hatenablog.com/entry/2018/10/06/002628
# http://watagassy.hatenablog.com/entry/2018/10/08/132939

from bs4 import BeautifulSoup
import requests
import argparse
from itertools import repeat


class Scraping():
    
    def __init__(self, target_url):
        self.target_url = target_url
        self.next_url = self.get_source()

    def get_source(self):
        next_url = ''
        
        # get html source and live_chat_replay URL
        html = requests.get(self.target_url)
        soup = BeautifulSoup(html.text, 'html.parser')

        for iframe in soup.find_all('iframe'):
            if('live_chat_replay' in iframe['src']):
                next_url = iframe['src']

        return next_url

    def get_comment(self):
        comment_data = []
        session = requests.Session()
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
        
        for _ in repeat(None):
            # get next comment url
            html = session.get(self.next_url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')

            # find 'script'
            for scrp in soup.find_all('script'):
                if 'window[\"ytInitialData\"]' in scrp.text:
                    dict_str = scrp.text.split(' = ')[1]

            # convert javascript format
            dict_str = dict_str.replace('false', 'False')
            dict_str = dict_str.replace('true', 'True')

            # convert to dictionary
            dict_str = dict_str.rstrip('  \n;')
            dics = eval(dict_str)

            # next live_chat_replay url
            # 'https://www.youtube.com/live_chat_replay?continuation='
            try:
                continue_url = dics['continuationContents']['liveChatContinuation']['continuations'][0]['liveChatReplayContinuationData']['continuation']
            except:
                # not found url
                break
            else:
                self.next_url = 'https://www.youtube.com/live_chat_replay?continuation=' + continue_url
            
            # get comment data
            for samp in dics['continuationContents']['liveChatContinuation']['actions'][1:]:
                # Normal comment
                try:
                    comment_path = samp['replayChatItemAction']['actions'][0]['addChatItemAction']['item']
                    comment_path = str(comment_path['liveChatTextMessageRenderer']['message']['runs'][0]['text'])+'\n'
                    comment_data.append(comment_path)
                except:
                    pass
                
                # Super Chat comment
                try:
                    comment_path = samp['replayChatItemAction']['actions'][0]['addLiveChatTickerItemAction']['item']
                    comment_path = comment_path['liveChatTickerPaidMessageItemRenderer']['showItemEndpoint']['showLiveChatItemEndpoint']
                    comment_path = str(comment_path['renderer']['liveChatPaidMessageRenderer']['message']['runs'][0]['text'])+'\n'
                    comment_data.append(comment_path)

                except:
                    pass
                    
        self.save(comment_data)

    def save(self, comment_data):
        with open('comment_data.txt', mode='w', encoding='utf-8') as f:
            f.writelines(comment_data)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL')
    args = parser.parse_args()
    target_url = args.url

    data = Scraping(target_url)
    data.get_comment()
    
