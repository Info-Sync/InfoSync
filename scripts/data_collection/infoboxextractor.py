import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import time
import wikipediaapi
import sys
import re
from collections import OrderedDict
import random
import json
from json2html import *
import matplotlib.pyplot as plt


# A function to return the BeautifulSoup of a website given its url

def get_bs(url):
    try:
        website_url = requests.get(url).text
        soup = BeautifulSoup(website_url,'lxml')
        return soup
    except:
        try:
            website_url = requests.get(url).text
            soup = BeautifulSoup(website_url,'lxml')
            return soup
        except:
            try:
                website_url = requests.get(url).text
                soup = BeautifulSoup(website_url,'lxml')
                return soup
            except:
                website_url = requests.get(url).text
                soup = BeautifulSoup(website_url,'lxml')
                return soup


#NOW ABSOLETE.

#An Older function to check if a page had an infobox. Has been replaced by a better function.

def check_if_infobox(link):
    soup = get_bs(link)
    if len(soup.findAll(class_="infobox"))==0 and len(soup.findAll(class_='infobox_v2'))==0 and len(soup.findAll(class_='infobox_v3'))==0 and len(soup.findAll(class_='toccolours')) == 0:
        return True
    return False

#A function which returns a list of csv files in the current directory
def get_csv():    
    csv_files = [pos_csv for pos_csv in os.listdir('/content/drive/MyDrive/Info_Sync') if pos_csv.endswith('.csv')]
    return csv_files
#check_if_infobox()

# A list of languages we work with on this project
lang = [
    "en","de", "fr", "es", "nl", "ar", "hi", "zh", "ko", "ru", "tr", "af","ceb","sv"
]

# The classes in which infoboxes are contained
classes = ["infobox","infobox_v2","infobox_v3","toccolours"] 

#A function to find the link of a page in another language
def get_link(title,link,language):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    if(language=="en"):
        return link
    else:
        try:
            return wiki_wiki.page(title).langlinks[language].fullurl
        except:
            return "empty"

# A set of simple functions used to perform preliminary processing.
def remove_small(soup):
    for a in soup.findAll('span',{'id':"coordinate"}):
        a.decompose()
    return soup

def remove_reference(soup):
    for sup in soup.find_all("sup", {'class':'reference'}): 
        sup.decompose()
    return soup

def remove_hreftags(soup):
    for a in soup.findAll('a'):
        a.replaceWithChildren()
    return soup

def remove_italics(soup):
    for i in soup.findAll('i'):
        i.replaceWithChildren()
    return soup


def delete_css(soup):
    #for tag in soup.findAll(True):
    #    for attr in [attr for attr in tag.attrs]:
    #        del tag[attr]
    for data in soup(['style']):
        # Remove tags
        data.decompose()
    for line in soup.findAll('hr'):
        line.decompose()
    return soup

def clean_stack(stack):
    #clean=stack
    clean=[]
    count=0
    for word in stack:
        if(clean_string(str(word))!=""):
            if(count!=0):
                clean.append("|")
            clean.append(clean_string(str(word)))
            count+=1
    s = " "
    for word in clean:
        #print(word)
        if(s[-1]!=" "):
            s = s+ " "+word
        else:
            s = s+word
    if(s.isspace()==False):
        #print(s[1:])
        return(s[1:])
    else:
        return ""

    
def clean_string(string):
    filter_arr=['\n','\xa0','\u200b','•']
    s2=""
    for char in string:
        if(char not in filter_arr):
            s2=s2+char
        else:
            s2 = s2+" "
    s2 = re.sub(' +', ' ',s2)
    if(s2.isspace()==False and len(s2)>=1):
        while(s2[-1]==":" or s2[-1]=="：" or s2[-1]==" "):
            s2= s2[:-1]
            if(len(s2)<1):
                break
        return s2
    else:
        return ""

def clean_stack_col(stack):
    #clean=stack
    clean=[]
    for word in stack:
        if(clean_string_col(str(word))!=""):
            clean.append(clean_string_col(str(word)))
    s = " "
    for word in clean:
        #print(word)
        if(s[-1]!=" "):
            s = s+ " "+word
        else:
            s = s+word
    if(s.isspace()==False):
        #print(s[1:])
        return(s[1:])
    else:
        return ""    

