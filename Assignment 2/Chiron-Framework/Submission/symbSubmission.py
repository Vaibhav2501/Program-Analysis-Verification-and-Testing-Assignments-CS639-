from z3 import *
import argparse
import json
import sys

sys.path.insert(0, "../KachuaCore/")

from sExecutionInterface import *
import z3solver as zs
from irgen import *
from interpreter import *
import ast

from sympy import symbols, Eq, solve, parse_expr


def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar("x")
    s.addSymbVar("y")
    # To add constraint in form of string
    s.addConstraint("x==5+y")
    s.addConstraint("And(x==y,x>5)")
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now", s.s.assertions())
    # To assign z=x+y
    s.addAssignment("z", "x+y")
    # To get any variable assigned
    print("variable assignment of z =", s.getVar("z"))


def checkEq(args, ir):

    file1 = open("../Submission/testData3_1.json", "r+")
    testData = json.loads(file1.read())
    file1.close()
    testData = convertTestData(testData)
    file2 = open("../Submission/testData3_2.json", "r+")
    testData2 = json.loads(file2.read())
    file2.close()
    # s = zs.z3Solver()
    s = Solver()
    testData2 = convertTestData(testData2)

    
    # Fetch TestCases
    y = Int('y')
    x = Int('x')
    k = Int('k')
    z = Int('z')
    c1 = Int('c1')
    c2 = Int('c2')
    c3 = Int('c3')
    c4 = Int('c4')
    c5 = Int('c5')
    c6 = Int('c6')
    c7 = Int('c7')
    c8 = Int('c8')
    c9 = Int('c9')
    c10 = Int('c10')
   
    # FOR TESTDATA.JSON P2
    parameter_P2 = {}
    SymbEnc_P2 = {}

    for key, value in testData2.items():
        parameter_P2[key] = value.get("params")

    for key, value in testData2.items():
        SymbEnc_P2[key] = value.get("symbEnc")

    input_P2 = []
    for value in parameter_P2:
        input_P2.append(parameter_P2[value])

    output_P2 = []
    for value in SymbEnc_P2:
        output_P2.append(SymbEnc_P2[value])


    input_eq_P2 = []
    for i_iterate in input_P2:
        list = []
        for j_iterate, k_iterate in i_iterate.items():
            list.append((j_iterate + "==" + str(k_iterate)))
        input_eq_P2.append(list)
 


    input_AND_P2 = []
    for i_iterate in input_eq_P2:
        A = True
        for j_iterate in i_iterate:
           
            A = And(A, eval(j_iterate))
        input_AND_P2.append(A)
        
    
    output_eq_P2 = []
    for i_iterate in output_P2:
        list = []
        for j_iterate, k_iterate in i_iterate.items():
            list.append(j_iterate + "==" + str(k_iterate))
        output_eq_P2.append(list)




    # FOR TESTDATA.JSON P1
    constraints_P1 = {}
    symbEnc_P1 = {}
    for key, value in testData.items():
        constraints_P1[key] = value.get("constraints")

    for key, value in testData.items():
        symbEnc_P1[key] = value.get("symbEnc")

 
    equations_dict_P1 = []
    for var in symbEnc_P1:
        equations_dict_P1.append(symbEnc_P1[var])  

    constr=[]
    for i in testData.keys():
        constr.append(testData[i]['constraints'][0].split(','))


    constraint_new=[]
    conditions_AND_P1 = []

    for i_iterate in constr:
        A = True
        list1=[]
        for j in i_iterate:
            list1.append(eval(str(j)))
        constraint_new.append(list1)

        for j_iterate in list1:
            A = And(A, eval(str(j_iterate)))
           
        conditions_AND_P1.append(A)


    eq1 = []
    list = []
  
    n = 0
    m = 0
    for i_iterate in symbEnc_P1:
        list = []
       
        for j_iterate in symbEnc_P1[i_iterate]:
            list.append("==" + symbEnc_P1[i_iterate][j_iterate])
        eq1.append(list)
        

    n = 0
    eq_P1 = []
    for k_iterate in output_P2:
        list = []
        m = 0
        for key in k_iterate:
            list.append(k_iterate[key] + eq1[n][m])
            m = m + 1
        eq_P1.append(list)
        n = n + 1



    # Fetch TestCases
    parameter_P1 = {}

    for key, value in testData.items():
        parameter_P1[key] = value.get("params")

    input_p1 = []
    for var in parameter_P1:
        input_p1.append(parameter_P1[var])

    input_eq_P1 = []
    for i in input_p1:
        list = []
        for j, k1 in i.items():
            list.append(j + "==" + str(k1))
        input_eq_P1.append(list)

    Symb3 = {}

    for key, value in testData.items():
        Symb3[key] = value.get("symbEnc")

    output_P1 = []
    for var in Symb3:
        output_P1.append(Symb3[var])

    output_eq_P1 = []
    for i in output_P1:
        list = []
        for j, k1 in i.items():
            list.append(j + "==" + str(k1))
        output_eq_P1.append(list)

 

    s1=Solver()
    s2=Solver()
    y = Int('y')
    x = Int('x')
    k = Int('k')
    z = Int('z')
    c1 = Int('c1')
    c2 = Int('c2')
    c3 = Int('c3')
    c4 = Int('c4')
    c5 = Int('c5')
    c6 = Int('c6')
    c7 = Int('c7')
    c8 = Int('c8')
    c9 = Int('c9')
    c10 = Int('c10')
   
    for i in range(len(input_AND_P2)):
        for j in range(len(conditions_AND_P1)):
            s1.reset()
            anding = And((input_AND_P2[i]),(conditions_AND_P1[j]))
            s1.add(anding)
            result = s1.check()
            
            if result == sat:
                temp = output_eq_P2[i]
                temp2 = output_eq_P1[j]

                dict_output={}
                for iterate in temp:
                   key, value = iterate.split('==')
                   dict_output[key.strip()] = value.strip()
                
                dict_equation={}
                for iterate in temp2:
                   key, value = iterate.split('==')
                   dict_equation[key.strip()] = value.strip()

                expression_list=[]
        
                for key1 , value1 in dict_output.items():
                    for key2 , value2 in dict_equation.items():
                        if key1 == key2:                        
                            expression_list.append(eval(str(dict_output[key1] + "==" + dict_equation[key2])))              
                for var in expression_list:
                    s2.add(var)    

    result = s2.check()
    if result == sat:
        model=s2.model()
        print("model",model)

# output = args.output
# example(s)
# TODO: write code to check equivalence


if __name__ == "__main__":
    cmdparser = argparse.ArgumentParser(
        description="symbSubmission for assignment Program Synthesis using Symbolic Execution"
    )
    cmdparser.add_argument("progfl")
    cmdparser.add_argument("-b", "--bin", action="store_true", help="load binary IR")
    cmdparser.add_argument(
        "-e",
        "--output",
        default=list(),
        type=ast.literal_eval,
        help="pass variables to kachua program in python dictionary format",
    )
    args = cmdparser.parse_args()
    ir = loadIR(args.progfl)
    checkEq(args, ir)
    exit()
