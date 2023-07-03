# InfoSync
<!-- <p align="center"><img width="80%" src="logo.png" /></p> -->

If you use our dataset, please cite our ACL 2023 paper: [INFOSYNC: Information Synchronization across Multilingual Semi-structured Tables](https://vgupta123.github.io/docs/infosync_paper.pdf).

```
TO  BE ADDED
```

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
│   ├── Final_Test_Set_Eng_X.json 		# json file with all annotations for Eng_X
│   └── Final_Test_Set_X_Y.json 		# json file with all annotations for X_Y
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

For the code, check out [here](https://github.com/Info-Sync/InfoSync/tree/main/scripts). Note : Wherever require consider year End of year 2022 as the build date for the dataset.
