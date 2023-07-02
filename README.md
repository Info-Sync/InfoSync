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
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics",
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
├── tables
│   ├── json				                # contains json data for all the categories. Files are in html format for easies understanding of the data
│   └── html                                # data scraped for all the categories
│
├── final_test_set							# test set, built using semi-automated pipeline. Annotated by humans using translations
│   ├── Final_Test_Set_Eng_X 				# contains files for Eng_X for all categories
│   ├── Final_Test_Set_X_Y 				    # contains files for X_Y for all categories
│   ├── Final_Test_Set_Eng_X.json 			# json file with all annotations for Eng_X
│   └── Final_Test_Set_X_Y.json 			# json file with all annotations for X_Y
│
│
├── true_test_set						    # true-test-set, annotated by native speakers of Hindi and Chinese without using translations
│   ├── True_Test_Set_HI 					# contains files for Eng_HI for all categories
│   ├── True_Test_Set_ZH 				    # contains files for Eng_ZH for all categories
│   ├── True_Test_Set_HI.json 			    # json file with all annotations for Eng_HI
│   └── True_Test_Set_ZH.json 			    # json file with all annotations for Eng_ZH
|
├── metadata 							    # metadata for error analysis
│   ├── Metadata_Eng_X 
│   ├── Metadata_X_Y						
│   ├── Metadata_Eng_X.json 							
|   └── Metadata_X_Y.json 
│   		  
├── csv_data						        # csv data for all categories, with links for different wikipedia pages
│
└── LICENSE, Datasheet, README.md, logo		#license,datasheet,dataset readme, logo files.

```

For the code, check out [here](https://github.com/Info-Sync/InfoSync/tree/main/scripts). Note : Wherever require consider year 2020 as the build date for the dataset.
