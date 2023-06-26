import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import time
# import wikipediaapi
import sys 
import os
import re
import json
from collections import OrderedDict
import random
import json
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer,util
from scipy.spatial import distance

from infoboxextractor import *

#A function which returns a dataframe of painting data scraped from a wikipedia list

def painting():
    website_url = requests.get('https://en.wikipedia.org/wiki/Wikipedia:Featured_pictures/Artwork/Paintings').text
    soup = BeautifulSoup(website_url,'lxml')

    soup.find('ul').findAll('a')

    Titles=[]
    Links=[]
    for a in soup.find('ul').find_all(lambda t: t.name == 'a' and t.get_text(strip=True) != ''):
        Titles.append(a.get('title'))
        Links.append("https://en.wikipedia.org"+a.get('href'))
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

#A function which returns a dataframe of movie data scraped from a wikipedia list

def movie():
    website_url = requests.get("https://en.wikipedia.org/wiki/List_of_films_considered_the_best").text
    soup = BeautifulSoup(website_url,'lxml')
    hrefs= []
    for i in soup.findAll('i'):
        if(i.findAll('a')!=[]):
            hrefs.append(i.findAll(lambda t: t.name == 'a' and t.get_text(strip=True) != ''))
    Titles=[]
    Links=[]
    count = 0
    for link in hrefs:
        count+=1
        Titles.append(link[0].get('title'))
        Links.append("https://en.wikipedia.org"+link[0].get('href'))
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df


#A function which returns a dataframe of animal data scraped from a wikipedia list

def animal():
    soup = get_bs('https://en.wikipedia.org/wiki/List_of_animal_names')
    table = soup.findAll('table',{'class':'wikitable sortable'})

    Titles=[]
    Links=[]
    for i in range(0,2):
        for link in table[i].findAll('a'):
            if link.get('href')[:5]=="/wiki":
                Titles.append(link.get('title'))
                Links.append("https://en.wikipedia.org"+link.get('href'))
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

#A function which returns a dataframe of planet data scraped from a wikipedia list

def planet():
    soup = get_bs('https://en.wikipedia.org/wiki/List_of_multiplanetary_systems')
    table = soup.find('table',{'class':'toccolours sortable wikitable'})

    df = pd.read_csv('Planet.csv')
    Titles=np.array(df['title'])
    Links=np.array((df['link']))

    for link in table.findAll('a'):
        if link.get('href')[:5]=="/wiki":
            if link.get('title') in Titles:
                pass
            else:
                Titles=np.append(Titles,link.get('title'))
                Links=np.append(Links,"https://en.wikipedia.org"+link.get('href'))
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

#A function which returns a dataframe of Book data scraped from a wikipedia list

def book_extra():
    soup = get_bs('https://en.wikipedia.org/wiki/List_of_best-selling_books')
    Titles=[]
    Links=[]
    num = []
    table_counter = 0
    for table in soup.find_all(class_="wikitable"):
        for tr in table.findAll('tr'):
            try:
                if(len(tr.find('td').findAll('a'))>0):
                    a = tr.find('td').find('a')
                    #print(a)
                    if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                        count = 0
                        for language in lang:

                            if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                                count+=1
                        if(count>=5):
                            table_counter+=1
                            print(a.get('title'))
                            Titles.append(a.get('title'))
                            Links.append("https://en.wikipedia.org"+a.get('href'))
            except (TypeError,AttributeError):
                continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    print(table_counter)
    return df

#A function which returns a dataframe of Musician data scraped from a wikipedia list

def musician_extra():
    soup = get_bs('https://en.wikipedia.org/wiki/List_of_artists_who_reached_number_one_in_the_United_States')
    df = pd.read_csv('Musician.csv')
    Titles=df['title']
    Links=df['link']
    tit = []
    link = []
    num = []
    table_counter = 0
    for a in soup.find_all(lambda t: t.name == 'a' and t.get_text(strip=True) != '')[56:500]:
        #print(a)
        try:
            if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                if("https://en.wikipedia.org"+a.get('href') not in Links):
                    #print(a)
                    count = 0
                    for language in lang:

                        if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                            count+=1
                    if(count>=5):
                        table_counter+=1
                        print(a.get('title'))
                        Titles = Titles.append(a.get('title'))
                        tit.append(a.get('title'))
                        Links = Links.append("https://en.wikipedia.org"+a.get('href'))
                        link.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError):
                continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    print(table_counter)
    return df

#A function which returns a dataframe of Athlete data scraped from a wikipedia list

def athlete_extra():
    soup = get_bs('https://en.wikipedia.org/wiki/List_of_multiple_Olympic_gold_medalists')
    Titles=[]
    Links=[]
    num = []
    table_counter = 0
    for table in soup.find_all(class_="wikitable"):
        for tr in table.findAll('tr'):
            try:
                if(len(tr.find('td').findAll('a'))>0):
                    a = tr.find('td').find('a')
                    #print(a)
                    if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                        count = 0
                        for language in lang:

                            if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                                count+=1
                        if(count>=5):
                            table_counter+=1
                            print(a.get('title'))
                            Titles.append(a.get('title'))
                            Links.append("https://en.wikipedia.org"+a.get('href'))
            except (TypeError,AttributeError):
                continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    print(table_counter)
    return df

