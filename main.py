"""

This is the main function to get the target data from specified sources/portals
version 3.2
@author: Xiaozhou Li, Sergio Moreschini

"""
import personalInfo.updateInfo
from scripts import getRedditData, getStackOverflowData, getNVDData, \
    getGithubData
import pandas as pd
import os
from personalInfo.updateInfo import your_email

#-------------------- Greetings --------------------
def print_hi(name):
    print(f'Hi, {name}')

#-------------------- Initial Installation --------------------
def installPackage():
    global installPythonPackage
    installPythonPackage = ['pip3 install prawcore pandas numpy requests praw']
    os.system('start cmd /k ' + installPythonPackage[0])

#-------------------- Start to Crawl Data --------------------
def startcrawling():
    # Read the progress stored in flag.csv
    flagdf = pd.read_csv('dataset/flag.csv')
    # Read the tasks to crawl assigned by email in flag.csv
    taskdf = flagdf.loc[flagdf['email'] == personalInfo.updateInfo.your_email]
    targetdatatypes = taskdf.datatype.values.tolist()
    task_dict = {}
    for item in targetdatatypes:
        task_dict[item] = (taskdf.loc[taskdf['datatype']==item, 'start_point'].values[0], taskdf.loc[taskdf['datatype']==item, 'end_point'].values[0])
    for datatype in task_dict.keys():
        currentlocation = task_dict[datatype][0]
        maxlocation = task_dict[datatype][1]
        print("You have started to crawl: {}".format(datatype))
        if datatype == 'project':
            getGithubData.getGithubdatafromRange_Graphv4(currentlocation, maxlocation)
        if datatype == 'stackoverflow':
            getStackOverflowData.getStackoverflowQuestionsDACfromProjectsInRange(currentlocation, maxlocation)
        if datatype == 'reddit':
            getRedditData.getRedditDataProjectsInRange(currentlocation, maxlocation)
        if datatype == 'nvd':
            getNVDData.getNVDDataProjectsInRange(currentlocation, maxlocation)

if __name__ == '__main__':
    print_hi(your_email)
    installPackage()
    print("Now you start crawling data.")
    startcrawling()
