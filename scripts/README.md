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
│   ├── json
│   │   ├── Airport					# amazon mturk annotator statistics (data annotators)
│   │   └── Person					# amazon mturk annotator statistics (data validators)
│   └── html
│       ├── Airport 				# annotation template example 1 
│       ├── Person 				    # annotation template example 2 
│
├── final_test_set							# primary infotabs dataset folder
│   ├── Final_Test_Set_Eng_X 					# development datasplit
│   ├── Final_Test_Set_X_Y 				# test alpha1 datasplit
│   ├── Final_Test_Set_Eng_X.json 				# test alpha2 datasplit
│   ├── Final_Test_Set_X_Y.json 				# test alpha3 datasplit
│
│
├── true_test_set						# reasoning statistic folder
│   ├── True_Test_Set_HI 					# reasoning on subset of development datasplit
│   └── True_Test_Set_ZH 				# reasoning on subset of alpha3 datasplit
│
├── metadata 							# tables folder
│   ├── Metadata_Eng_X 							# tables premises in html format
│   │   ├── T0.html
│   │   ├── T1000.html
│   │   ├── T1001.html
│   │   ├── T998.html
│   │   ├── T999.html
│   │   ├── T99.html
│   │   └── T9.html
│   │
│   ├── Metadata_X_Y							# tables premises in json format
│   │   ├── T0.json
│   │   ├── T1000.json
│   │   ├── T1001.json
│   │   ├── T1002.json
│   │   ├── T999.json
│   │   ├── T99.json
│   │   └── T9.json
│   └── Metadata_Eng_X.json 					# table categories
│   		  
├── csv_data							# validation annotations folder
│   ├── infotabs_valid_dev.tsv 					# validation annotations development dataset
│   ├── infotabs_valid_test_alpha1.tsv 				# validation alpha1 annotations datasplit
│   ├── infotabs_valid_test_alpha2.tsv 				# validation alpha2 annotations datasplit
│   └── infotabs_valid_test_alpha3.tsv 				# validation alpha3 annotations datasplit
│
└── LICENSE, Datasheet, README.md, logo				#license,datasheet,dataset readme, logo files.

```
 
## 1. Training and Prediction with linearSVM
```data/maindata/``` and ```data/tables/``` will be the primary datasets folders to work on here.

### 1.1 Preprocessing
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
### 1.2 Convert to SVM format
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
## 1.3 Training and Prediction
For training and prediction on the SVM baseline download and install the [liblinear library](https://github.com/cjlin1/liblinear) in ```scripts/svm```. Use the appropiate directiory in ```./../../temp/svmformat/``` from either union or hypo for training and prediction. For example,
```
cd liblinear
./train -C ./../../temp/svmformat/union/train.txt
./train -c <best_c_value> ../svmformat/format/union/train.txt 	# <best_c_value> is the number obtained from last the iteration
./predict ../svmformat/union/test_dev.txt train.txt.model output_dev.txt
./predict ../svmformat/union/test_alpha1.txt train.txt.model output_test_alpha1.txt
./predict ../svmformat/union/test_alpha2.txt train.txt.model output_test_alpha2.txt
./predict ../svmformat/union/test_alpha3.txt train.txt.model output_test_alpha3.txt

```
```train.txt.model``` is the train model. ``` output_<split_name>.txt``` is the prediction for the mentioned split.

## 2. Training and Prediction with RoBERTa
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

## 3. mturk Validation
```data/validation/``` will be the primary dataset folder to work on here.

```
mkdir ./../../temp/validation/
mkdir ./../../temp/validation/plots
bash validation.sh
```
You would see a ```temp/validation/``` folder created with the following structure 
```

temp/validation/
│
├── metric_summary.txt 				# summary of all the inter-annotator results, i.e., individual agreements (majority/gold) and the Kappa values
└── plots 					# plots of percentage of number of gold and majority label agreements matches for 3,4, and 5 annotators agreements
    ├── dev.png 				# plot for dev splits
    ├── test_alpha1.png 			# plot for alpha1 splits
    ├── test_alpha2.png 			# plot for alpha2 splits
    └── test_alpha3.png 			# plot for alpha3 splits

```
## 4. Statistics
```data/maindata/```, ```data/tables/``` and ```data/reasoning/``` will be the primary datasets folders to work on here.

### 4.1 General Statistics
```data/maindata/``` and ```data/tables/``` will be the primary datasets folders to work on here.
```
mkdir ./../../temp/statistic
python3 data_statistics.py > ./../../temp/statistic/general-statitics.txt			# output general statistics

```
### 4.2 Reasoning Statistics
```data/reasoning/``` and ```data/tables/``` will be the primary datasets folders to work on here. 

We need to first get predictions on the reasoning subset before running

```
# perform preprocessing as in section 1.1

cd scripts
mkdir ./../../temp
mkdir ./../../temp/data/
mkdir ./../../temp/data/reasoning
python3 json_to_para.py --json_dir ./../../data/tables/json/ --data_dir ./../../data/reasoning/ --save_dir ./../../temp/data/reasoning/  --splits dev test_alpha3

# perform vectorizing as in section 1.2
mkdir ./../../temp/processed
python3 preprocess_roberta.py --max_len 512 --data_dir ./../../temp/data/ --in_dir reasoning --out_dir ../processed/reasoning --single_sentence 0 --splits dev test_alpha3

# do prediction by using the best train model on premises as in section 1.3
set the arguments as 'in_dir' as "./../../temp/processed/parapremise/" and other parameters as "-- mode" t0 "test", "moder_dir" to "./../../temp/models/parapremise/", "model_name" is set to the best dev accuracy model name for ```temp/models/parapremise```, "parallel" to 0/1 similar to earlier instructions in classifier.sh

```
You will see a new ```./../../temp/models/reasoning/``` with files as ```predict_dev.json``` and ```predict_test_alpha3.json``` which is similar to earlier discussed prediction files. You can now run the reasoning statistics code as following:

```
mkdir ./../../temp/statistic
python3 reasoning_statistics.py > ./../../temp/statistic/reasoning-statitics.txt			# output reasoning statistics

```

## ToDo

```
1. Table extractor, table-splitter, table2json codes (we manualy clean many jsons)
2. Datasheet (in the data github directory)
3. TabAttn code

```
