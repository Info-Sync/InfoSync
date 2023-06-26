multikey_list = ["Opened","Language","President","Genre","Headquarters","Kingdom","Website","Type","Coordinates","Internet TLD","Born","Genus","Occupation","Density","Calling code","Time zone","Awards","Species","Years active","Country","Died","Location","Family","Labels","Order","Genres","Founded","Nationality","Official languages","Currency","Capital | and largest city","Capacity","Total"]
multiKey_engX = {"Opened":[],"Language":[],"President":[],"Genre":[],"Headquarters":[],"Kingdom":[],"Website":[],"Type":[],"Coordinates":[],"Internet TLD":[],"Born":[],"Genus":[],"Occupation":[],"Density":[],"Calling code":[],"Time zone":[],"Awards":[],"Species":[],"Years active":[],"Country":[],"Died":[],"Location":[],"Family":[],"Labels":[],"Order":[],"Genres":[],"Founded":[],"Nationality":[],"Official languages":[],"Currency":[],"Capital | and largest city":[],"Capacity":[],"Total":[]}

lang = [
    "en","de", "fr", "es", "nl", "ar", "hi", "zh", "ko", "ru", "tr", "af","ceb","sv"
]

high_res_lang = ["en", "fr", "ru", "ko", "es", "tr", "sv", "nl"]
low_res_lang = ["de", "hi", "ar", "ceb", "af", "zh"]
trend_keys = ['Age','Total equity', 'Employees', 'Number of locations', 'AUM', 'Students', 'Budget', 'Academic staff', 'Administrative staff', 'Undergraduates', 'Postgraduates', 'Population', 'Revenue', 'Net Income', 'Total Assets', 'Sales', 'Number of employees', 'Turnover', 'Net income', 'Net result', 'Income', 'Net profit', 'turnover/year', 'Win/Year', 'Business volume', 'Net worth of assets', 'Capital', 'Number of Employees', 'Tax break', 'Equity', 'Population of employees', 'Staff', 'Outturn', 'Capitalization', 'Share capital', 'Net Profit', 'Market capitalization', 'Total Equity', 'The number of employees.', 'net profit', 'Net Worth', 'Revenues', 'Total revenue', 'Net profits', 'Total Shares', 'Business Location', 'Returns', 'Business', 'Used capital', 'Operating income', 'revenue', 'Sales revenue', 'students', 'Professors', 'Number of students', 'Number of staff', 'Undergraduate', 'Graduate', 'Students.', 'Number of teachers', 'Number of undergraduates', 'Number of graduates', 'Number of teachers.', 'Number of undergraduates.', 'Ph.D. student count', 'Teachers', 'Bachelors', 'Masters and Doctors', 'Postgraduate Students',  'Ph.D. students', 'Postgraduate students', 'Annual budget', 'Registered students',  'Postgraduate Studies', 'graduate school number', 'Student Number', 'Number of Students',  'Workers', 'Number of students.',  'graduate school population', 'Budget.', 'population',  'Population | – Metropolitan region',  'Population Census', 'The number of employees', 'Population Census | (2018)',  'Population Density',  'Population Census | (2014)', 'Population Census | (2019)']
rarerKey = ["Website"]
not_time_mentioned = ['Place of birth','Years in Service','Year of construction','Years of service','Postal codes','Renovation', 'Opened', 'Rebuilt', 'Born', 'Premieres', 'Death', 'Active years', 'Christmas', 'Period of activity.', 'Years of activity', 'Years of Activity', 'Official Opening History', 'Opening day', 'Opening date', 'Date of Foundation', 'Establishment', 'Founded', 'Established', 'Foundation','Recorded']

filename = 'value_add.txt'
with open(filename) as f:
    value_add = f.read().splitlines() 


def row_addition(al_t1, al_t2, table1_trans, table2_trans):
    unal_t1 = [i for i in table1_trans if i not in al_t1]
    unal_t2 = [i for i in table2_trans if i not in al_t2]
    return unal_t1, unal_t2