def company():
    Titles=[]
    Links=[]
    num = []
    soup = get_bs("https://en.m.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue")
    table_counter = 0
    for tr in soup.find(class_="wikitable").findAll('tr'):
        try:
            #print(tr)
            if(len(tr.findAll('td')[1].findAll('a'))>0):
                a = tr.findAll('td')[1].find('a')
                #print(a)
                if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                    count = 0
                    for language in lang:

                        if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                            count+=1
                    if(count>=5):
                        table_counter+=1
                        print(a.get('title'))
                        Titles.append(a.get('title'))
                        Links.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError,IndexError):
            continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

def University_Germany():
    Titles=[]
    Links=[]
    num = []
    soup = get_bs("https://en.wikipedia.org/wiki/List_of_universities_in_Germany")
    table_counter = 0
    for a in soup.findAll('a')[72:130]:
        try:        
            if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                    count = 0
                    for language in lang:

                        if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                            count+=1
                    if(count>=5):
                        table_counter+=1
                        print(a.get('title'))
                        Titles.append(a.get('title'))
                        Links.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError,IndexError):
            continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

def University_QS():
    Titles=[]
    Links=[]
    num = []
    soup = get_bs("https://en.wikipedia.org/wiki/QS_World_University_Rankings")
    table_counter = 0
    for tr in soup.findAll(class_="wikitable")[1].findAll('tr')[1:]:
        try:
            #print(tr)
            if(len(tr.findAll('td')[0].findAll('a'))>0):
                a = tr.findAll('td')[0].findAll('a')[1]
                #print(a)
                if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                    count = 0
                    for language in lang:

                        if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                            count+=1
                    if(count>=5):
                        table_counter+=1
                        print(a.get('title'))
                        Titles.append(a.get('title'))
                        Links.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError,IndexError):
            continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

def Nobel():
    Titles=[]
    Links=[]
    table_counter = 0
    soup = get_bs("https://en.wikipedia.org/wiki/List_of_Nobel_laureates")
    for a in soup.find(class_="wikitable").findAll('a')[8:200]:
        try:
            if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                    count = 0
                    for language in lang:

                        if(str(get_table(get_link(a.get('title'),"https://en.wikipedia.org"+a.get('href'),language)))!=""):
                            count+=1
                    if(count>=5):
                        table_counter+=1
                        print(a.get('title'))
                        Titles.append(a.get('title'))
                        Links.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError,IndexError):
            continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

def oscar():
    soup = get_bs("https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films")
    Titles=[]
    Links=[]
    table_counter = 0
    for tr in soup.find(class_="wikitable").findAll('tr'):
        try:
            #print(tr)
            if(len(tr.findAll('td')[0].findAll('a'))>0):
                a = tr.findAll('td')[0].find('a')
                #print(a)
                if(a.get('href')[:5]!="https" and a.get('title')[-6:]!="exist)"):    
                    table_counter+=1
                    print(a.get('title'))
                    Titles.append(a.get('title'))
                    Links.append("https://en.wikipedia.org"+a.get('href'))
        except (TypeError,AttributeError,IndexError):
            continue
    df = pd.DataFrame()
    df['title']=Titles
    df['link']=Links
    return df

def food():
    df = pd.read_csv("Food.csv")
    Titles = []
    Links = []
    table_counter=0
    for i in range(0,100):
        try:
            title = df['title'][i]
            link = df['link'][i]
            count = 0
            for language in lang:
                if(str(get_table(get_link(title,link,language)))!=""):
                    count+=1
            if(count>=5):
                table_counter+=1
                print(title)
                Titles.append(title)
                Links.append(link)

        except (TypeError,AttributeError,IndexError):
            continue
    print(table_counter)
    df = pd.DataFrame()
    df['title'] = Titles
    df['link'] = Links
    return df

def book_extra():
    df = pd.read_csv("books_extra.csv")
    Titles = []
    Links = []
    table_counter=0
    for i in range(0,18):
        try:
            title = df['title'][i]
            link = df['link'][i]
            count = 0
            for language in lang:
                if(str(get_table(get_link(title,link,language)))!=""):
                    count+=1
            if(count>=5):
                table_counter+=1
                print(title)
                Titles.append(title)
                Links.append(link)

        except (TypeError,AttributeError,IndexError):
            continue
    print(table_counter)
    df = pd.DataFrame()
    df['title'] = Titles
    df['link'] = Links
    return df

def Medicine():
    df = pd.read_csv("Medicine.csv")
    Titles = []
    Links = []
    table_counter=0
    for i in range(0,55):
        try:
            title = df['title'][i]
            link = df['link'][i]
            count = 0
            for language in lang:
                if(str(get_table(get_link(title,link,language)))!=""):
                    count+=1
            if(count>=5):
                table_counter+=1
                print(title)
                Titles.append(title)
                Links.append(link)

        except (TypeError,AttributeError,IndexError):
            continue
    print(table_counter)
    df = pd.DataFrame()
    df['title'] = Titles
    df['link'] = Links
    return df

def Diseases():
    df = pd.read_csv("Diseases.csv")
    Titles = []
    Links = []
    table_counter=0
    for i in range(0,699):
        try:
            title = df['title'][i]
            link = df['link'][i]
            count = 0
            for language in lang:
                if(str(get_table(get_link(title,link,language)))!=""):
                    count+=1
            if(count>=5):
                table_counter+=1
                print(title)
                Titles.append(title)
                Links.append(link)

        except (TypeError,AttributeError,IndexError):
            continue
    print(table_counter)
    df = pd.DataFrame()
    df['title'] = Titles
    df['link'] = Links
    return df