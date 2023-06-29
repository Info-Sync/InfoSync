from infoboxextractor import *

def get_main_arr(topic):
    main_arr = []

    for language in lang:
        count_dict = {}
        value_dict = {}
        print(language)
        names = os.listdir("data/tables/json/"+topic)
        print(len(names))
        count = 0
        for name in names:
            # if count % 50 ==0:
            #     print(count)
            count=count+1
            if(name[-3:]=="(1)"):
                continue
            jsp = []
            if(language=="en"):
                try:
                    t1 = checker(open_table("data/tables/json/"+topic+"/"+name+"/"+"en"+"/table.html"),"en",topic+".csv")
                except KeyboardInterrupt:
                    exit(0)
                except:
                    print(name)
                    continue
            else:
                try:
                    t1 = checker(open_table("data/tables/json/"+topic+"/"+name+"/"+language+"/final_translations.html"),"en",topic+".csv")
                    t2 = checker(open_table("data/tables/json/"+topic+"/"+name+"/"+language+"/table.html"),language,topic+".csv")
                except KeyboardInterrupt:
                    exit(0)
                except:
                    print(name)
                    continue

            for i in range (0,len(t1)):
                en_key = t1[i][0].lower()
                en_value = t1[i][1].lower()
                try:
                    if(language!="en"):
                        orig_key = t2[i][0].lower()
                        orig_value = t2[i][1].lower()
                        #print("\n\n"+orig_key+"\n"+orig_value+"\n\n")
                except:
                    #print(t2[i])
                    continue
                try:
                    if(language=="en"):
                        count_dict[en_key][0]=count_dict[en_key][0]+1
                        value_dict[en_key].append(en_value)
                    else:
                        count_dict[orig_key][0]=count_dict[orig_key][0]+1
                        found=0
                        for index, pair in enumerate(count_dict[orig_key][1:]):
                            if pair[0]==en_key:
                                pair[1]=pair[1]+1
                                found=1
                        if not found:
                            count_dict[orig_key].append([en_key,1])

                except KeyError:
                        if(language=="en"):
                            count_dict[en_key]=[1]
                            value_dict[en_key]=[en_value]
                        else:
                            count_dict[orig_key]=[1]
                            if en_key not in count_dict[orig_key]:
                                count_dict[orig_key].append([en_key,1])


        arr= []
        for key in count_dict:
            arr.append(([key]+count_dict[key]))
            #if(language=="ar"):
            #    print(([key]+count_dict[key])[1])
        arr.sort(key = lambda x: (-x[1],-x[1]))
        main_arr.append(arr)
    return main_arr


def convert_main_to_work(threshold,main_arr):
    main_to_work=[]
    for arr in main_arr:
        to_work_arr = [i for i in arr if i[1]>=threshold]
        main_to_work.append(to_work_arr)
    # for arr in main_to_work:
    #     print(arr)
    return main_to_work


def remove_brackets(stri):
    stri = stri.replace('(', "")
    stri = stri.replace(')', "")
    return stri


def create_dictionary(main_to_work,threshold):
    fin_dict = []
    temp_dict = []
    for i in range(0,len(main_to_work[0])):
        fin_dict.append({"en":[(main_to_work[0][i])]})
        temp_dict.append([remove_brackets(main_to_work[0][i][0])])
    for i in range(1,14):
        print(lang[i])
        for index,word_to_align in enumerate(main_to_work[i]):
            aligned = False
            mx_num = max([x[1] for x in word_to_align[2:]])
            # print("Dealing with "+str(word_to_align))
            main_to_work_modified=[]
            if mx_num>=20:
                words_mapped = []
                for x in word_to_align[2:]:
                    if x[1] >= 15:
                        words_mapped.append(remove_brackets(x[0]))
                        main_to_work_modified.append(x)
            else:
                for x in word_to_align[2:]:
                    if x[1] == mx_num:
                        words_mapped.append(x[0])
                        main_to_work_modified.append(x)
            # print("Words mapped are "+str(words_mapped))
            to_comp = sbert_model.encode(words_mapped)
            for id,temp_dict_row in enumerate(temp_dict):
                # print("Checking with "+str(temp_dict_row))
                emb = sbert_model.encode(temp_dict_row)
                emb_calc = util.cos_sim(to_comp,emb)
                if(emb_calc.max()>=0.7):

                    # print("Passed")
                    if(len(np.shape(emb_calc))==1):
                        for word_to_add in words_mapped:
                            temp_dict_row.append(word_to_add)
                        if lang[i] not in fin_dict[id].keys():
                            fin_dict[id][lang[i]]=[word_to_align]
                            aligned=True
                        else:
                            fin_dict[id][lang[i]].append(word_to_align)
                    else:
                        tr_count = 0
                        tot_count = 0
                        for wid,word_to_add in enumerate(main_to_work_modified):
                            #if(emb_calc[wid].max()>=0.7):
                            tr_count+=word_to_add[1]*emb_calc[wid].max()
                            tot_count+=word_to_add[1]
                        if(tr_count/tot_count>=0.7):
                            for wid,word_to_add in enumerate(main_to_work_modified):
                                if(emb_calc[wid].max()>=0.7):
                                    temp_dict_row.append(word_to_add[0])
                            if lang[i] not in fin_dict[id].keys():
                                fin_dict[id][lang[i]]=[word_to_align]
                                aligned=True
                            else:
                                fin_dict[id][lang[i]].append(word_to_align)
                # else:
                #     print(emb_calc.max())

            if(aligned == False and word_to_align[1]>=threshold):
                fin_dict.append({lang[i]:[word_to_align]})
                temp_dict.append([])
                for word_to_add in word_to_align[2:]:
                    temp_dict[-1].append(word_to_add[0])
        print(fin_dict)
    return fin_dict
# for i in range(1,14):
#     print(lang[i])
#     for index,word_to_align in enumerate(main_to_work[i]):
#         aligned = False
#         words_mapped = [x[0] for x in word_to_align[2:]]
#         to_comp = sbert_model.encode(words_mapped)
#         for id,temp_dict_row in enumerate(temp_dict):
#             #print(temp_dict_row)
#             emb = sbert_model.encode(temp_dict_row)
#             emb_calc = util.cos_sim(emb,to_comp)
#             if(emb_calc.mean()>=0.80):
#                 for word_to_add in word_to_align[2:]:
#                     temp_dict_row.append(word_to_add[0])
#                 fin_dict[id][lang[i]]=word_to_align
#                 aligned=True
#                 break



def main():
    main_arr = get_main_arr("Musician")
    main_to_work = convert_main_to_work(15,main_arr)

    # for lst in fin_dict:
    #     print(lst)
    # print(main_to_work)

    fin_dict = create_dictionary(main_to_work,20)

if __name__ == "__main__":
    main()
