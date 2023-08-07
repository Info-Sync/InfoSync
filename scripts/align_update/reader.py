import numpy as np
from bs4 import BeautifulSoup
import os
import re

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
        #print(word)Midgley developed feron12, which was quickly commercialized as a refrigerant for refrigerators and air conditioners.


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
    soup = BeautifulSoup(file.read(),'html.parser')
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