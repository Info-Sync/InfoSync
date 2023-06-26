# InfoSync
<!-- <p align="center"><img width="80%" src="logo.png" /></p> -->

If you use our dataset, please cite our ACL 2023 paper: [INFOSYNC: Information Synchronization across Multilingual Semi-structured Tables](https://www.aclweb.org/anthology/2020.acl-main.210.pdf).

```
@inproceedings{gupta-etal-2020-infotabs,
    title = "{INFOSYNC}: Information Synchronization across Multilingual Semi-structured Tables",
    author = "Khincha, Siddharth  and
      Jain, Chelsi  and
      Gupta, Vivek  and
      Kataria, Tushar and
      Zhang, Shuo",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2023",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.210",
    pages = "2309--2324",
    abstract = "Information Synchronization of semi-structured data across languages is challenging. For instance, Wikipedia tables in one language should be synchronized across languages. To address this problem, we introduce a new dataset INFOSYNC and a two-step method for tabular synchronization. INFOSYNC contains 100K entity-centric tables (Wikipedia Infoboxes) across 14 languages, of which a subset (∼3.5K pairs) are manually annotated. The proposed method includes 1) Information Alignment to map rows and 2) Information Update for updating missing/outdated information for aligned tables across multilingual tables. When evaluated on INFOSYNC, information alignment achieves an F1 score of 87.91 (en ↔ non-en). To evaluate information updation, we perform human-assisted Wikipedia edits on Infoboxes for 603 table pairs. Our approach obtains an acceptance rate of 77.28% on Wikipedia, showing the effectiveness of the proposed method."
}
```

Carefully read the LICENCE and the Datasheet for non-academic usage. 

After downloading, you have multiple sub-folders with several csv/html/json files. Each csv file in the sub-folders has 1st rows as a header:

```
data
│ 
├── annotation_info
│   ├── annoations_stats
│   │   ├── creators.tsv 					# amazon mturk annotator statistics (data annotators)
│   │   └── validation.tsv 					# amazon mturk annotator statistics (data validators)
│   └── templates
│       ├── annotation-template1.html 				# annotation template example 1 
│       ├── annotation-template2.html 				# annotation template example 2 
│       ├── annotation-template3.html 				# annotation template example 3 
│       ├── annotation-template4.html 				# annotation template example 4 
│       └── validation-template.html 				# validation template
│
├── maindata							# primary infotabs dataset folder
│   ├── infotabs_dev.tsv 					# development datasplit
│   ├── infotabs_test_alpha1.tsv 				# test alpha1 datasplit
│   ├── infotabs_test_alpha2.tsv 				# test alpha2 datasplit
│   ├── infotabs_test_alpha3.tsv 				# test alpha3 datasplit
│   └── infotabs_train.tsv 					# training dataset
│
├── reasoning 							# reasoning statistic folder
│   ├── infotabs_dev.tsv 					# reasoning on subset of development datasplit
│   └── infotabs_test_alpha3.tsv 				# reasoning on subset of alpha3 datasplit
│
├── tables 							# tables folder
│   ├── html 							# tables premises in html format
│   │   ├── T0.html
│   │   ├── T1000.html
│   │   ├── T1001.html
│   │   ├── T998.html
│   │   ├── T999.html
│   │   ├── T99.html
│   │   └── T9.html
│   │
│   ├── json							# tables premises in json format
│   │   ├── T0.json
│   │   ├── T1000.json
│   │   ├── T1001.json
│   │   ├── T1002.json
│   │   ├── T999.json
│   │   ├── T99.json
│   │   └── T9.json
│   └── table_categories.tsv 					# table categories
│   		  
├── validation 							# validation annotations folder
│   ├── infotabs_valid_dev.tsv 					# validation annotations development dataset
│   ├── infotabs_valid_test_alpha1.tsv 				# validation alpha1 annotations datasplit
│   ├── infotabs_valid_test_alpha2.tsv 				# validation alpha2 annotations datasplit
│   └── infotabs_valid_test_alpha3.tsv 				# validation alpha3 annotations datasplit
│
└── LICENSE, Datasheet, README.md, logo				#license,datasheet,dataset readme, logo files.

```

For the code, check out [here](https://github.com/utahnlp/infotabs-code). Note : Wherever require consider year 2019 as the build date for the dataset.
