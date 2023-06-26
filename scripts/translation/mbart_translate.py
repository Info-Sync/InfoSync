from collections import OrderedDict
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from spacy_install import *
from preprocessing import *

langbart = OrderedDict([
    ('af',"af_ZA"), 
    ('de',"de_DE"),  
    ('hi',"hi_IN"), 
    ('ko',"ko_KR"), 
    ('nl',"nl_XX"), 
    ('ru',"ru_RU"), 
    ('sv',"sv_SE"), 
    ('tr',"tr_TR"), 
    ('zh',"zh_CN")
    ])

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt").to(torch_device)
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

def translate_mbart(text, src_code):
  tokenizer.src_lang = src_code
  encoded = tokenizer(text, return_tensors="pt")
  generated_tokens = model.generate(
      **encoded.to(torch_device),
      forced_bos_token_id = tokenizer.lang_code_to_id["en_XX"]
  )
  res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
  return res[0]

def translate_all_mbart(table_texts, value):
  tr_table_texts = []
  tr_punk_1 = '//'
  tr_punk_2 = ':'

  err_1 = 0
  err_2 = 0

  for text in tqdm(table_texts):
      text_1 = text.replace("||", tr_punk_1)
      tr_text = translate_mbart(text_1, value)
      # print(tr_text)

      if len(tr_text.split(tr_punk_1)) == 3 :
          tr_text = tr_text.replace(tr_punk_1, '||')
          tr_table_texts.append(tr_text)
      else:
          err_1 += 1

          text_2 = text.replace("||", tr_punk_2)
          tr_text = translate_mbart(text_2, value)

          if len(tr_text.split(tr_punk_2)) == 3 :
              tr_text = tr_text.replace(tr_punk_2, '||')
              tr_table_texts.append(tr_text)
          else:
              err_2 += 1
      # print(tr_table_texts)


              cat, key, val = text.split(' || ')

              tr_cat = translate_mbart(cat, value)
              tr_key = translate_mbart(key, value)
              tr_val = translate_mbart(val, value)
              
              tr_text = tr_cat + " || " + tr_key + " || " + tr_val
              tr_table_texts.append(tr_text)
  # print(tr_table_texts)

  # print(f"{100 * err_1/len(table_texts)} {100 * err_2 / len(table_texts)}")
  
  tr_table = {}
  for text in tr_table_texts:
      cat, key, val = [x.strip() for x in text.split('||')]

      # try:
      #     text_content = val
      #     new_text = ""
      #     for t in text_content.split('"'):
      #         doc = nlp(t)
      #         detect_language = doc._.language
      #         if detect_language['language'] != keys and detect_language['language'] != 'UNKNOWN':
      #             suggestions = transliterate_word(t, lang_code=keys)
      #             new_text = new_text+" " + suggestions[0]
      #         else:
      #             new_text = new_text+t
      #         new_text = new_text.strip()
      #     val = new_text
      #     if key in tr_table.keys():
      #         tr_table[key].append(val)
      #     else:
      #         tr_table[key] = []
      #         tr_table[key].append(val)

      # except:
      val = val.replace('"', '')   # Removing quotes from NER values
      if key in tr_table.keys():
          tr_table[key].append(val)
      else:
          tr_table[key] = []
          tr_table[key].append(val)

      # print(tr_table)

  json_object = json.dumps(tr_table, indent=4, ensure_ascii=False)
  return json_object

def main():
    for topic in os.scandir("./tables/html"):
        print(topic.name)
        for n in os.scandir("./tables/html/"+topic.name):
            print(n.name)

            for keys, value in langbart.items():
                table_texts = []
                for row in checker(open_table("./tables/html/"+topic.name+"/"+n.name+"/"+keys+"/table.html"), keys, topic.name+".csv"):
                    # print(row)
                    category = topic.name
                    context = category + " || " + row[0] + " || "
                    ner_text = ner(row[1])
                    # ner_flag = all([(a.tag_ == 'NNP' or a.tag_ == 'NNPS' or a.tag_ == 'NNS' or a.tag_ == 'NN')
                    #                 for a in ner_text if str(a) not in string.punctuation])

                    if ProperNounExtractor(str(ner_text)):
                        # print(value)
                        text = context + '"' + row[1] + '"'
                    else:
                        text = context + row[1]

                    table_texts.append(text)
                # print(table_texts)
                file = open("./tables/json/"+topic.name+"/"+n.name+"/" +keys+"/final_translations.html", "w", encoding='utf-8')
                file.write(json2html.convert(json=translate_all_mbart(table_texts, value)))
                file.close()

if __name__ == "__main__":
    main()
