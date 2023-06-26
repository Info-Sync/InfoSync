from spacy_install import *
from preprocessing import *

from transformers import MarianMTModel, MarianTokenizer

en_model_name = 'Helsinki-NLP/opus-mt-ROMANCE-en'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
en_tokenizer = MarianTokenizer.from_pretrained(en_model_name)
en_model = MarianMTModel.from_pretrained(en_model_name).to(torch_device)

def translate_marian(text, model, tokenizer, language):
    # Prepare the text data into appropriate format for the model
    template = lambda text: f"{text}" if language == "en" else f">>{language}<< {text}"

    # Tokenize the texts
    # encoded = tokenizer.prepare_seq2seq_batch(template(text))
    
    # Generate translation using model
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True).to(torch_device))

    # Convert the generated tokens indices back into text
    translated_texts = tokenizer.batch_decode(translated, skip_special_tokens=True)
    
    return translated_texts

def preprocessing_es_fr(table_texts):
  tr_table_texts = []
  tr_punk_1 = '//'
  tr_punk_2 = ':'

  err_1 = 0
  err_2 = 0

  for text in tqdm(table_texts):
      text = text.replace("|", "::")
      text_1 = text.replace("%%", tr_punk_1)
      tr_text = translate_marian(text_1, en_model, en_tokenizer, language='en')

      if len(tr_text[0].split(tr_punk_1)) == 3 :
          tr_text[0] = tr_text[0].replace(tr_punk_1, '||')
          tr_text[0] = tr_text[0].replace("::", "|")
          tr_table_texts.append(tr_text[0])
      else:
          err_1 += 1

          text_2 = text.replace("%%", tr_punk_2)
          tr_text = translate_marian(text_2, en_model, en_tokenizer, language='en')

          if len(tr_text[0].split(tr_punk_2)) == 3 :
              tr_text[0] = tr_text[0].replace(tr_punk_2, '||')
              tr_text[0] = tr_text[0].replace("::", "|")
              tr_table_texts.append(tr_text[0])
          else:
              err_2 += 1


              cat, key, val = text.split(' %% ')
              tr_cat = translate_marian(cat, en_model, en_tokenizer, language='en')
              tr_key = translate_marian(key, en_model, en_tokenizer, language='en')
              tr_val = translate_marian(val, en_model, en_tokenizer, language='en')
              tr_text[0] = tr_cat[0] + " || " + tr_key[0] + " || " + tr_val[0]
              tr_text[0] = tr_text[0].replace("::", "|")
              tr_table_texts.append(tr_text[0])
  # print(tr_table_texts)

  # print(f"{100 * err_1/len(table_texts)} {100 * err_2 / len(table_texts)}")
  
  tr_table = {}
  for text in tr_table_texts:
      cat, key, val = [x.strip() for x in text.split('||')]
      val = val.replace('"', '') 
      if key in tr_table.keys():
          tr_table[key].append(val)
      else:
          tr_table[key] = []
          tr_table[key].append(val)

  # return tr_table
  json_object = json.dumps(tr_table, indent=4, ensure_ascii=False)
  return json_object


def french():
    for topic in os.scandir("./tables/html"):
        print(topic.name)
        for n in os.scandir("./tables/html/"+topic.name):
            print(n.name)

            table_texts = []
            for row in checker(open_table("./tables/html/"+topic.name+"/"+n.name+"/fr/table.html"), 'fr', topic.name+".csv"):
                # print(row)
                category = topic.name
                context = category + " %% " + row[0] + " %% "
                ner_text = ner(row[1])
                # print(ner_text)
                # ProperNounExtractor(str(ner_text))
                # ner_flag = all([(a.tag_ == 'NNP' or a.tag_ == 'NNPS' or a.tag_ == 'NNS' or a.tag_ == 'NN')
                #                 for a in ner_text if str(a) not in string.punctuation])

                if ProperNounExtractor(str(ner_text)):
                    # print(value)
                    text = context + '"' + row[1] + '"'
                else:
                    text = context + row[1]

                table_texts.append(text)
        # print(table_texts)

            # preprocessing_es_fr(table_texts)
            file = open("./tables/json/"+topic.name+"/"+n.name+"/fr/final_translations.html", "w", encoding='utf-8')
            file.write(json2html.convert(json=preprocessing_es_fr(table_texts)))
            file.close()

def es():
    for topic in os.scandir("./tables/html"):
        print(topic.name)
        for n in os.scandir("./tables/html/"+topic.name):
            print(n.name)

            table_texts = []
            for row in checker(open_table("./tables/html/"+topic.name+"/"+n.name+"/es/table.html"), 'es', topic.name+".csv"):
                # print(row)
                category = topic.name
                context = category + " %% " + row[0] + " %% "
                ner_text = ner(row[1])
                # print(ner_text)
                # ProperNounExtractor(str(ner_text))
                # ner_flag = all([(a.tag_ == 'NNP' or a.tag_ == 'NNPS' or a.tag_ == 'NNS' or a.tag_ == 'NN')
                #                 for a in ner_text if str(a) not in string.punctuation])

                if ProperNounExtractor(str(ner_text)):
                    # print(value)
                    text = context + '"' + row[1] + '"'
                else:
                    text = context + row[1]

                table_texts.append(text)
            # print(table_texts)
            preprocessing_es_fr(table_texts)
            
            file = open("./tables/json/"+topic.name+"/"+n.name+"/es/final_translations.html", "w", encoding='utf-8')
            file.write(json2html.convert(json=preprocessing_es_fr(table_texts)))
            file.close()

def main():
    french()
    es()
    
if __name__ == "__main__":
    main()
