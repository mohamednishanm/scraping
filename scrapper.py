import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from collections import deque

class Crawl():
    def __init__(self, url, key_word) -> None:
        self.new_url = deque([(url, 0)])
        self.all_url_log = open("all_url_log.txt", "w+")
        self.process_urls = set()
        self.key_word = key_word
        self.final_url = open("final_urls.txt", "w+")



    def bfs_url_crawler(self):
        url_count = 0
        stop_flag = 0

        while len(self.new_url) > 0 and not stop_flag:
            if len(self.new_url) > 1000:
                stop_flag = 1
                print("stop flag enabled")
            # pop the url and put all thre nei in th queue
            pop_val = self.new_url.popleft()
            url, cur_level = pop_val
            info = f"url: {url} - depth level: {cur_level}\n"
            self.all_url_log.write(info)
            self.process_urls.add(url)
            
            url_count += 1
           #log writter

            if cur_level > 3:
                print("url out of scope")
                continue

            try:
                response = requests.get(url)
            except:
                print("Broken url - skipping.....")
                continue

            url_parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(url_parts)
            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all("a"):
                local_link = link.get("href")
                if (not local_link
                    or local_link.startswith("/ar")
                    or local_link.startswith("/zh")
                    or local_link.startswith("/es")
                    or local_link.endswith("index")):
                    continue

                if local_link.startswith("/"):
                    local_link = f"{base_url}{local_link}"

                for key in self.key_word:
                    if key in local_link and local_link not in self.process_urls:
                        self.new_url.append((local_link, cur_level+1))
                        self.process_urls.add(local_link)
                        self.final_url.write(f"{local_link}\n")

                        print(local_link,cur_level+1, len(self.new_url))

            
        
        

if __name__ == "__main__":
    url = "https://www.mayoclinic.org/diseases-conditions"
    path_level = ["index"]
    key_word = ["diseases-conditions","symptoms-causes"]

    crawler = Crawl(url, key_word)
    crawler.bfs_url_crawler()
