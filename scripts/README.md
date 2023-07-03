# InfoSync
<!-- <p align="center"><img width="80%" src="logo.png" /></p> -->

Implementation of the semi-structured inference model in our [ACL 2023](https://2023.aclweb.org/) paper: [INFOSYNC: Information Synchronization across Multilingual Semi-structured Tables](https://vgupta123.github.io/docs/infosync_paper.pdf). To explore the dataset online visit [project page](https://info-sync.github.io/info-sync/).

```
TO BE ADDED
```

Below are the details about the [INFOSYNC datasets](https://github.com/Info-Sync/InfoSync) and scripts for reproducing the results reported in the [ACL 2023](https://2023.aclweb.org/) paper.

## 0. Prerequisites
The code requires `python 3.6+`

Clone this repository on your machine - `https://github.com/Info-Sync/InfoSync.git` 

Install requirements by typing the following command-
```pip install -r requirements.txt``` 


Download and unpack the [INFOSYNC datasets](https://github.com/Info-Sync/InfoSync) into ```./data``` in the main ```InfoSync``` folder. 

Carefully read the LICENCE and the Datasheet for non-academic usage. 

After downloading, you have multiple sub-folders with several csv/html/json files. Each csv file in the sub-folders has 1st rows as a header:

```
data
│ 
├── tables
│   ├── json				    # contains json data for all the categories. Files are in html format for easies understanding of the data
│   └── html                                # data scraped for all the categories
│
├── final_test_set		            # test set, built using semi-automated pipeline. Annotated by humans using translations
│   ├── Final_Test_Set_Eng_X 		    # contains files for Eng_X for all categories
│   ├── Final_Test_Set_X_Y 	            # contains files for X_Y for all categories
│   ├── Final_Test_Set_Eng_X.json 	    # json file with all annotations for Eng_X
│   └── Final_Test_Set_X_Y.json 	    # json file with all annotations for X_Y
│
│
├── true_test_set			    # true-test-set, annotated by native speakers of Hindi and Chinese without using translations
│   ├── True_Test_Set_HI 		    # contains files for Eng_HI for all categories
│   ├── True_Test_Set_ZH 		    # contains files for Eng_ZH for all categories
│   ├── True_Test_Set_HI.json 	            # json file with all annotations for Eng_HI
│   └── True_Test_Set_ZH.json 		    # json file with all annotations for Eng_ZH
|
├── metadata 			            # metadata for error analysis
│   ├── Metadata_Eng_X 
│   ├── Metadata_X_Y						
│   ├── Metadata_Eng_X.json 							
|   └── Metadata_X_Y.json 
│   		  
├── csv_data				    # csv data for all categories, with links for different wikipedia pages
│
└── LICENSE, Datasheet, README.md, logo	    #license,datasheet,dataset readme, logo files.

```
 
## 1. Dataset
```data/maindata/``` and ```data/tables/``` will be the primary datasets folders to work on here.

### 1.1 Collection
Preprocessing is separated into the following steps.

First extract something out of the json files. Assume the data is downloaded and unpacked into ```data/maindata/```
```
cd scripts/preprocess/
mkdir ./../../temp
mkdir ./../../temp/data/
mkdir ./../../temp/data/parapremise
python3 json_to_para.py --json_dir ./../../data/tables/json/ --data_dir ./../../data/maindata/ --save_dir ./../../temp/data/parapremise/

```
You would see a ```temp/data/``` folder. ```temp/data/``` will contain sub-folders for several premise types. For example,
```

temp/data/
│ 
└── parapremise 						# paragraph as premise
    ├── dev.tsv 						# development datasplit
    ├── test_alpha1.tsv 					# test alpha1 datasplit
    ├── test_alpha2.tsv 					# test alpha2 datasplit
    ├── test_alpha3.tsv 					# test alpha3 datasplit
    └── train.tsv 						# training datasplit

```
### 1.2 Preprocessing
Then batch examples and vectorize them:
```
cd ../svm
mkdir ./../../temp/svmformat
mkdir ./../../temp/svmformat/hypo
mkdir ./../../temp/svmformat/union 						
python hypo.py 					#only hypothesis unigram-bigram tokens as features
python union.py 				#union of premise and hypothesis unigram-bigram tokens as features

```
Your ```temp/svmformat/``` will contain sub-folders for the premise type (hypo, union). For example, 
```

temp/svmformat/union
│									
├── dev.txt 							# development datasplit
├── test_alpha1.txt 						# test alpha1 datasplit
├── test_alpha2.txt 						# test alpha2 datasplit
├── test_alpha3.txt 						# test alpha3 datasplit
└── train.txt 							# training datasplit

```

## 2. Alignment
```data/maindata/``` and ```data/tables/``` will be the primary datasets folders to work on here.

### 2.1 Preprocessing
Preprocessing is separated into the following steps.

First extract something out of the json files. Assume the data is downloaded and unpacked into ```data/maindata/```
```
cd scripts/preprocess/
mkdir ./../../temp
mkdir ./../../temp/data/
bash json_to_all.sh 						# comment premise types as needed

```
This might take a few minutes. You would see a ```temp/data/``` folder. ```temp/data/``` will contain sub-folders for several premise types. For example, 
```

temp/data/
│ 
└── parapremise 						# paragraph as premise
    ├── dev.tsv 						# development datasplit
    ├── test_alpha1.tsv 					# test alpha1 datasplit
    ├── test_alpha2.tsv 					# test alpha2 datasplit
    ├── test_alpha3.tsv 					# test alpha3 datasplit
    └── train.tsv 						# training datasplit

```
### 2.2 Vectorizing
Then batch examples and vectorize them:
```
cd ../roberta
mkdir ./../../temp/processed 						
bash preprocess_roberta.sh 					# comment premise types as needed

```
You would see a ```temp/processed/``` folder. ```temp/processed/``` will contain sub-folders for several premise types. For example, 
```

temp/processed/
│
└── parapremise 						# paragraph as premise
    ├── dev.pkl 						# development datasplit
    ├── test_alpha1.pkl 					# test alpha1 datasplit
    ├── test_alpha2.pkl 					# test alpha2 datasplit
    ├── test_alpha3.pkl 					# test alpha3 datasplit
    └── train.pkl 						# training datasplit

```
## 2.3 Training and Prediction
For training and prediction on the RoBERTa baseline look at ```.\scripts\roberta\classifier.sh```:
```
example argument in train_classifier

python3 classifier.py \
	--mode "train" \
	--epochs 10 \
	--batch_size 8 \
	--in_dir "./../../temp/processed/parapremise/" \
	--model_type "roberta-large" \
	--model_dir "./../../temp/models/parapremise1/" \
	--model_name "model_6_0.7683333333333333" \
	--save_dir "./../../temp/models/" \
	--save_folder "parapremise1/" \
	--nooflabels 3 \
	--save_enable 0 \
	--eval_splits dev test_alpha1\
	--seed 13 \
	--parallel 0

important argument details which could be reset as needed for training and prediction

-- mode: set "train" for training, set "test" for prediction
-- epochs: set training epochs number (only used while training, i.e., model is "train")
-- batch_size: set batch size for training (only used while training)
-- in_dir: set as preprocessed directory name, i.e., a folder named in temp/processed/ . Use this for setting the appropriate premise type. (only used while training, i.e., model is "train") 
-- model_type: A string which determines which model will be used for training/evaluating. The value should be one of the classes mentioned on the Huggingface transformers website - https://huggingface.co/transformers/pretrained_models.html
-- model_dir: use the model directory containing the train model (only used while prediction, i.e., model is "test")
-- model_name: model finename usually is in format 'model_<batch_number>_<dev_accuracy>' (only used while prediction, i.e., model is "test")
-- save_folder: name the primary models directory appropriately as ./../.../temp/models/ (only used while training i.e., model is "train")
-- save_dir: name the primary models directory appropriately, usually same as the in_dir final directory (only used while training, i.e., model is "train")
-- nooflabels: set as 3 as three labels entailment, neutral and contradiction)
-- save_enable: set as 1 to save prediction files as predict_<datsetname>.json in model_dir. json contains accuracy, predicted label and gold label (in the same sequence order as the dataset set tsv in temp/data/)  (only used while prediction, i.e., model is "test")
-- eval-splits: ' '  separated datasplits names [dev, test_alpha1, test_alpha2, test_alpha3] (only used while prediction, i.e., model is "test")
-- seed: set a particular seed
-- parallel:  for a single GPU, 1 for multiple GPUs (used when training large data, use the same flag at both predictions and train time)

```
After training you would see a ```temp/models/``` folder. ```temp/models/``` will contain sub-folders for several premise types. Furthermore, prediction would create ```predict_<split>.json``` files. For example, 
```

temp/models/
│
└── parapremise 						# paragraph as premise
    ├── model_<epoch_no>_<dev_accuracy> 			# save models after every epoch
    ├── scores_<epoch_no>_dev.json  				# development prediction json results
    ├── scores_<epoch_no>_test.json				# test alpha1 prediction json results
    └── predict_<split>.json 					# prediction json (when predicting with argument "-- save_enable" set to 1)

```

For prediction on INFOTABS with SNLI and MNLI datasets train RoBerta models. Do the following
```
1. download pre-train snli/mnli models and put them in ```temp/models/``` under snli/mnli folders
2. modify the arguments "-- mode" t0 "test", "moder_dir" to "./../../temp/models/snli/" for snli and  "moder_dir" to "./../../temp/models/mnli/" for mnli, "model_name" is set to appropriate downloaded model name for snli/mnli, "parallel" to 0/1 as per earlier instructions, "in_dir" as per premise type in classifier.sh

```

For evaluation on metrics other than accuracy, such as F1-score, use the scikit-learn metrics functions with arguments as "predict" and "gold" lists from the predicted jsons.

## 3. Updation
```data/final_test_set/``` will be the primary dataset folder to work on here.

```
python align_update/updation.py
```
You would see the print with the update results
