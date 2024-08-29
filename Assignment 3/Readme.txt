All 5 test Cases and its Buggy file are present in tests folder under ChironCore folder.


5 test Cases are named as:-
	test1.tl	test1bug.tl		contains 3 variables x,y,z
	test2.tl	test2bug.tl		contains 2 variables x,y
	test3.tl	test3bug.tl		contains 3 variables x,y,z
	test4.tl	test4bug.tl		contains 3 variables x,y,z
	test5.tl	test5bug.tl		contains 2 variables x,y

To run sbflSubmission.py file use,
	python ./chiron.py --SBFL ./tests/sbfl1.tl --buggy ./tests/sbfl1_buggy.tl -vars '[":x", ":y", ":z"]' --timeout 10 --ntests 20 --popsize 100 --cxpb 1.0 --mutpb 1.0 --ngen 100 --verbose True 

