import numpy as np
from bs4 import BeautifulSoup
import os
from sentence_transformers import SentenceTransformer,util
from scipy.spatial import distance
import torch
import json
import configparser
import argparse
import reader

##Input: 2 Tables
##Output: A list containing [embedding vector of table1, embedding vector of table2] 
def emb_calc(table_1,table_2):
    
    table_1_s = ''.join(table_1)
    table_1_emb=sbert_model.encode(table_1)
    
    table_2_s = ''.join(table_2)

    table_2_emb=sbert_model.encode(table_2)

    return [table_1_emb,table_2_emb]

##Input: The 2 tables and their embedding vectors
##Output: The row vs row cosine distances
def calc_cosine(table_1_emb,table_1,table_2_emb,table_2):
    cosines = []
    cosines = distance.cdist(table_1_emb,table_2_emb,'cosine')
    return cosines

##Input: 2 tables
##Output: 3 different cosine distance metrics based on keys, values, keys+value
def get_cosines(table_1,table_2):
    key_val_1 = []
    key_1 = []
    val_1 = []
    key_val_2 = []
    key_2 = []
    val_2 = []
    
    key_val_1 = [x[0]+":"+x[1] for x in table_1]
    key_1 = [x[0] for x in table_1]
    val_1 = [x[1] for x in table_1]
    
    
    key_val_2 = [x[0]+":"+x[1] for x in table_2]
    key_2 = [x[0] for x in table_2]
    val_2 = [x[1] for x in table_2]

    key_val_1_emb,key_val_2_emb = emb_calc(key_val_1,key_val_2)
    key_1_emb,key_2_emb = emb_calc(key_1,key_2)
    val_1_emb,val_2_emb = emb_calc(val_1,val_2)

    key_val_cos = calc_cosine(key_val_1_emb,table_1,key_val_2_emb,table_2)
    key_cos = calc_cosine(key_1_emb,table_1,key_2_emb,table_2)
    val_cos = calc_cosine(val_1_emb,table_1,val_2_emb,table_2)
    
    return {
        'key_val':key_val_cos,
        'key':key_cos,
        'val':val_cos
    }

def multi_dist(v1,v2):
    v1= v1.replace(".", " ")
    v2 = v2.replace("."," ")
    # print(v1)
    # print(v2)
    v1_emb = sbert_model.encode(v1)
    v2_emb = sbert_model.encode(v2)
    
            
    x = distance.pdist([v1_emb,v2_emb],'cosine')[0]
    # print(x)
    # print()
    return x

"""### Align With Dictionary"""

def align_with_dictionary_new(table1_orig,table2_orig,table1_trans,table2_trans,category,languages):
    cat_dictionary = json.loads("%s/%s"%(open(config["data"]["dictionary_path"],category),"r").read())
    #print(cat_dictionary)
    aligned_t1=[]
    aligned_t2=[]
    al_reason = []
    for row in table1_orig:
        #print("checking for "+row[0])
        aligned=False
        for temp_dict in cat_dictionary:
            if languages[0] in temp_dict.keys() and languages[1] in temp_dict.keys():
                #print(temp_dict)
                for synonym in temp_dict[languages[0]]:
                    #print("comparing with "+synonym[0])
                    if(synonym[0].lower()==row[0].lower()):
                        #print("found" + row[0])
                        for synonym2 in temp_dict[languages[1]]:
                            for row2 in table2_orig:
                                if row2[0].lower()==synonym2[0].lower():
                                    aligned_t1.append(row)
                                    for find_idx in range(0,len(table2_orig)):
                                        if(table2_orig[find_idx]==row2):
                                            aligned_t2.append(table2_orig[find_idx])
                                            break

                                    al_reason.append("Dict")
                                    aligned=True
                                    break
                            if(aligned==True):
                                break
                    if(aligned==True):
                        break
                if(aligned==True):
                    break
    return aligned_t1,aligned_t2 ,al_reason

"""### Alignment Main"""

