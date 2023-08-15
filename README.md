# InfoSync
<!-- <p align="center"><img width="80%" src="logo.png" /></p> -->

If you use our dataset, please cite our ACL 2023 paper: [InfoSync: Information Synchronization across Multilingual Semi-structured Tables](https://vgupta123.github.io/docs/infosync_paper.pdf).

```
@inproceedings{khincha-etal-2023-infosync,
    title = "{I}nfo{S}ync: Information Synchronization across Multilingual Semi-structured Tables",
    author = "Khincha, Siddharth  and
      Jain, Chelsi  and
      Gupta, Vivek  and
      Kataria, Tushar  and
      Zhang, Shuo",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2023",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-acl.159",
    pages = "2536--2559",
    abstract = "Information Synchronization of semi-structured data across languages is challenging. For example, Wikipedia tables in one language need to be synchronized with others. To address this problem, we introduce a new dataset InfoSync and a two-step method for tabular synchronization. InfoSync contains 100K entity-centric tables (Wikipedia Infoboxes) across 14 languages, of which a subset ({\textasciitilde}3.5K pairs) are manually annotated. The proposed method includes 1) Information Alignment to map rows and 2) Information Update for updating missing/outdated information for aligned tables across multilingual tables. When evaluated on InfoSync, information alignment achieves an F1 score of 87.91 (en {\textless}-{\textgreater} non-en). To evaluate information updation, we perform human-assisted Wikipedia edits on Infoboxes for 532 table pairs. Our approach obtains an acceptance rate of 77.28{\%} on Wikipedia, showing the effectiveness of the proposed method.",
} 
```

```
Note :- This repository is still under construction. Please wait until this note has been removed before using the associated data or code.
```

Carefully read the LICENCE and the Datasheet for non-academic usage. 

After downloading, you have multiple sub-folders with several csv/html/json files. Each csv file in the sub-folders has 1st rows as a header:

```
data
│ 
├── tables
│   ├── json				    # contains json data for all the categories. Files are in html format for easies understanding of the data
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
|
│   └── html                                # data scraped for all the categories
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |
│   |   | 
│
|
├── final_test_set		            # test set, built using semi-automated pipeline. Annotated by humans using translations
│   ├── Final_Test_Set_Eng_X 		    # contains files for Eng_X for all categories
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
│   ├── Final_Test_Set_X_Y 	            # contains files for X_Y for all categories
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
│   ├── Final_Test_Set_Eng_X.json 	    # json file with all annotations for Eng_X
│   └── Final_Test_Set_X_Y.json 	    # json file with all annotations for X_Y
│
│
├── true_test_set			    # true-test-set, annotated by native speakers of Hindi and Chinese without using translations
│   ├── True_Test_Set_HI 		    # contains files for Eng_HI for all categories
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
│   ├── True_Test_Set_ZH 		    # contains files for Eng_ZH for all categories
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
│   ├── True_Test_Set_HI.json 	            # json file with all annotations for Eng_HI
│   └── True_Test_Set_ZH.json 		    # json file with all annotations for Eng_ZH
|
|
├── metadata                       # Human annotators also classify the types of errors present in the test data in one of the five categories 1) Disambiguation 2) Multiple alignments 3) Partial or incorrect extraction 4) Wrong_translations 5) Key Paraphrasing. This evaluation helps standardizing and comparing update methods against each other.
│   ├── Metadata_Eng_X
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|
│   ├── Metadata_X_Y
│   |   ├── Airport 	            
│   |   |   ├── NioroAirport
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   | 		            
│   |   ├── Company
│   |   |   ├── WellsFargo
│   |   |   |   ├── en
│   |   |   |   |   ├── table.html
│   |   |   |   ├── fr
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   ├── es
│   |   |   |   |   ├── table.html
│   |   |   |   |   ├── updated.html
│   |   |   |   |
│   |   |
|	
│   ├── Metadata_Eng_X.json 							
|   └── Metadata_X_Y.json 
│
├── updation_data				    # this folder contains json file which are finally used to execute the update algorithm
│   ├── Gold.json                   # "Gold.json" comprises alignments sourced from the final_test_set that have undergone meticulous human annotation.
│   ├── Live.json                   # "Live.json" is generated by executing our alignment pipeline on the live-updates dataset. This file captures the alignments produced by our automated process when applied to real-time data updates.
│   ├── Model.json                 # "Model.json" contains alignments derived from the final_test_set prior to undergoing any human annotation. These alignments originate directly from our automated alignment model.
|
|
├── csv_data				    # csv data for all categories, with links for different wikipedia pages
│   ├── Airport
│   ├── Person
│   ├── Planet
│   ├── Company
|   |
│
└── LICENSE, Datasheet, README.md, logo	    #license,datasheet,dataset readme, logo files.

```
Note - Due to the large size of tree structure for the data it is partially listed to give reader an idea of folder organization.
For the code, check out [here](https://github.com/Info-Sync/InfoSync/tree/main/scripts). Note : Wherever require consider year End of year 2022 as the build date for the dataset.