def clean_string_col(string):
    filter_arr=['\n','\xa0','\u200b','•']
    s2=""
    for char in string:
        if(char not in filter_arr):
            s2=s2+char
        else:
            s2 = s2+" "
    s2 = re.sub(' +', ' ',s2)
    if(s2.isspace()==False and len(s2)>=1):
        return s2
    else :
        return ""
def find_colon(string):
    try:
        i = len(string)
        while(string[i-1]==" " or string[i-1]=="\n"):
            i=i-1
        if(string[i-1]==":" or string[i-1]=="："):
            return True
        return False
    except:
        return False
    
def remove_timeline(soup):
    for div in soup.findAll(id='Timeline-row'):
        div.decompose()
    return soup

def push(arr,string1,string2):
    #print(string1)
    try:
        for element in arr:
            if(element[0]==string1):
                string1 = string1.encode('utf-8')+' '+prev_header_arr[-1].encode('utf-8')
                break
        arr.append([string1,string2])
    except:
        return
        #print(len(arr))
        #print(string1)
def check(soup):
    soup = remove_timeline(soup)
    soup = remove_italics(soup)
    stack = []
    global prev_header_arr
    prev_header_arr=[]
    prev_header=""
    global arr
    arr = []
    for tr in soup.findAll('tr'):
        if(len(tr.findAll(class_='plainlinks wikidata-link'))!=0):
            continue
        if(len(tr.findAll('td'))==1 and len(tr.findAll('th'))==0):
            if(len(tr.find('td').findAll('b'))!=0):
                prev_header = clean_stack(tr.find('td').find('b').findAll(text=True))
                prev_header_arr.append(prev_header)
                continue
        if(len(tr.findAll('td'))==2 and len(tr.findAll('th'))==0):
            if(len(tr.find('td').findAll('b'))!=0):
                push(arr,clean_stack(tr.find('td').find('b').findAll(text=True)),clean_stack(tr.findAll('td')[1].findAll(text=True)))
                continue
            elif('font-weight:bold' in str(tr.find('td'))):
                push(arr,clean_stack(tr.find('td').findAll(text=True)),clean_stack(tr.findAll('td')[1].findAll(text=True)))
                continue
        if(len(tr.findAll('td'))==2 and len(tr.findAll('th'))==0 and find_colon(tr.find('td').find(text=True))==True):
            push(arr,clean_stack(tr.find('td').findAll(text=True)),clean_stack(tr.findAll('td')[1].findAll(text=True)))
            print
            stack = []
        elif(len(tr.findAll('th'))==1 and len(tr.findAll('td'))==1):
            if(clean_string(prev_header)!="" and len(clean_stack(stack))!=0):
                push(arr,clean_string(prev_header),clean_stack(stack))
            push(arr,clean_stack(((tr.find('th').findAll(text=True)))),clean_stack(tr.find('td').findAll(text=True)))
            stack = []
            prev_header=""
        
        elif(len(tr.findAll('th'))==1 and len(tr.findAll('td'))==0):
            if(prev_header!="" and len(clean_stack(stack))!=0):
                push(arr,clean_string(prev_header),clean_stack(stack))
            prev_header=clean_stack(tr.find('th').findAll(text=True))
            prev_header_arr.append(prev_header)
            stack=[]
        
        else:
            for td in tr.findAll('td'):
#                 if(len(clean_stack(stack))>=1):
#                      stack.append(" | ")
                if(len(td.findAll('img'))==0):
                    stack.append(clean_stack(td.findAll(text=True)))
    if(prev_header!="" and len(clean_stack(stack))!=0):
        push(arr,clean_string(prev_header),clean_stack(stack))
    return arr     

def de_ms(soup):
    arr=[]
    for tr in soup.findAll('tr'):
        if(len(tr.findAll('td'))==2):
            arr.append([clean_stack(tr.findAll('td')[0].findAll(text=True)),clean_stack(tr.findAll('td')[1].findAll(text=True))])
    return arr