def highRes_lowRes(lang1, lang2):
    if lang1 in high_res_lang and lang2 in low_res_lang or lang1 in low_res_lang and lang2 in high_res_lang:
        return True
    elif lang1 == "en" or lang2 == "en":
        if lang1 == "en" and lang2 == "fr" or lang2 == "es" or lang2 == "ru":
            return False
        elif lang2 == "en" and lang1 == "fr" or lang1 == "es" or lang1 == "ru":
            return False
        else:
            return True
    else:
        return False

def highRows_lowRows(table1_trans, table2_trans):
    if len(table1_trans) == len(table2_trans):
        return False
    else:
        return True

def superset_subset(key1, value1, value2):
    if key1 in value_add:
        if len(value1.split(" | "))>1 and len(value2.split(" | ")) < len(value1.split(" | ")):
            return True
        elif len(value1.split(" | ")) < len(value2.split(" | ")) and len(value2.split(" | "))>1:
            return True
        elif len(value1.split(", "))>1 and len(value2.split(", ")) < len(value1.split(", ")):
            return True
        elif len(value1.split(", ")) < len(value2.split(", ")) and len(value2.split(", "))>1:
            return True
        else:
            return False
    else:
        False

def time_mentioned(key1, key2, value1, value2):
    if key1 not in not_time_mentioned:
        year_pattern = re.compile(r'\b\d{4}\b')
        match1 = year_pattern.search(key1)
        match2 = year_pattern.search(key2)
        match3 = year_pattern.search(value1)
        match4 = year_pattern.search(value2)
        if match1 and match2:
            year1 = int(match1.group())
            year2 = int(match2.group())
            # Compare the years
            if year1 == year2:
                return False
            else:
                return True
        elif match3 and match4:
            year3 = int(match3.group())
            year4 = int(match4.group())
            if year3 == year4:
                return False
            else:
                return True
        elif match1 and match4:
            year1 = int(match1.group())
            year4 = int(match4.group())
            if year1 == year4:
                return False
            else:
                return True
        elif match3 and match2:
            year3 = int(match3.group())
            year2 = int(match2.group())
            if year3 == year2:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def key_with_trend(key1, value1, value2):
    if key1 in trend_keys:
        match1 = re.search(r'\d+', value1)
        match2 = re.search(r'\d+', value2)
        if match1 and match2:
            num1 = int(match1.group(0))
            num2 = int(match2.group(0))
            if num1 == num2:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def multiKey_singleKey(arr1, arr2):
    final_arr = []
    count1 = Counter(arr1)
    duplicate_element1 = [element for element, count in count1.items() if count > 1]
    count2 = Counter(arr2)
    duplicate_element2 = [element for element, count in count2.items() if count > 1]
    for item in duplicate_element1:
        final_arr.append(item)
    for item in duplicate_element2:
        final_arr.append(item)
    return final_arr


def rareKey(table1_trans, table2_trans):
    k1 = []
    k2 = []
    for item in table1_trans:
        k1.append(item[0])
    for item in table2_trans:
        k2.append(item[0])

    for key in rarerKey:
        if key in k1 and key not in k2:
            return True
        elif key not in k1 and key in k2:
            return True
        else:
            return False


