# Ref.
# http://watagassy.hatenablog.com/entry/2018/10/06/002628

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import argparse


class Scraping():
    
    def __init__(self, target_url, options):
        self.target_url = target_url
        self.options = options
        self.next_url = self.get_source()

    def get_source(self):
        dict_str = ""
        next_url = ""

        # get html source and live_chat_replay URL
        html = requests.get(self.target_url)
        soup = BeautifulSoup(html.text, "html.parser")

        for iframe in soup.find_all("iframe"):
            if("live_chat_replay" in iframe["src"]):
                next_url = iframe["src"]

        return next_url

    def get_comment(self):
        comment_data = []

        while(1):
            try:
                # get next comment url
                driver = webdriver.Chrome(options=self.options, executable_path="/usr/bin/chromedriver")
                driver.get(self.next_url)
                soup = BeautifulSoup(driver.page_source,"lxml")
                driver.quit()

                # find "script"
                for scrp in soup.find_all("script"):
                    if "window[\"ytInitialData\"]" in scrp.text:
                        dict_str = scrp.text.split(" = ")[1]

                # convert javascript format 
                dict_str = dict_str.replace("false","False")
                dict_str = dict_str.replace("true","True")

                # convert to dictionary
                dict_str = dict_str.rstrip("  \n;")
                dics = eval(dict_str)

                # next live_chat_replay url
                # "https://www.youtube.com/live_chat_replay?continuation="
                continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
                self.next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
                
                # get comment data
                for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
                    try:
                        comment_path = samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]
                        comment_path = str(comment_path["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"])+"\n"
                        comment_data.append(comment_path)
                    except:
                        pass
            except:
                break
        
        self.save(comment_data)

    
    def save(self, comment_data):
        # save
        with open("comment_data1.txt", mode='w', encoding="utf-8") as f:
            f.writelines(comment_data)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL')
    args = parser.parse_args()
    target_url = args.url

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-desktop-notifications')
    options.add_argument("--disable-extensions")
    options.add_argument('--blink-settings=imagesEnabled=false')

    data = Scraping(target_url, options)
    data.get_comment()
    
