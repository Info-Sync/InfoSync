from infoboxextractor import *

def download_tables(csv_name):    
    csv = csv_name
    for x in get_csv()[:1]:
        df = pd.read_csv(csv)
        print(csv)
        os.system("mkdir data/tables/html")
        os.system("mkdir data/tables/html/"+csv[:-4])
        for i in range(38,125):
            title = df['title'][i]
            titlespl = title.split(" ")
            title=""
            for word in titlespl:
                title=title+word
            title=removech(title)
            count=0
            for language in lang:
                if(str(get_table(get_link(df['title'][i],df['link'][i],language)))!=""):
                    count+=1
                    if(count>=5):
                        print(title)
                        break
            if(count>=5):
                os.system("mkdir data/tables/html/"+csv[:-4]+"/"+title)
                for language in lang:
                    try:
                        os.system("mkdir data/tables/html/"+csv[:-4]+"/"+title+"/"+language)
                        file = open("data/tables/html/"+csv[:-4]+"/"+title+"/"+language+"/table.html","w")
                        file.write(str(get_table(get_link(df['title'][i],df['link'][i],language))))
                    except (TypeError,AttributeError):
                            print('failed at '+"data/tables/html/"+csv[:-4]+"/"+title+"/"+language+"/table.html")
                            file = open("data/tables/html/"+csv[:-4]+"/"+title+"/"+language+"/table.html","w")
                            file.write("")


def open_table(location):
    file = open(location,'r')
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


def main():
    for csv_file in os.listdir("data/csv_data"):
        download_tables(csv_file)

if __name__ == "__main__":
    main()
