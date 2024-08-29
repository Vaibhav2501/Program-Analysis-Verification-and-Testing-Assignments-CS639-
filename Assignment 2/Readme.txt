All 5 test Cases and its corresponding output images are present in tests folder under KachuaCore folder.

Generate JSON File for both P1 and P2.

5 test Cases are named as:-
	eqtest1_1	eqtest1_2
	eqtest2_1	eqtest2_2
	eqtest3_1	eqtest3_2
	eqtest4_1	eqtest4_2
	eqtest5_1	eqtest5_2

JSON files of each test case file is named as:-
	testData1_1	testData1_2
	testData2_1	testData2_2
	testData3_1	testData3_2
	testData4_1	testData4_2
	testData5_1	testData5_2

eqtest2.kw file is present in Submission Folder

To generate JSON file use, go to KachuaCore directory
	
	For program with unknown holes :- python ./kachua.py -t 100 -se tests/eqtest5_1.tl -d '{\":x\": 40, \":y\": 120, \":z\": 80}' -c '{\":c1\": 10, \":c2\": 20, \":c3\": 30, \":c4\": 40}'

	For program with no holes :- python ./kachua.py -t 100 -se tests/eqtest5_1.tl -d '{\":x\": 40, \":y\": 120, \":z\": 80}' 

To generate kw file use,
	python kachua.py -O filename.

To run symbSubmission.py file use,
	python symbSubmission.py -b eqtest2.kw -e '[\"x\", \"y\"]'