def alignment_key_dict(table1_orig,table2_orig,table1_trans,table2_trans,category,languages):
    dict_set = eval(config["alignment_params"]["dict_set"])
    KeyBidirectional_threshold = float(config["alignment_params"]["KeyBidirectional_threshold"])
    ValueBidirectional_threshold = float(config["alignment_params"]["ValueBidirectional_threshold"])
    Valueunidirectional_threshold = float(config["alignment_params"]["Valueunidirectional_threshold"])
    Valuemulti_threshold = float(config["alignment_params"]["Valuemulti_threshold"])
    max_multi = int(config["alignment_params"]["max_multi"])
    param_mapping = {
        "dict_set" : dict_set,
        "KeyBidirectional_threshold" : KeyBidirectional_threshold,
        "ValueBidirectional" : ValueBidirectional_threshold,
        "Valueunidirectional_threshold" : Valueunidirectional_threshold,
        "Valuemulti_threshold" : Valuemulti_threshold,
    }
    if config["running"]["ablations"].strip() == "True":
        for key in config["ablations"]:
            if config["ablations"][key].strip() == "True":
                param_mapping[key] = 0
                if key=="dict_set":
                    dict_set=False

    if(len(table1_orig)!=0 and len(table2_orig)!=0):
            try:
                aligned_t1 ,aligned_t2,al_reason=align_with_dictionary_new(table1_orig,table2_orig,table1_trans,table2_trans,category,languages)
            except:
                aligned_t1,aligned_t2,al_reason=[],[],[]
            if not dict_set:
                aligned_t1,aligned_t2,al_reason=[],[],[]
           
            cosines = get_cosines(table1_trans,table2_trans)
            key_cosines = cosines['key']
            val_cosines = cosines['val']
            cosines = cosines['key_val']
           
            aligning_cosine = []
            unaligned_t1 = []
            unaligned_t2 = []
            key_order = np.argsort(key_cosines, axis=1)
            val_order = np.argsort(val_cosines, axis=1)
            order = np.argsort(cosines, axis=1)
            key_orderT = np.argsort(key_cosines.T, axis=1)
            val_orderT = np.argsort(val_cosines.T, axis=1)
            orderT = np.argsort(cosines.T, axis=1)
            
            for table1_row in range(len(table1_trans)):
                ckey_order, cval_order, corder = key_order[table1_row], val_order[table1_row], order[table1_row]
                
                if key_orderT[ckey_order[0]][0] == table1_row and key_cosines[table1_row][ckey_order[0]]<=KeyBidirectional_threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[ckey_order[0]])
                    aligning_cosine.append(key_cosines[table1_row][ckey_order[0]])
                    al_reason.append("Key")
                elif orderT[corder[0]][0] == table1_row and cosines[table1_row][corder[0]]<=ValueBidirectional_threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[corder[0]])
                    aligning_cosine.append(cosines[table1_row][corder[0]])
                    al_reason.append("ValueBidirectional")

                if val_cosines[table1_row][cval_order[0]]<=Valueunidirectional_threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[corder[0]])
                    aligning_cosine.append(val_cosines[table1_row][cval_order[0]])
                    al_reason.append("ValueUnidirectional")

                for multi_idx in range(1,min(max_multi,len(corder))):
                    
                    try:
                        orig_dist = multi_dist(table1_trans[table1_row][1],table2_trans[corder[0]][1])
                        merged_dist = multi_dist(table1_trans[table1_row][1],table2_trans[corder[0]][1]+table2_trans[corder[multi_idx]][1])
                    except ValueError:
                        continue
                    if merged_dist <= Valuemulti_threshold and merged_dist<orig_dist:
                        aligned_t1.append(table1_orig[table1_row])
                        aligned_t2.append(table2_orig[corder[multi_idx]])
                        aligning_cosine.append(val_cosines[table1_row][cval_order[multi_idx]])
                        al_reason.append("Multi")

            
            return {
                'aligned_t1':aligned_t1,
                'aligned_t2':aligned_t2,
                'aligning_cosine':aligning_cosine,
                'unaligned_t1':unaligned_t1,
                'unaligned_t2':unaligned_t2,
                'aligning_reason':al_reason
            }
    return None