def check_rule(al_t1, al_t2, lang1, lang2, table1_trans, table2_trans):
    rule_count = {
        "Row Addition": 0,
        "High res to Low res Language": 0,
        "Higher no of rows to lower no": 0,
        "Superset-subset": 0,
        "Time mentioned": 0,
        "Trend": 0,
        "Multikey to single key": 0,
        "Rarer key": 0
    }
    key_store = {
        "Row Addition": [],
        "High res to Low res Language": [],
        "Higher no of rows to lower no": [],
        "Superset-subset": [],
        "Time mentioned": [],
        "Trend": [],
        "Multikey to single key": [],
        "Rarer key": []
    }
    unal_t1, unal_t2 = row_addition(al_t1, al_t2, table1_trans, table2_trans)
    rule_count["Row Addition"] = len(unal_t1) + len(unal_t2)
    # key_store["Row Addition"].append(unal_t1)
    # key_store["Row Addition"].append(unal_t2)
    arr1=[]
    arr2=[]
    for al_row in range(0, len(al_t1)):
        arr1.append(al_t1[al_row][0])
        arr2.append(al_t2[al_row][0])  

    flag_multikey_singlekey = False
    for al_row in range(0, len(al_t1)):
        key1 = al_t1[al_row][0]
        key2 = al_t2[al_row][0]
        value1 = al_t1[al_row][1]
        value2 = al_t2[al_row][1]    
        if key1 in key_store["Multikey to single key"]:
            continue
        else:
            if not flag_multikey_singlekey:
                final_arr = multiKey_singleKey(arr1, arr2)
                rule_count["Multikey to single key"] = len(final_arr)
                key_store["Multikey to single key"] = final_arr
                flag_multikey_singlekey = True

            else:
                if time_mentioned(key1, key2, value1, value2):
                    rule_count["Time mentioned"] += 1
                    key_store["Time mentioned"].append(key1)
                else:
                    if key_with_trend(key1, value1, value2):
                        rule_count["Trend"] += 1
                        key_store["Trend"].append(key1)
                    else:
                        if superset_subset(key1, value1, value2):
                            rule_count["Superset-subset"] += 1
                            key_store["Superset-subset"].append(key1)
                        else:
                            if highRes_lowRes(lang1, lang2):
                                rule_count["High res to Low res Language"] += 1
                                key_store["High res to Low res Language"].append(key1)
                            else:
                                if highRows_lowRows(table1_trans, table2_trans):
                                    rule_count["Higher no of rows to lower no"] += 1
                                    key_store["Higher no of rows to lower no"].append(key1)
                                else:
                                    if rareKey(table1_trans, table2_trans):
                                        rule_count["Rarer key"] += 1
                                        key_store["Rarer key"].append(key1)
                                    else:
                                        continue
                    
    return rule_count, key_store        
                


def update():
    rd=0
    hres = 0
    hrow = 0
    va = 0
    tm = 0
    tk = 0
    ms = 0
    rk = 0
    total = 0

    test_file = open("live_new.json","r")
    test_set = json.load(test_file)
    for category in test_set.keys():
        print(category)
        for tables in test_set[category]:
            print(tables)
            for lang_key in test_set[category][tables]:
                splitted = lang_key.split("_")
                lang1 = splitted[0]
                lang2 = splitted[1]
                # # print(lang_key)
                # if lang1 == 'en':
                #     continue
                # else:
                print(lang_key)
                try:
                    table1_orig =  checker(open_table("tables/json/"+category+"/"+tables+"/"+lang1+"/table.html"),lang1,category+".csv")
                    if lang1=="en":
                        table1_trans=table1_orig
                    else:
                        table1_trans = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang1+"/final_translations.html"),lang1,category+".csv")
                    table2_orig = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang2+"/table.html"),lang2,category+".csv")
                    if lang2=="en":
                        table2_trans=table2_orig
                    else:
                        table2_trans = checker(open_table("tables/json/"+category+"/"+tables+"/"+lang2+"/final_translations.html"),lang2,category+".csv")
                    if len(table2_orig)!=len(table2_trans) or len(table1_orig)!=len(table1_trans):
                        continue
                except KeyboardInterrupt:
                    print(abcd)
                al_t1 = []
                al_t2 = []
                for value in test_set[category][tables][lang_key]:
                    al_t1.append(value[0])
                    al_t2.append(value[1])

                print(al_t1)
                print(al_t2)
                total += len(al_t1)
                
                rule_count, key_store = check_rule(al_t1, al_t2, lang1, lang2, table1_trans, table2_trans)
                print(str(rule_count))
                print(str(key_store))

                rd+=rule_count["Row Addition"]
                hres+=rule_count["High res to Low res Language"]
                hrow+= rule_count["Higher no of rows to lower no"]
                va += rule_count["Superset-subset"]
                
                tm += rule_count["Time mentioned"]
                tk += rule_count["Trend"]
                ms += rule_count["Multikey to single key"]
                rk += rule_count["Rarer key"]
        print(total, rd, ms, tm, tk, va, hres, hrow, rk)

    print(total, rd, ms, tm, tk, va, hres, hrow, rk)


def main():
    update()

if __name__ == "__main__":
    main()