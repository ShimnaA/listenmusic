from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from time import sleep, ctime
from collections import namedtuple
from threading import Thread



class BandListner():
    def __init__(self):
        self.base_url='https://bandcamp.com/'
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def get_to_bandcamp(self):
        self.browser.get(self.base_url)
        sleep(3)

    def get_track(self):
        discover_section = self.browser.find_element_by_class_name('discover-results')
        left_x = discover_section.location['x']
        right_x = left_x + discover_section.size['width']

        discover_items = self.browser.find_elements_by_class_name('discover-item')
        print("Length of discover_items = {}".format((str(len(discover_items)))))
        tracks = [t for t in discover_items if t.location['x'] >= left_x and t.location['x'] < right_x]
        print("Length of tracks = {}".format((str(len(tracks)))))

        for (i,track) in enumerate(tracks):
            print("[{}]".format(i+1))
            print(track.text)
            lines = track.text.split('\n')
            print("Album : {}".format(lines[0]))
            print("Artist : {}".format(lines[1]))
            if len(lines)>2:
                print("Genre : {}".format(lines[2]))
        sleep(3)

    def catalogue_pages(self):
        '''
        Print the pages that are currently accessible
        '''
        pages = self.browser.find_elements_by_class_name('item-page')
        for page in pages:
            print(page.text)

    def get_page(self, page_num='next'):

        next_button = [e for e in self.browser.find_elements_by_class_name('item-page') if e.text.lower().strip() == str(page_num)]
        if next_button:
            next_button[0].click()
            self.get_track()
        sleep(3)

    def playtrack(self):
        self.browser.find_element_by_class_name('playbutton').click()
        sleep(10)

    def main_logic(self):
        self.get_to_bandcamp()

        #self.get_track()
        #self.playtrack()
        self.catalogue_pages()
        self.get_page(5)
        #self.get_track()
        sleep(3)
        self.browser.quit()


if __name__ == '__main__':
    bot = BandListner()
    bot.main_logic()
