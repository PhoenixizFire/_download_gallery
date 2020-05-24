import bs4
from io import BytesIO
import numpy as np
import os.path
import pandas as pd
import PIL
import requests
import shutil
import sys
import tkinter as tk
import tkinter.ttk as ttk
import urllib
from urllib import request
from urllib.parse import urljoin

if getattr(sys, 'frozen', False):
    # frozen
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # unfrozen
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

def make_dir(dirName):
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
        
def fetch_image(image_url,name):
    resp = requests.get(image_url, stream=True)
    local_file = open(name, 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp

def open_page(link):
    request_text = request.Request(url=link,headers=HEADERS)
    html = request.urlopen(request_text).read()
    page = bs4.BeautifulSoup(html, "lxml")
    return page

class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Gallery downloader')
        self.root.configure(background='#888888')
        self.root.geometry('1200x600')
        #self.root.iconbitmap()

        self.mainframe = tk.Frame(self.root).grid(sticky='nsew')

        self.link_here = tk.Label(self.mainframe,text='Enter your link here')
        self.link_here.grid(column=1,row=1)

        self.link = tk.Entry(self.mainframe)
        self.link.grid(column=1,row=2)
        
        self.submit_link = tk.Button(self.mainframe,text='Submit',command=self.access_website)
        self.submit_link.grid(column=1,row=3)

        self.separator = ttk.Separator(self.mainframe,orient='vertical')
        self.separator.grid(column=2,row=0,rowspan=10,sticky='ns')

        self.results = tk.Frame(self.mainframe)
        self.results.grid(column=3,row=0,rowspan=10,columnspan=6,sticky='ns')

        self.code_box = tk.Frame(self.results)
        self.code_box.grid(row=0,rowspan=5,columnspan=6,column=0,sticky='ns')

        self.code = tk.Text(self.code_box,background='black',fg='#00ff00',padx=5,pady=5)
        self.code.grid(row=0,column=0,columnspan=6)

        self.code_bar = tk.Scrollbar(self.code_box,orient='vertical',command=self.code.yview)
        self.code_bar.grid(row=0,column=6,rowspan=5,sticky='ns')

        self.code.config(yscrollcommand=self.code_bar.set)

        self.split = ttk.Separator(self.results,orient='horizontal')
        self.split.grid(row=5,columnspan=6,sticky='ns')

        self.resultat = tk.Canvas(self.results,background='green')
        self.resultat.grid(row=6,rowspan=5,columnspan=6)

    def access_website(self):
        a = self.link.get()
        b = open_page(a)
        print(b)
        self.code.delete('1.0','end')
        self.code.insert('end',b)

    def run(self):
        self.root.mainloop()

if __name__=='__main__':
    App().run()