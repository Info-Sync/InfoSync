def getRecall(aligned_table,ideal_table):
    count=0
    for alignment in ideal_table:
        if alignment in aligned_table:
            count+=1
    return count/len(ideal_table)

def getPrecision(aligned_table,ideal_table):
    count=0
    for alignment in aligned_table:
        if alignment in ideal_table:
            count+=1
    return count/len(aligned_table)

def get_metric(aligned_table,ideal_table,verbosity):
    aligned_table = [[x[0][0],x[1][0]] for x in aligned_table]
    if verbosity:
        print(aligned_table)
        print(ideal_table)
        print("\n\n")
    return getPrecision(aligned_table,ideal_table),getRecall(aligned_table,ideal_table)

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def getUnPrec(l1, l2):
    c = [x for x in l1 if x not in l2]
    if len(l1) == 0:
        return 1
    return 1 - (len(c)/len(l1))

def getUnRec(l1, l2):
    if len(l2) == 0:
        return 1
    return getUnPrec(l2,l1)

def getUnMetric(aligned_table,ideal_table,t1,t2):
    aligned_table = [[x[0][0],x[1][0]] for x in aligned_table]
    k1 = [x[0] for x in aligned_table]
    k2 = [x[1] for x in aligned_table]

    ik1 = [x[0] for x in ideal_table]
    ik2 = [x[1] for x in ideal_table]

    tk1 = [x[0] for x in t1]
    tk2 = [x[0] for x in t2]

    return getUnPrec(Diff(tk1+tk2,k1+k2),Diff(tk1+tk2,ik1+ik2)), getUnRec(Diff(tk1+tk2,k1+k2),Diff(tk1+tk2,ik1+ik2))
