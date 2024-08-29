#!/usr/bin/env python3

import argparse
import sys
import numpy as np

from math import sqrt
from operator import itemgetter

sys.path.insert(0, "../ChironCore/")
from irhandler import *
from ChironAST.builder import astGenPass
import csv


def fitnessScore(IndividualObject):
    """
    Parameters
    ----------
    IndividualObject : Individual (definition of this class is in ChironCore/sbfl.py)
        This is a object of class Individual. The Object has 3 elements
        1. IndividualObject.individual : activity matrix.
                                    type : list, row implies a test
                                    and element of rows are components.
        2. IndividualObject.fitness : fitness of activity matix.
                                    type : float
        3. Indivisual.fitness_valid : a flag used by Genetic Algorithm.
                                    type : boolean
    Returns
    -------
    fitness_score : flaot
        returns the fitness-score of the activity matrix.
        Note : No need to set/change fitness and fitness_valid attributes.
    """
    # Design the fitness function
    fitness_score = 0
    activity_mat = np.array(IndividualObject.individual, dtype="int")
    activity_mat = activity_mat[:, : activity_mat.shape[1] - 1]
    # Use 'activity_mat' to compute fitness of it.
    # ToDo : Write your code here to compute fitness of test-suite

    
    #DENSITY
    no_of_ones = 0
    for i in range(0,len(activity_mat)):
        for j in range(0,len(activity_mat[i])):
            no_of_ones+=activity_mat[i][j]

    total_ones = len(activity_mat)*len(activity_mat[0])
    density = no_of_ones/total_ones
    density_updated = 1 - abs(1 - 2*density)

    #DIVERSITY
    act_cnt = {}
    total_nk = 0
    for row in activity_mat:
        actv = tuple(row)
        if actv in act_cnt:
            act_cnt[actv] += 1
        else:
            act_cnt[actv] = 1
    
    for value in act_cnt.values():
        total_nk += value*(value-1)
    length=len(activity_mat)
    if(length!=1):
        diversity = 1 - (total_nk/(length*(length-1)))
    else:
        diversity = 1

    #UNIQUENESS
    act_grp={}
    for i in range (0,len(activity_mat)):
        grp=[]
        for j in range (0,len(activity_mat[0])):
            grp.append(activity_mat[i][j])
        temp = tuple(grp)
        if temp in act_grp:
            act_grp[temp] += 1
        else:
            act_grp[temp] = 1

    act_group = len(act_grp)
    unique = act_group/len(activity_mat[0])

    fitness_score = density_updated * diversity * unique
    fit_sc = fitness_score*-1
    return fit_sc


# This class takes a spectrum and generates ranks of each components.
# finish implementation of this class.
class SpectrumBugs:
    def __init__(self, spectrum):
        self.spectrum = np.array(spectrum, dtype="int")
        self.comps = self.spectrum.shape[1] - 1
        self.tests = self.spectrum.shape[0]
        self.activity_mat = self.spectrum[:, : self.comps]
        self.errorVec = self.spectrum[:, -1]

    def getActivity(self, comp_index):
        """
        get activity of component 'comp_index'
        Parameters
        ----------
        comp_index : int
        """
        return self.activity_mat[:, comp_index]

    def suspiciousness(self, comp_index):
        """
        Parameters
        ----------
        comp_index : int
            component number/index of which you want to compute how suspicious
            the component is. assumption: if a program has 3 components then
            they are denoted as c0,c1,c2 i.e 0,1,2
        Returns
        -------
        sus_score : float
            suspiciousness value/score of component 'comp_index'
        """
        sus_score = 0

        comp_activity = [row[comp_index] for row in self.activity_mat]
        
        # Implementing ochiai metric
        cf=0
        cp=0
        nf=0
          
        cf = sum(1 for i in range(len(comp_activity)) if self.errorVec[i] == 1 and comp_activity[i] == 1 )
        cp = sum(1 for i in range(len(comp_activity)) if self.errorVec[i] == 0 and comp_activity[i] == 1 )
        nf = sum(1 for i in range(len(comp_activity)) if self.errorVec[i] == 1 and comp_activity[i] == 0 )

        if((cf+nf)*(cf+cp)!=0):
            sus_score = cf/sqrt((cf+nf)*(cf+cp))
        print(sus_score)
        return sus_score

    def getRankList(self):
        """
        find ranks of each components according to their suspeciousness score.

        Returns
        -------
        rankList : list
            ranList will contain data in this format:
                suppose c1,c2,c3,c4 are components and their ranks are
                1,2,3,4 then rankList will be :
                    [[c1,1],
                     [c2,2],
                     [c3,3],
                     [c4,4]]
        """

        rankList = []
        # ToDo : implement rankList
        r_temp=[]
        for i in range(0, len(self.activity_mat[0])):
            sus_list=[]
            sus_list.append('c'+str(i+1))
            sus_list.append(self.suspiciousness(i))
            r_temp.append(sus_list)
        rankList = sorted(r_temp, key=lambda x: x[1], reverse=True)
        print(rankList)
        rank = 0
        prev_value = None

        result_with_ranks = []

        for item in rankList:
            if item[1] != prev_value:
                rank += 1
            result_with_ranks.append([item[0], rank])
            prev_value = item[1]  
        print(result_with_ranks)   
        return result_with_ranks


# do not modify this function.
def computeRanks(spectrum, outfilename):
    """
    Parameters
    ----------
    spectrum : list
        spectrum
    outfilename : str
        components and their ranks.
    """
    S = SpectrumBugs(spectrum)
    rankList = S.getRankList()
    with open(outfilename, "w") as file:
        writer = csv.writer(file)
        writer.writerows(rankList)
