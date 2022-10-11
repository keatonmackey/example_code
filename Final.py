#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:06:14 2022

@author: keatonmackey
"""


import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


# define input sheet
path = '/Users/keatonmackey/Desktop/FullDF329_newCols.csv'

def csvToDataframe(path):
    dataFrame = pd.read_csv(path) #read the document into the code
    return dataFrame



def makeNewDataFrame(compareConditions, dataframe): #more specific graph
    filter1 = dataframe['Cond'].isin(compareConditions) #this dataframe is used for the new specialized paired graph
    conditionDataFrame = dataframe[filter1] #returns new dataframe
    return conditionDataFrame

def plotter(newDataFrame, scoringVariable):
    lf = ttk.Labelframe(root, text='Plot Area') #creates new place to put plot
    lf.grid(row=20, column=1, sticky='nwes', padx=1, pady=1)
    fig = Figure(figsize=(4,4), dpi=100)
    plot = fig.add_subplot(111)
    newDataFrame.boxplot(column = scoringVariable, by = 'Cond', ax = plot) #plots based on condition and score variable, based on clicked conditions
    canvas = FigureCanvasTkAgg(fig, master=lf) #will put into master root
    canvas.draw()
    canvas.get_tk_widget().grid(row=20, column=1) #grid placement
    return 


def plotterEXTRA(newDataFrame, scoringVariable, extraFactor):
    """this is for paired boxplots only, the first part will be used within the tkinter window, the boxplot
    itself is the sns.boxplot part"""
    lf = ttk.Labelframe(root, text='Plot Area')
    lf.grid(row=20, column=1, sticky='nwes', padx=1, pady=1)
    fig = Figure(figsize=(4,4), dpi=100)
    plot = fig.add_subplot(111)
    sns.boxplot(x = newDataFrame['Cond'], y = newDataFrame[scoringVariable],
                hue = newDataFrame[extraFactor], ax = plot)
    canvas = FigureCanvasTkAgg(fig, master=lf)
    canvas.draw()
    canvas.get_tk_widget().grid(row=20, column=1)
    return 

def plotterOther(dataframe,differentiationBy, scoringVariable):
    lf = ttk.Labelframe(root, text='Plot Area') #creates place to put graph
    lf.grid(row=20, column=1, sticky='nwes', padx=1, pady=1)
    fig = Figure(figsize=(4,4), dpi=100)
    plot = fig.add_subplot(111)
    dataframe.boxplot(column = scoringVariable, by = differentiationBy, ax = plot) #this is based on the binary elements of pre/post or b1/b2 versus the other condition based graph
    canvas = FigureCanvasTkAgg(fig, master=lf)
    canvas.draw()
    canvas.get_tk_widget().grid(row=20, column=1)
    return 

def tTest(dataframe, differentiationBy, scoringVariable):
    """This function will run a t Test on binary elements (this is an independent t test) and it will return
    the t test statistic and p value. It does this by pulling elements from the dataframe and ommitting any NAs"""
    if differentiationBy == 'Assigned_Order_Block': 
        Cyber = dataframe.loc[dataframe['Assigned_Order_Block']== 'B1']
        NonCyber = dataframe.loc[dataframe['Assigned_Order_Block']== 'B2']
        CyberScoreVar = Cyber[scoringVariable]
        nonCyberScoreVar = NonCyber[scoringVariable]
        statsP = sp.stats.ttest_ind(CyberScoreVar, nonCyberScoreVar, nan_policy='omit')
        statsT = ('t statistics =', str(statsP[0]), 'p value =', str(statsP[1]))
    elif differentiationBy == 'Pre_Post': 
        Pre = dataframe[dataframe[differentiationBy] == 'Pre']
        Post = dataframe[(dataframe[differentiationBy] == 'Post')]
        preScoreVar = Pre[scoringVariable]
        postScoreVar = Post[scoringVariable]
        statsP = sp.stats.ttest_ind(preScoreVar, postScoreVar, nan_policy='omit')
        statsT = ('t statistics =', str(statsP[0]), 'p value =', str(statsP[1]))
    elif differentiationBy == 'STEM': 
        nonStem = dataframe[dataframe[differentiationBy] == 0]
        Stem = dataframe[(dataframe[differentiationBy] == 1)]
        preScoreVar = nonStem[scoringVariable]
        postScoreVar = Stem[scoringVariable]
        statsP = sp.stats.ttest_ind(preScoreVar, postScoreVar, nan_policy='omit')
        statsT = ('t statistics =', str(statsP[0]), 'p value =', str(statsP[1]))
    elif differentiationBy == 'Cyber': 
        nonCyb = dataframe[dataframe[differentiationBy] == 0]
        Cyb = dataframe[(dataframe[differentiationBy] == 1)]
        preScoreVar = nonCyb[scoringVariable]
        postScoreVar = Cyb[scoringVariable]
        statsP = sp.stats.ttest_ind(preScoreVar, postScoreVar, nan_policy='omit')
        statsT = ('t statistics =', str(statsP[0]), 'p value =', str(statsP[1]))
    else:
        statsT = 'Nope'
    return statsT

def largeFunction(differentiationBy, scoringVariable, compareConditions, extraFactor, dataframe, secondDiffBy, testType):
    """This large function will be used within the submit button and the input will be 
    defined with the submit button function. This is essentially a tree depending on which inputs the user chooses. 
    because we cannot do t tests on non binary elements, when a user chooses this, it will simply not work or return just plots needed"""
    if differentiationBy == 'Condition':
        if extraFactor == 'No':
            newDataFrame = makeNewDataFrame(compareConditions, dataframe)
            plotter(newDataFrame, scoringVariable)
            statsT = ['Plots!']
        elif extraFactor != 'No':
          newDataFrame = makeNewDataFrame(compareConditions, dataframe)
          plotterEXTRA(newDataFrame, scoringVariable, extraFactor)
          statsT = ['Plots!']
    elif differentiationBy != 'Condition':
        if testType == 'T Test': 
            statsT = tTest(dataframe, secondDiffBy, scoringVariable)
        elif testType == 'Plots':
            plotterOther(dataframe,secondDiffBy, scoringVariable)
            statsT = 'Plots'
        elif testType == 'Both':
            plotterOther(dataframe,secondDiffBy, scoringVariable)
            statsT = tTest(dataframe, secondDiffBy, scoringVariable)
    else:
        statsT = 'Nope'
    return statsT


"""This below part is all of the graphical user interface aspect!"""


root=tk.Tk() #creates window
root.geometry("1220x400") #geometry of window
root.title('Platt Labs Adventure') #title of window




""" this is all of the score variables -- they will use the same integer based variables and the function it 
is called will be a large if/elif statment based on what they chose-- all names are from the dataframe"""
ScoreVar = tk.IntVar()
ScoreVar.set(0)

def scoreVariable_change():
    if ScoreVar.get() == 1:
        scoreVariableFunc = 'PK_attacker_points'
    elif ScoreVar.get() == 2:
        scoreVariableFunc = 'PK_defender_points'
    elif ScoreVar.get() == 3:
        scoreVariableFunc = 'Forager_total_reward'
    elif ScoreVar.get() == 4:
        scoreVariableFunc = 'Letter_Number_Switching_score'
    elif ScoreVar.get() == 5:
        scoreVariableFunc = 'N_Back_Outcomes_errorCount'
    elif ScoreVar.get() == 6:
        scoreVariableFunc = 'Trail_Making_score'
    elif ScoreVar.get() == 7:
        scoreVariableFunc = 'Multiple_Object_Tracking_score'
    elif ScoreVar.get() == 8:
        scoreVariableFunc = 'Delay_k_delta'
    else:
        scoreVariableFunc = 'please try again'
    return scoreVariableFunc
    
"""This is the creation of all the button, the text names them, the value corresponds to the function.
Because this is a radio button, only one can be clicked. I have no found out a way to compare all score variables!"""
pkAttackCheck = ttk.Radiobutton(root, text = 'PK Score: Attack', value = 1,
                                command = scoreVariable_change, variable = ScoreVar)
pkDefendCheck = ttk.Radiobutton(root, text = 'PK Score: Defend',value = 2,  command = scoreVariable_change, 
                variable = ScoreVar)
foragerCheck = ttk.Radiobutton(root, text = 'Forager Score ', value = 3, command = scoreVariable_change, 
                variable = ScoreVar)
letnumbCheck = ttk.Radiobutton(root, text = 'Letter Number Switch Score',value = 4, command = scoreVariable_change, 
                variable = ScoreVar)
multiobjCheck = ttk.Radiobutton(root, text = 'Multiple Object Tracking Score', value = 7, command = scoreVariable_change, 
                variable = ScoreVar)
nbackCheck = ttk.Radiobutton(root, text = 'N-Back Score ', value = 5, command = scoreVariable_change, 
                variable = ScoreVar)
trailMakeCheck = ttk.Radiobutton(root, text = 'Trail Making Score',value = 6, command = scoreVariable_change, 
                variable = ScoreVar)
adaptDelayCheck = ttk.Radiobutton(root, text = 'Adaptive Delay Score',value = 8, command = scoreVariable_change, 
                variable = ScoreVar)

"""This is the options the user has if they are not choosing stress condition based tests. This follows the same breakdown
as all the other buttons. It is an integer based system ."""
#Non Condition:
nonCondGroupVar = tk.IntVar()
nonCondGroupVar.set(0)


def nonConditions_Change():
    if nonCondGroupVar.get() == 1:
        nonCondition = 'Pre_Post'
    elif nonCondGroupVar.get() == 2:
        nonCondition = 'Assigned_Order_Block'
    elif nonCondGroupVar.get() == 3:
        nonCondition = 'STEM'
    elif nonCondGroupVar.get() == 4:
        nonCondition = 'Cyber'
    else:
        nonCondition = 'please try again'
    return nonCondition


"""This is the creation of all the button, the text names them, the value corresponds to the function.
Because this is a radio button, only one can be clicked. I have no found out a way to compare all conditions variables!"""
prePostCheck = ttk.Radiobutton(root, text = 'Pre/Post', value = 1, command = nonConditions_Change, 
                variable = nonCondGroupVar)
blockCheck = ttk.Radiobutton(root, text = 'B1/B2',value = 2, command = nonConditions_Change, 
                variable = nonCondGroupVar)
stemCheckFirst = ttk.Radiobutton(root, text = 'STEM',value = 3, command = nonConditions_Change, 
                variable = nonCondGroupVar)
cyberCheckFirst = ttk.Radiobutton(root, text = 'Cyber',value = 4, command = nonConditions_Change, 
                variable = nonCondGroupVar)

#Conditions:
"""this is a string variables so pressing it will push an on value of a string which is how I used the add list function.
This also means the user is permitted to click multiple. """
    
preTestMathVar = tk.StringVar()
postTestMathVar = tk.StringVar()
preControlMathVar = tk.StringVar()
postControlMathVar = tk.StringVar()
preTestTrierVar = tk.StringVar()
postTestTrierVar = tk.StringVar() 
preControlTrierVar = tk.StringVar()
postControlTrierVar = tk.StringVar() 
preTestSASVar = tk.StringVar()
postTestSASVar = tk.StringVar() 
preControlSASVar = tk.StringVar()
postControlTSASVar = tk.StringVar() 

varList = [preTestMathVar, postTestMathVar, preControlMathVar, postControlMathVar, preTestTrierVar, postTestTrierVar, 
           preControlTrierVar, postControlTrierVar, preTestSASVar, postTestSASVar, preControlSASVar, postControlTSASVar]
"""The function will create a list of the stress conditions the user wants to see in list format that will then go into the plotting function. 
This was actually easier than the user input based method!"""
def addtolist():
    List = []
    for item in varList:
        if item.get() != "":
            List.append(item.get())
    return List

"""All of these are defining the button. For the onvalue it is directly from the dataframe."""
preTestMathCheck = ttk.Checkbutton(root, text = 'Pre Test Math', onvalue = 'PreTestMath', offvalue = "", command = addtolist, 
                variable = preTestMathVar)
postTestMathCheck = ttk.Checkbutton(root, text = 'Post Test Math',onvalue = 'PostTestMath', offvalue = "", command = addtolist, 
                variable = postTestMathVar)
preControlMathCheck = ttk.Checkbutton(root, text = 'Pre Control Math', onvalue = 'PreControlMath', offvalue = "", command = addtolist, 
                variable = preControlMathVar)
postControlMathCheck = ttk.Checkbutton(root, text = 'Post Control Math', onvalue = 'PostControlMath', offvalue = "", command = addtolist, 
                variable = postControlMathVar)



preTestTrierCheck = ttk.Checkbutton(root, text = 'Pre Test Trier',onvalue = 'PreTestTrier', offvalue = "", command = addtolist, 
                variable = preTestTrierVar)
postTestTrierCheck = ttk.Checkbutton(root, text = 'Post Test Trier',onvalue = 'PostTestTrier', offvalue = "", command = addtolist, 
                variable = postTestTrierVar)
preControlTrierCheck = ttk.Checkbutton(root, text = 'Pre Control Trier',onvalue = 'PreControlTrier', offvalue = "" ,command = addtolist, 
                variable = preControlTrierVar)
postControlTrierCheck = ttk.Checkbutton(root, text = 'Post Control Trier',onvalue = 'PostControlTrier', offvalue = "" ,command = addtolist, 
                variable = postControlTrierVar)



preTestSASCheck = ttk.Checkbutton(root, text = 'Pre Test SAS', onvalue = 'PreTestSAS', offvalue = "", command = addtolist, 
                variable = preTestSASVar)
postTestSASCheck = ttk.Checkbutton(root, text = 'Post Test SAS',onvalue = 'PostTestSAS', offvalue = "", command = addtolist, 
                variable = postTestSASVar)
preControlSASCheck = ttk.Checkbutton(root, text = 'Pre Control SAS',onvalue = 'PreControlSAS', offvalue = "", command = addtolist, 
                variable = preControlSASVar)
postControlSASCheck = ttk.Checkbutton(root, text = 'Post Control SAS',onvalue = 'PostControlSAS', offvalue = "", command = addtolist, 
                variable = postControlTSASVar)

#Extra Factor Differentiation:
"""This is for the extra factor that would push a pair boxplot (which you can do only with the stress conditions. 
This is something I would like to continue to work on with someone with more knowledge on how to make this more efficient. But this follows the same structure as above. """
StemCyberVar = tk.IntVar()
StemCyberVar.set(0)
 
def extraFactor_change():
    if (StemCyberVar.get()==1):
        extraFactorFunc = 'STEM'
    elif (StemCyberVar.get()==2):
        extraFactorFunc = 'Cyber'
    elif (StemCyberVar.get()==0):
        extraFactorFunc = 'No'
    return extraFactorFunc

    

"""This is again, radio buttons, so only one of them can be clicked and it pushed a singular value (integer based)"""
stemCheck = ttk.Radiobutton(root, text = 'STEM',value = 1, command = extraFactor_change, 
                variable = StemCyberVar)
cyberCheck = ttk.Radiobutton(root, text = 'Cyber', value = 2, command = extraFactor_change, 
                variable = StemCyberVar)

#Test Type Buttons
"""These correspond to the test type buttons! This follows the same format at the above button based sections. 
Also they are not radio buttons so the user can choose both!"""
tTestVar = tk.IntVar()
boxPlotVar = tk.IntVar() 

 

def testType_change():
    if (tTestVar.get() == 1) & (boxPlotVar.get() == 1):
        testTypeFunc = 'Both'
    elif (tTestVar.get() == 1) & (boxPlotVar.get() == 0):
        testTypeFunc = 'T Test'
    elif (tTestVar.get() == 0) & (boxPlotVar.get() == 1):
        testTypeFunc = 'Plots'
    return testTypeFunc
        

    

    


tTestCheck = ttk.Checkbutton(root, text = 'T Test',onvalue = 1, offvalue = 0, command = testType_change, 
                variable = tTestVar)
PlotsCheck = ttk.Checkbutton(root, text = 'Boxplots', onvalue = 1, offvalue =0, command = testType_change, 
                variable = boxPlotVar)

#Differentiation By:
"""This is the first button which basically decides which way the program will go. So they either can choose the stress conditionals 
or they can choose the more binary variables. """
CondVar = tk.IntVar()
CondVar.set(0)


 

def differentiateBy_change():
    if (CondVar.get() == 1):
        DiffByFunc = "Non Conditions"
    elif (CondVar.get() == 2):
        DiffByFunc = 'Condition'
    return DiffByFunc

"""Follows the same radio button system and will push one of two values or if not, will stay on 0"""
nonStressCondCheck = ttk.Radiobutton(root, text = 'Not Stress Conditions', value = 1, command = differentiateBy_change, 
                variable = CondVar)
StressCondCheck = ttk.Radiobutton(root, text = 'Stress Conditions', value = 2, command = differentiateBy_change, 
                variable = CondVar)



#Sumbit Button
"""This is what happens when submit button is pushed. This almost acts as a main function. It will define all of 
the variables and then run the larger function. It will then put StatsT variable into the output text box. This 
was oddly structured so this is a place to come back to with the lab. """
def submit():
    dataframe = csvToDataframe(path)
    differentiationBy = differentiateBy_change()
    scoringVariable = scoreVariable_change()
    compareConditions = addtolist()
    extraFactor = extraFactor_change()
    secondDiffBy = nonConditions_Change()
    testType = testType_change()
    outPut = largeFunction(differentiationBy, scoringVariable, compareConditions, extraFactor, dataframe, secondDiffBy, testType)
    outputtxt.insert(tk.END, outPut)

submitButton = tk.Button(root, text = 'Submit', width = 10, command=submit, bg = 'blue', fg= 'red')
#output text: 
outputtxt = tk.Text(root, height = 5, width = 100, bg = 'light cyan')


"""All of the below code is creating labels and placing the buttons and labels within the grid!"""
titleLabel = tk.Label(root, text = 'Platt Labs Data Navigator', font = ('calibre', 18, "bold"))
conditionLabel = tk.Label(root, text = 'Which Kind of Conditions', font = ('calibre', 14, "bold"))
behavioralGamesLabel = tk.Label(root, text = 'Which Behavioral Game?', font = ('calibre', 14, "bold"))
nonStressLabel = tk.Label(root, text = 'Specific Differentiation', font = ('calibre', 14, "bold"))
stressLabel = tk.Label(root, text = "Specific Stress Conditions", font = ('calibre', 14, "bold"))
extraLabel = tk.Label(root, text = 'Extra Specifier', font = ('calibre', 14, "bold"))
testTypeLabel = tk.Label(root, text = "Test Type", font = ('calibre', 14, "bold"))


# Placing labels, entries, and buttons in the window
titleLabel.grid(row = 0, column = 2, pady = 2)
conditionLabel.grid(row = 1, column = 0)
nonStressCondCheck.grid(row = 2, column = 1)
StressCondCheck.grid(row = 2, column = 0)

behavioralGamesLabel.grid(row = 3, column = 0, pady = 2)
pkAttackCheck.grid(row = 4, column= 0, pady = 2)
pkDefendCheck.grid(row = 5, column = 0, pady = 2)
foragerCheck.grid(row = 4, column = 1, pady = 2)
letnumbCheck.grid(row = 5, column = 1, pady = 2)
multiobjCheck.grid(row = 4, column = 2, pady = 2)
nbackCheck.grid(row = 5, column = 2, pady = 2)
trailMakeCheck.grid(row = 4, column = 3, pady = 2)
adaptDelayCheck.grid(row = 5, column = 3, pady = 2)

nonStressLabel.grid(row = 6, column = 0, pady = 2)
prePostCheck.grid(row = 7, column = 0, pady = 2)
blockCheck.grid(row = 7, column = 1, pady = 2)
stemCheckFirst.grid(row = 7, column = 2, pady = 2)
cyberCheckFirst.grid(row = 7, column = 3, pady = 2)

stressLabel.grid(row = 8, column = 0)
preTestMathCheck.grid(row = 9, column = 0, pady = 2)
postTestMathCheck.grid(row = 9, column = 1, pady = 2)
preControlMathCheck.grid(row = 9, column = 2, pady = 2)
postControlMathCheck.grid(row = 9, column = 3, pady = 2)

preTestTrierCheck.grid(row = 11, column = 0, pady = 2)
postTestTrierCheck.grid(row = 11, column = 1,pady = 2)
preControlTrierCheck.grid(row = 11, column = 2, pady = 2)
postControlTrierCheck.grid(row = 11, column = 3, pady = 2)

preTestSASCheck.grid(row = 13, column = 0, pady = 2)
postTestSASCheck.grid(row = 13, column = 1, pady = 2)
preControlSASCheck.grid(row = 13, column = 2, pady = 2)
postControlSASCheck.grid(row = 13, column = 3, pady = 2)

extraLabel.grid(row = 16, column = 0, pady = 2)
stemCheck.grid(row = 17, column = 0, pady = 2)
cyberCheck.grid(row=17, column = 2, pady = 2)

testTypeLabel.grid(row = 18, column = 0, pady = 2)
tTestCheck.grid(row =19, column=0, pady = 2)
PlotsCheck.grid(row=19, column=2, pady = 2)

submitButton.grid(row = 21, column = 2, pady = 2)
outputtxt.grid(row=20, column = 2, pady = 2)



root.mainloop()

# Placing labels, entries, and buttons in the window
"""titleLabel.pack(side = LEFT)
conditionLabel.pack(side = LEFT)
nonStressCondCheck.pack()
StressCondCheck.pack()

behavioralGamesLabel.pack()
pkAttackCheck.pack()
pkDefendCheck.pack()
foragerCheck.pack()
letnumbCheck.pack()
multiobjCheck.pack()
nbackCheck.pack()
trailMakeCheck.pack()
adaptDelayCheck.pack()

nonStressLabel.pack()
prePostCheck.pack()
blockCheck.pack()
stemCheckFirst.pack()
cyberCheckFirst.pack()

stressLabel.pack()
preTestMathCheck.pack()
postTestMathCheck.pack()
preControlMathCheck.pack()
postControlMathCheck.pack()

preTestTrierCheck.pack()
postTestTrierCheck.pack()
preControlTrierCheck.pack()
postControlTrierCheck.pack()

preTestSASCheck.pack()
postTestSASCheck.pack()
preControlSASCheck.pack()
postControlSASCheck.pack()

extraLabel.pack()
stemCheck.pack()
cyberCheck.pack()

testTypeLabel.pack()
tTestCheck.pack()
PlotsCheck.pack()

submitButton.pack()
outputtxt.pack()"""