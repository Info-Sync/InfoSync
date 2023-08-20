import os
import pandas as pd
import reader
import configparser
import argparse
def row_data():
    cols = ["Table","Category"].extend(lang)
    df = pd.DataFrame(columns=cols)
    row_list = []
    for category in list(os.listdir(args.d)):
        for table in os.listdir("%s/%s/"%(args.d,category)):
            row = {}
            for language in lang:
                row[language] = 0
            row["Table"] = table
            row["Category"] = category
            for language in os.listdir("tables/json/"+category+"/"+table+"/"):
                opened_table =  reader.checker(reader.open_table("tables/json/"+category+"/"+table+"/"+language+"/table.html"),language,category+".csv")
                row[language] = len(opened_table)
            row_list.append(row)
    df =  pd.DataFrame(row_list)
    df["Variance"] = df[df.columns[:14]].var(axis=1)
    variance_df = pd.DataFrame(columns = ["Category","Variance","Len"])
    for group, cat_df in df.groupby("Category"):
        variance_df.loc[len(variance_df)] = [group, cat_df["Variance"].mean(),len(cat_df)]

if __name__ == "__main__":
    lang = ["en","es","nl","fr","ru","zh","hi","de","ar","af","ceb","hi","ko","tr"]
    parser = argparse.ArgumentParser()
    parser.add_argument("-d")
    args = parser.parse_args()

    