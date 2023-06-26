# InfoSync
<!-- <p align="center"><img width="80%" src="logo.png" /></p> -->

If you use our dataset, please cite our ACL 2020 paper: [INFOTABS: Inference on Tables as Semi-structured Data](https://www.aclweb.org/anthology/2020.acl-main.210.pdf). To explore the dataset online visit [project page](https://infotabs.github.io).

```
@inproceedings{gupta-etal-2020-infotabs,
    title = "{INFOTABS}: Inference on Tables as Semi-structured Data",
    author = "Gupta, Vivek  and
      Mehta, Maitrey  and
      Nokhiz, Pegah  and
      Srikumar, Vivek",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.210",
    pages = "2309--2324",
    abstract = "In this paper, we observe that semi-structured tabulated text is ubiquitous; understanding them requires not only comprehending the meaning of text fragments, but also implicit relationships between them. We argue that such data can prove as a testing ground for understanding how we reason about information. To study this, we introduce a new dataset called INFOTABS, comprising of human-written textual hypotheses based on premises that are tables extracted from Wikipedia info-boxes. Our analysis shows that the semi-structured, multi-domain and heterogeneous nature of the premises admits complex, multi-faceted reasoning. Experiments reveal that, while human annotators agree on the relationships between a table-hypothesis pair, several standard modeling strategies are unsuccessful at the task, suggesting that reasoning about tables can pose a difficult modeling challenge.",
}
```

Carefully read the LICENCE and the Datasheet for non-academic usage. 

After downloading, you have multiple sub-folders with several csv/tsv/html files. Each csv/tsv file in the sub-folders has 1st rows as a header:

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