def ru_animal(soup):
    arr = []
    soup = remove_italics(soup)
    for tr in soup.findAll('tr'):
        if(clean_stack_col(tr.findAll(text=True)).count(':')>5):
            split_arr = []
            for element in tr.findAll(text=True):
                if(clean_string(element)!=""):
                    split_arr.append(clean_string(element))
            for i in range(0,len(split_arr)):
                if i%2==1:
                    arr.append([clean_string(split_arr[i-1]),clean_string(split_arr[i])])
            tr.decompose()
            break
    return [arr,soup]

#A function, which given a url returns the infobox on that page.
#It returns the infobox as a BeautifulSoup object. 
#If there is no infobox it returns an empty string.

def get_table(url):
    if(url=="empty"):
        return ""
    soup = get_bs(url)
    fl=0
    for cl in classes:
        if (soup.find(class_=cl)) !=None:
            soup = soup.find(class_=cl)
            fl=1
            break
    if(fl==0):
        return ""
    soup = remove_hreftags(soup)
    soup = remove_small(soup)
    soup = remove_reference(soup)
    return soup



def removech(title):
    arr = [
        "(",
        ")",
        "/",
        "&",
        "/",
        ":",
        ">",
        "'",
        "?",
        "*"
    ]
    s=""
    for char in title:
        if char in arr:
            continue
        else:
            s=s+char
    if(s[-1]=='.'):
        return s[:-1]
    return s

def open_table(location):
    file = open(location,'r', encoding='utf-8')
    soup = BeautifulSoup(file.read(),'lxml')
    soup = delete_css(soup)
    #soup = remove_divs(soup)
    #soup = remove_empty(soup)
    #soup = remove_single(soup)
    return soup

def checker(soup,language,csv):
    for el in soup.findAll(style="display:none"):
        el.decompose()
    if(language=='ru' and (csv == "Animal.csv" or csv == "Food.csv") ):
        arr1 = ru_animal(soup)[0]
        arr2 = check(ru_animal(soup)[1])
        for element in arr2:
            arr1.append(element)
        return arr1
    if(language=='de' and (csv == "Movie.csv" or csv=="Shows.csv" or csv=="Medicine.csv")):
        arr1 = de_ms(soup)
        arr2 = check(soup)
        for element in arr2:
            arr1.append(element)
        return(arr1)
    return(check(soup))

def json_from_arr(arr):   
    diction = {}
    json_object=""
    for element in arr:
        diction[element[0]]=element[1]
        json_object = json.dumps(diction, indent = 4,ensure_ascii=False)
    return json_object

def convert_to_json(address,lang,csv):
    soup = open_table(address)
    arr = checker(soup,lang,csv)
    return(json_from_arr(arr))

def store_json(orig):
    sl = orig.split("/")
    json_file= convert_to_json(orig,sl[-2],sl[2])
    os.system("mkdir an/html/"+sl[2])
    os.system("mkdir an/html/"+sl[2]+"/"+sl[3])
    os.system("mkdir an/html/"+sl[2]+"/"+sl[3]+"/"+sl[4])
    os.system("mkdir an/json/"+sl[2])
    os.system("mkdir an/json/"+sl[2]+"/"+sl[3])
    os.system("mkdir an/json/"+sl[2]+"/"+sl[3]+"/"+sl[4])
    file = open("an/json/"+orig[12:],"w")
    file.write(json2html.convert(json = json_file))
    file.close()

def store_json_all(orig):
    s1 = orig.split("/")
    json_file = convert_to_json(orig, s1[-2], s1[2])
    file = open("tables/json/"+topic.name+"/"+n.name+"/"+language+"/table.html","w",encoding ="utf8")
    file.write(json2html.convert(json=json_file))
    file.close()

# for topic in os.scandir("tables/html"):
#     for n in os.scandir("tables/html/"+topic.name):
#         for language in lang:
#             # os.makedirs("./tables/json/"+topic.name+"/"+n.name+"/"+language)
#             store_json_all("tables/html/"+topic.name+"/"+n.name+"/"+language+"/table.html")