def alignment_driver(table_name,category,lang1,lang2):
    
    table1_orig =  reader.checker(reader.open_table("%s/json/%s/%s/%s/table.html"%(config["data"]["datapath"],category,table_name,lang1)),lang1,category+".csv")
    if lang1=="en":
        table1_trans=table1_orig
    else:
        table1_trans = reader.checker(reader.open_table("%s/json/%s/%s/%s/final_translations.html"%(config["data"]["datapath"],category,table_name,lang1)),lang1,category+".csv")
    
    table2_orig = reader.checker(reader.open_table("%s/json/%s/%s/%s/table.html"%(config["data"]["datapath"],category,table_name,lang2)),lang2,category+".csv")
    if lang2=="en":
        table2_trans=table2_orig
    else:
        table2_trans = reader.checker(reader.open_table("%s/json/%s/%s/%s/final_translations.html"%(config["data"]["datapath"],category,table_name,lang2)),lang2,category+".csv")
    
 

    # if len(table2_orig)!=len(table2_trans) or len(table1_orig)!=len(table1_trans):
    #     return None
    

    dc = alignment_key_dict(table1_orig,table2_orig,table1_trans,table2_trans,category,[lang1,lang2])
    
    if dc is None:
        return None

    al_t1=dc['aligned_t1']
    al_t2=dc['aligned_t2']
    unal_t1=dc['unaligned_t1']
    unal_t2=dc['unaligned_t2']
    reason = dc['aligning_reason']

    while(len(unal_t1)<len(unal_t2)):
            unal_t1.append(["",""])
    while(len(unal_t1)>len(unal_t2)):
            unal_t2.append(["",""])
    dict_aligned, key_aligned, vals_aligned, valw_aligned, multi_aligned = [], [], [], [], []


    for i in range(0,len(reason)):
        al_t1[i] = [al_t1[i][0].strip(),al_t1[i][1].strip()]
        al_t2[i] = [al_t2[i][0].strip(),al_t2[i][1].strip()]

        if reason[i] == "Dict":
            dict_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "Key":
            key_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "ValueBidirectional":
            vals_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "ValueUnidirectional":
            valw_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "Multi":
            multi_aligned.extend([[al_t1[i],al_t2[i]]])
    
    complete_alignment = []
    for x in [dict_aligned,key_aligned,vals_aligned,valw_aligned,multi_aligned]:
        if x is not None:
            complete_alignment.extend(x)
    
    return dict_aligned, key_aligned, vals_aligned, valw_aligned, multi_aligned ,complete_alignment, unal_t1, unal_t2,table1_orig, table2_orig


if __name__ == "__main__":
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    sbert_model = SentenceTransformer('stsb-mpnet-base-v2').to(device)
    parser = argparse.ArgumentParser()
    parser.add_argument("-cnf")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.cnf)

    languages = ["en","es","nl","fr","ru","zh","hi","de","ar","af","ceb","hi","ko","tr"]
    eng_x = ["en_es","en_nl","en_fr","en_ru","en_zh","en_hi","en_de","en_ar","en_af","en_ceb","en_hi","en_ko","en_tr"]
    xy = ["fr_ru","fr_de","fr_ko","fr_hi","fr_ar","de_ru","de_ko","de_hi","de_ar","ru_ko","ru_hi","ru_ar","ko_hi","ko_ar","hi_ar"]
    if config["running"]["mode"] == "pair_mode":
        output = {}
        output[config["pair_mode"]["category"]] = {}
        output[config["pair_mode"]["category"]][config["pair_mode"]["table_name"]] = {}
        output[config["pair_mode"]["category"]][config["pair_mode"]["table_name"]]["%s_%s"%(config["pair_mode"]["lang1"],config["pair_mode"]["lang2"])] = {}
        dict_aligned, key_aligned, vals_aligned, valw_aligned, multi_aligned ,complete_alignment, unal_t1, unal_t2,table1_orig, table2_orig = alignment_driver(config["pair_mode"]["table_name"],config["pair_mode"]["category"],config["pair_mode"]["lang1"],config["pair_mode"]["lang2"])
        
        output[config["pair_mode"]["category"]][config["pair_mode"]["table_name"]]["%s_%s"%(config["pair_mode"]["lang1"],config["pair_mode"]["lang2"])] = complete_alignment
        file = open(config["pair_mode"]["dump_file"],"w")
        json.dump(output,file)
        file.close()

    elif config["running"]["mode"] == "dataset_mode":
        output = {}
        for category in os.listdir("%s/json"%(config['dataset_mode']["datapath"])):
            if category not in output:
                output[category] = {}
            for table_name in os.listdir("%s/json/%s"%(config["dataset_mode"]["datapath"],category)):
                if table_name not in output[category]:
                    output[category][table_name] = {}
                if config["dataset_mode"]["languages"] == "ENG_X":
                    langs = eng_x
                else:
                    langs = xy
                for pair in langs:
                    dict_aligned, key_aligned, vals_aligned, valw_aligned, multi_aligned ,complete_alignment, unal_t1, unal_t2,table1_orig, table2_orig = alignment_driver(table_name,category,pair.split("_")[0],pair.split("_")[0])
                    output[category][table_name][pair] = complete_alignment
        file = open(config["dataset_mode"]["dump_file"],"w")
        json.dump(output,file)
        file.close()
