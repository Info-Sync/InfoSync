from infoboxextractor import *

def download_json():
    for topic in os.scandir("data/tables/html"):
        for n in os.scandir("data/tables/html/"+topic.name):
            for language in lang:
                # os.makedirs("./tables/json/"+topic.name+"/"+n.name+"/"+language)
                store_json_all("data/tables/html/"+topic.name+"/"+n.name+"/"+language+"/table.html")

def main():
    download_json()

if __name__ == "__main__":
    main()