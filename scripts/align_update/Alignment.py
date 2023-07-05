
"""### Embedding Calculations"""

def emb_calc(table_1,table_2):
    
    table_1_s = ''.join(table_1)
    table_1_emb=sbert_model.encode(table_1)
    
    table_2_s = ''.join(table_2)

    table_2_emb=sbert_model.encode(table_2)

    return [table_1_emb,table_2_emb]


def calc_cosine(table_1_emb,table_1,table_2_emb,table_2):
    cosines = []
    cosines = distance.cdist(table_1_emb,table_2_emb,'cosine')
    return cosines

def get_cosines(table_1,table_2):
    row_val_1 = []
    row_1 = []
    val_1 = []
    row_val_2 = []
    row_2 = []
    val_2 = []
    for row in table_1:
        row_val_1.append(row[0]+":"+row[1])
        row_1.append(row[0])
        val_1.append(row[1])
    for row in table_2:
        row_val_2.append(row[0]+":"+row[1])
        row_2.append(row[0])
        val_2.append(row[1])
    row_val_1_emb,row_val_2_emb = emb_calc(row_val_1,row_val_2)
    row_1_emb,row_2_emb = emb_calc(row_1,row_2)
    val_1_emb,val_2_emb = emb_calc(val_1,val_2)

    row_val_cos = calc_cosine(row_val_1_emb,table_1,row_val_2_emb,table_2)
    row_cos = calc_cosine(row_1_emb,table_1,row_2_emb,table_2)
    val_cos = calc_cosine(val_1_emb,table_1,val_2_emb,table_2)
    return {
        'row_val':row_val_cos,
        'row':row_cos,
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
    return x

"""### Align With Dictionary"""

def align_with_dictionary_new(table1_orig,table2_orig,table1_trans,table2_trans,category,languages):
    cat_dictionary = json.loads(open(category+"_dict.json","r").read())
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

def alignment_key_dict_new(table1_orig,table2_orig,table1_trans,table2_trans,category,languages,threshold, key_threshold, multi_threshold, max_multi,uni_threshold, dict_set=1):
    if(len(table1_orig)!=0 and len(table2_orig)!=0):
            try:
                aligned_t1 ,aligned_t2,al_reason=align_with_dictionary_new(table1_orig,table2_orig,table1_trans,table2_trans,category,languages)
            except:
                aligned_t1,aligned_t2,al_reason=[],[],[]
            if not dict_set:
                aligned_t1,aligned_t2,al_reason=[],[],[]
            # aligned_t1,aligned_t2,al_reason=[],[],[]
            # for al_row in range(0,len(aligned_t1)):
            #     print(str(aligned_t1[al_row])+"  "+str(aligned_t2[al_row]))
            cosines = get_cosines(table1_trans,table2_trans)
            key_cosines = cosines['row']
            val_cosines = cosines['val']
            cosines = cosines['row_val']
            # print(cosines)
            #aligned_t1 ,aligned_t2 = [],[]
            aligning_cosine = []
            unaligned_t1 = []
            unaligned_t2 = []
            key_order = np.argsort(key_cosines, axis=1)
            val_order = np.argsort(val_cosines, axis=1)
            order = np.argsort(cosines, axis=1)
            key_orderT = np.argsort(key_cosines.T, axis=1)
            val_orderT = np.argsort(val_cosines.T, axis=1)
            orderT = np.argsort(cosines.T, axis=1)
            # print(order)
            for table1_row in range(len(table1_trans)):
                ckey_order, cval_order, corder = key_order[table1_row], val_order[table1_row], order[table1_row]
                # print(len(cosines[table1_row]))
                if key_orderT[ckey_order[0]][0] == table1_row and key_cosines[table1_row][ckey_order[0]]<=key_threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[ckey_order[0]])
                    aligning_cosine.append(key_cosines[table1_row][ckey_order[0]])
                    al_reason.append("Key")
                elif orderT[corder[0]][0] == table1_row and cosines[table1_row][corder[0]]<=threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[corder[0]])
                    aligning_cosine.append(cosines[table1_row][corder[0]])
                    al_reason.append("Vals")

                if val_cosines[table1_row][cval_order[0]]<=uni_threshold:
                    aligned_t1.append(table1_orig[table1_row])
                    aligned_t2.append(table2_orig[corder[0]])
                    aligning_cosine.append(val_cosines[table1_row][cval_order[0]])
                    al_reason.append("Valw")

                for multi_idx in range(1,min(max_multi,len(corder))):
                    # print(table2_trans[corder[multi_idx]])
                    try:
                        orig_dist = multi_dist(table1_trans[table1_row][1],table2_trans[corder[0]][1])
                        # print(table1_trans[table1_row][1]," ",table2_trans[corder[0]][1]+table2_trans[corder[multi_idx]][1])
                        merged_dist = multi_dist(table1_trans[table1_row][1],table2_trans[corder[0]][1]+table2_trans[corder[multi_idx]][1])
                    except ValueError:
                        continue
                    if merged_dist <= multi_threshold and merged_dist<orig_dist:
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


def align_tables(tables,category,lang1,lang2,strong_thresh,key_thresh,align_thresh,multi_thresh,max_multi, uni_threshold, dict_set=1):
    try:
        table1_orig =  checker(open_table("tables/json/"+category+"/"+tables+"/"+lang1+"/table.html"),lang2,category+".csv")
        if lang1=="en":
            table1_trans=table1_orig
        else:
            table1_trans = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang1+"/final_translations.html"),lang2,category+".csv")
        table2_orig = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang2+"/table.html"),lang2,category+".csv")
        if lang2=="en":
            table2_trans=table2_orig
        else:
            table2_trans = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang2+"/final_translations.html"),lang2,category+".csv")
        if len(table2_orig)!=len(table2_trans) or len(table1_orig)!=len(table1_trans):
            return None
    except KeyboardInterrupt:
        print(abcd)
    
    try:
        dc = alignment_key_dict_new(table1_orig,table2_orig,table1_trans,table2_trans,category,[lang1,lang2],align_thresh,key_thresh,multi_thresh, max_multi, uni_threshold, dict_set)
    except KeyboardInterrupt:
            print(abcd)

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
        elif reason[i] == "Vals":
            vals_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "Valw":
            valw_aligned.extend([[al_t1[i],al_t2[i]]])
        elif reason[i] == "Multi":
            multi_aligned.extend([[al_t1[i],al_t2[i]]])
    complete_alignment = []
    if dict_aligned!=None:
        complete_alignment.extend(dict_aligned)
    if key_aligned!=None:
        complete_alignment.extend(key_aligned)
    if vals_aligned!=None:
        complete_alignment.extend(vals_aligned)
    if valw_aligned!=None:
        complete_alignment.extend(valw_aligned)
    if multi_aligned!=None:
        complete_alignment.extend(multi_aligned)
    return dict_aligned, key_aligned, vals_aligned, valw_aligned, multi_aligned ,complete_alignment, unal_t1, unal_t2,table1_orig, table2_orig