"""

    This script contains functions to merge separately crawled datasets
    and visualize the data in terms of stats.

"""

import os
from pprint import pprint
import requests
import pandas as pd
import numpy as np
import csv
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pprint import pprint
import requests
import operator

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',25)

personal_token = "636cd7f6d8423025dd09e96f3e8aa08e580144a0"
token = os.getenv('GITHUB_TOKEN', personal_token)
headers = {'Authorization': f'token {token}'}

licenseshortDict = {
    'Not Specified': 'Not Specified',
    'LaTeX Project Public License v1.3c': 'Latex v1.3c',
    'Creative Commons Attribution Share Alike 4.0 International': 'Sharealike 4.0',
    'GNU Lesser General Public License v2.1': 'GNU LGPL v2.1',
    'ISC License': 'ISC',
    'PostgreSQL License': 'PostgreSQL',
    'Microsoft Reciprocal License': 'MS Reciprocal',
    'Universal Permissive License v1.0': 'UPL v1.0',
    'BSD 2-Clause "Simplified" License': 'BSD 2',
    'Other': 'Other',
    'Apache License 2.0': 'Apache 2.0',
    'GNU General Public License v2.0': 'GNU GPL 2.0',
    'Microsoft Public License': 'MS Public',
    'GNU General Public License v3.0': 'GNU GPL v3.0',
    'The Unlicense': 'Unlicense',
    'MIT License': 'MIT',
    'Eclipse Public License 1.0': 'Eclipse 1.0',
    'SIL Open Font License 1.1': 'SIL OF 1.1',
    'Do What The F*ck You Want To Public License': 'DWTFYWT',
    'BSD 4-Clause "Original" or "Old" License': 'BSD 4',
    'Artistic License 2.0': 'Artistic 2.0',
    'Educational Community License v2.0': 'ECL v2.0',
    'Creative Commons Attribution 4.0 International': 'CCA 4.0',
    'Boost Software License 1.0': 'BSL 1.0',
    'zlib License': 'zlib',
    'European Union Public License 1.2': 'EUPL 1.2',
    'European Union Public License 1.1': 'EUPL 1.1',
    'GNU Lesser General Public License v3.0': 'GNU LGPL v3.0',
    'BSD 3-Clause "New" or "Revised" License': 'BSD 3 - CNRL',
    'BSD 3-Clause Clear License': 'BSD 3 - CCL',
    'Mozilla Public License 2.0': 'Mozilla 2.0',
    'Open Software License 3.0': 'OSL 3.0',
    'GNU Affero General Public License v3.0': 'GNU AGPL v3.0',
    'University of Illinois/NCSA Open Source License': 'UI/NCSA',
    'Academic Free License v3.0': 'AFL v3.0',
    'Creative Commons Zero v1.0 Universal': 'CCZ v1.0',
    'Eclipse Public License 2.0': 'Eclipse 2.0',
    'BSD Zero Clause License': 'BSD Zero'
}


def merge_csv(csvtypename):
    all_filenames = [i for i in glob.glob('../dataset_merge/{}_*.csv'.format(csvtypename))]
    combined_csv = pd.concat([pd.read_csv(f, low_memory=False) for f in all_filenames])
    #combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
    #combined_csv.drop_duplicates(subset='project_id', keep='last', inplace=True)
    return combined_csv

def getdays(days):
    return int(str(days).split()[0])

def merge_csv_language(languagelist):
    all_filenames = [i for i in glob.glob('../dataset_merge/devlanguages_*.csv')]
    dflist = []
    languagelist = ['project_id']+languagelist
    for f in all_filenames:
        df_f = pd.read_csv(f, low_memory=False)
        df_f = df_f.loc[:, languagelist]
        dflist.append(df_f)
    combined_csv = pd.concat(dflist)
    combined_csv.drop_duplicates(subset='project_id', keep='last', inplace=True)
    return combined_csv

"""
githubdata = merge_csv('githubdata')
githubdata['loc_count_k'] = round(githubdata['loc_count']/1000,1)
githubdata['age'] = pd.to_datetime(githubdata['updated_at']) - pd.to_datetime(githubdata['created_at'])
githubdata['age'] = githubdata['age'].apply(getdays)
githubdata['age_year'] = round(githubdata['age']/365,3)
githubdata['issue_count'] = githubdata['open_issue_count']+githubdata['closed_issue_count']
githubdata = githubdata.loc[githubdata['stargazer_count']>=200,:]
githubdata.to_csv('githubData.csv', encoding='utf-8', index=False)

redditdata = merge_csv('redditcsv')
redditdata.replace('No', 0, inplace=True)
redditdata.replace('Forbidden', 0, inplace=True)
redditdata['subscribers'] = redditdata['subscribers'].apply(int)
redditdata['#posts'] = redditdata['#posts'].apply(int)
redditdata.to_csv('Rtesting.csv', encoding='utf-8', index=False)
"""

#df_devlanguagedata = merge_csv_language(top20langs)
#df_devlanguagedata.dropna(axis = 0, how = 'all', inplace = True)

stackoverflowdata = merge_csv('newstackoverflowdata')
df = pd.read_csv('githubData.csv')
df_r = pd.read_csv('Rtesting.csv')
#df.sort_values(by=['stargazer_count'], ascending=False, inplace=True)
#df['release_count'] = df['release_count'].replace(np.NaN, 0)
#df['issue_count'] = df['issue_count'].replace(np.NaN, 0)
#df = df.head(100000)
#df.to_csv('githubData.csv', encoding='utf-8', index=False)

def getProjectListinStarRange(txtfilename, fromstar, tostar):
    theQuery = f"https://api.github.com/search/repositories?q=stars:{fromstar}..{tostar}"
    page = 1
    while 1==1:
        search_params = {"page": page, "per_page": 100}
        with open(txtfilename, 'r', encoding='utf-8') as txtread:
            existingList = [x.strip('\n') for x in txtread.readlines()]
        r_search = requests.get(theQuery, headers=headers, params=search_params)
        search_30 = r_search.json()
        try:
            items = search_30['items']
            if len(items)==0:
                break
            else:
                print(len(items), page)
                starMin = min([x['stargazers_count'] for x in items])
                newCondition = f"stars:{fromstar}..{starMin}"
                theQuery = f"https://api.github.com/search/repositories?q={newCondition}"
                projectList_30 = [x['full_name'] for x in items]
                projectList = [x for x in projectList_30 if x not in existingList]
                if len(projectList)==0:
                    page = page+1
                    continue
                else:
                    with open(txtfilename, 'a', encoding='utf-8') as txtwrite:
                        for project in projectList:
                            txtwrite.write(project+'\n')
                    page = 1
        except:
            pprint(search_30)
            if 'errors' in list(search_30.keys()):
                break

def getProjectListinStarRangeUpdated(txtfilename, fromstar, tostar):
    theQuery = f"https://api.github.com/search/repositories?q=stars:{fromstar}..{tostar}"
    search_params = {"per_page": 100}
    r_search = requests.get(theQuery, headers=headers, params=search_params)
    total_count = int(r_search.json()['total_count'])
    page_count = int(total_count/100)+1
    starMin = 0
    while page_count>=10:
        for i in range(10):
            search_params["page"] = i+1
            with open(txtfilename, 'r', encoding='utf-8') as txtread:
                existingList = [x.strip('\n') for x in txtread.readlines()]
            r_search = requests.get(theQuery, headers=headers, params=search_params)
            search_100 = r_search.json()
            try:
                items = search_100['items']
                starMin = min([x['stargazers_count'] for x in items])
                if len(items) == 0:
                    continue
                else:
                    print(len(items), i+1)
                    print(theQuery)
                    projectList_100 = [x['full_name'] for x in items]
                    projectList = [x for x in projectList_100 if x not in existingList]
                    if len(projectList) == 0:
                        continue
                    else:
                        with open(txtfilename, 'a', encoding='utf-8') as txtwrite:
                            for project in projectList:
                                txtwrite.write(project + '\n')
            except:
                print(search_100)
                continue
        newCondition = f"stars:{fromstar}..{starMin}"
        theQuery = f"https://api.github.com/search/repositories?q={newCondition}"
        r_search = requests.get(theQuery, headers=headers, params=search_params)
        total_count = int(r_search.json()['total_count'])
        page_count = int(total_count / 100) + 1
        #break

def displayStarStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    ax = sns.histplot(data=thedf, x='stargazer_count', binwidth=100, kde=True)
    plt.xlim(0,50000)
    plt.ylim(0,5000)
    plt.savefig('stars.png', bbox_inches='tight')
    plt.show()

def displayWatcherStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    ax = sns.histplot(data=thedf, x='watcher_count', binwidth=100, kde=True)
    plt.xlim(0,50000)
    plt.ylim(0,5000)
    #plt.savefig('stars.png', bbox_inches='tight')
    plt.show()

def displayPLStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    ax = sns.countplot(data=thedf, x='primary_language', order = thedf['primary_language'].value_counts().iloc[:50].index)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    #plt.xlim(1200,2000)
    #plt.ylim(0,4000)
    plt.savefig('primaryLanguageTop50.png', bbox_inches='tight')
    plt.show()

def displayAgeStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    ax = sns.histplot(data=thedf, x='age', binwidth=100, kde=True)
    # plt.xlim(1200,2000)
    # plt.ylim(0,4000)
    plt.savefig('age.png', bbox_inches='tight')
    plt.show()

def displayReleaseStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    #plt.hist(thedf['release_count'], bins=20000)
    #plt.xlabel('Count')
    #plt.ylabel('Release_count')
    ax = sns.histplot(data=thedf, x='release_count', binwidth=10, kde=True)
    #plt.ylim(0,10000)
    plt.xlim(1,200)
    plt.savefig('release.png', bbox_inches='tight')
    plt.show()

def displayLicenseStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    ax = sns.countplot(data=thedf, x='license_name', order = thedf['license_name'].value_counts().index)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    #plt.xlim(1200,2000)
    #plt.ylim(0,4000)
    plt.savefig('license.png', bbox_inches='tight')
    plt.show()

def displayIssueStatsHistplot(thedf):
    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    plt.hist(thedf['issue_count'], bins=10000)
    plt.xlabel('issue_count')
    plt.ylabel('count')
    #ax = sns.histplot(data=thedf, x='loc_count_k', binwidth=10, kde=True)
    #plt.ylim(0,10000)
    plt.xlim(0,1000)
    plt.savefig('issue.png', bbox_inches='tight')
    plt.show()

def getmissingProjects(thedf, thenewlist, savetotxt):
    existingProjects = thedf.loc[:,'full_name'].values.tolist()
    with open(thenewlist, 'r', encoding='utf-8') as txtread:
        theTargetProjects = [x.strip('\n') for x in txtread.readlines()]
    themissingProject = [x for x in theTargetProjects if x not in existingProjects]
    with open(savetotxt, 'w', encoding='utf-8') as txtwrite:
        for project in themissingProject:
            txtwrite.write(project + '\n')

def displayYearsStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    years = thedf.loc[:,'age_year'].values.tolist()
    yearlist = list(range(int(max(years)+1)))
    df_year = thedf.loc[:,['age_year']]
    df_year['year_int'] = df_year['age_year'].apply(int)
    df_year_group = df_year.groupby('year_int').count()
    countlist = df_year_group.loc[:,'age_year'].values.tolist()
    #print(countlist)
    #print(yearlist)
    plot = plt.bar(yearlist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Age")
    plt.xlabel("Project Age (Years)")
    plt.ylabel("Number of Projects")
    #ax = sns.histplot(data=thedf, x='age_year', binwidth=1, kde=True)
    # plt.xlim(1200,2000)
    # plt.ylim(0,4000)
    plt.savefig('ageyear.png', bbox_inches='tight')
    plt.show()

def displayStarStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_star = thedf.loc[:, ['stargazer_count']]
    starlist = df_star.loc[:,'stargazer_count'].values.tolist()
    rangelist = ['<500', '501-1k', '1k-2k', '2k-4k', '4k-10k', '10k-20k', '20k-100k', '>100k']
    thresholdlist = [0,500,1000,2000,4000,10000,20000,100000,max(starlist)]
    #print(df_star.head())
    countlist = []
    for i in range(len(thresholdlist)-1):
        countlist.append(len([x for x in starlist if x>thresholdlist[i] and x<=thresholdlist[i+1]]))
    #print(rangelist)
    #print(countlist)
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    #ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    plt.title("Number of Projects by Stars")
    plt.xlabel("Number of Stars Ranges")
    plt.ylabel("Number of Projects")
    plt.savefig('stars.png', bbox_inches='tight')
    plt.show()

def displayIssueStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_issue = thedf.loc[:, ['issue_count']]
    issuelist = df_issue.loc[:, 'issue_count'].values.tolist()
    rangelist = ['<10','10-50','50-100','100-200','200-500', '501-1k', '1k-2k', '2k-4k', '4k-10k', '10k-20k', '20k-100k', '>100k']
    thresholdlist = [0, 10, 50, 100, 200, 500, 1000, 2000, 4000, 10000, 20000, 100000, max(issuelist)]
    countlist = []
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in issuelist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Issues")
    plt.xticks(np.arange(len(rangelist)), rangelist, rotation='vertical')
    plt.xlabel("Number of Issues Ranges")
    plt.ylabel("Number of Projects")
    #plt.hist(thedf['issue_count'], bins=10000)
    #plt.xlabel('issue_count')
    #plt.ylabel('count')
    #ax = sns.histplot(data=thedf, x='loc_count_k', binwidth=10, kde=True)
    #plt.ylim(0,10000)
    #plt.xlim(0,1000)
    plt.savefig('issue.png', bbox_inches='tight')
    plt.show()

def displayReleaseStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_re = thedf.loc[:, ['release_count']]
    relist = df_re.loc[:, 'release_count'].values.tolist()
    print(max(relist))
    rangelist = ['=0', '<10', '10-50', '50-100', '100-200', '200-500', '501-1k', '1k-2k', '2k-4k', '4k-10k', '>10k']
    thresholdlist = [0, 10, 50, 100, 200, 500, 1000, 2000, 4000, 10000, max(relist)]
    countlist = []
    countlist.append(len([x for x in relist if x == 0]))
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in relist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Releases")
    plt.xticks(np.arange(len(rangelist)), rangelist, rotation='vertical')
    plt.xlabel("Number of Releases Ranges")
    plt.ylabel("Number of Projects")
    # plt.hist(thedf['issue_count'], bins=10000)
    # plt.xlabel('issue_count')
    # plt.ylabel('count')
    # ax = sns.histplot(data=thedf, x='loc_count_k', binwidth=10, kde=True)
    # plt.ylim(0,10000)
    # plt.xlim(0,1000)
    plt.savefig('release.png', bbox_inches='tight')
    plt.show()

def displayLicenseStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    oslicenses = list(set(thedf.loc[:, 'license_name'].values.tolist()))
    print(oslicenses)
    oslicenses.remove(np.NaN)
    df_license = thedf.loc[:,['license_name']]
    #countlist = df_license_group.loc[:, 'license_name'].values.tolist()
    countlist = []
    for item in oslicenses:
        countlist.append(df_license.loc[df_license['license_name']==item].shape[0])
    oslicenses.append("Not Specified")
    countlist.append(thedf.shape[0]-sum(countlist))
    licensedict = {}
    oslicenses = [licenseshortDict[x] for x in oslicenses]
    for i in range(len(oslicenses)):
        licensedict[oslicenses[i]] = countlist[i]
    sorted_d = dict(sorted(licensedict.items(), key=operator.itemgetter(1), reverse=True))
    plot = plt.bar(list(sorted_d.keys()), list(sorted_d.values()))
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 height+1000, '%d' % int(height), ha='center', va='bottom', rotation=90)
    plt.title("Number of Projects by License")
    plt.xticks(np.arange(len(list(sorted_d.keys()))), list(sorted_d.keys()), rotation='vertical')
    plt.xlabel("Licenses")
    plt.ylabel("Number of Projects")
    plt.savefig('license_short.png', bbox_inches='tight')
    plt.show()

def displayPLStatsHistplot_matplotlib(thedf, toplanguage):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    languages = list(set(thedf.loc[:, 'primary_language'].values.tolist()))
    languages.remove(np.NaN)
    df_lang = thedf.loc[:, ['primary_language']]
    countlist = []
    for item in languages:
        countlist.append(df_lang.loc[df_lang['primary_language'] == item].shape[0])
    languages.append("Not Specified")
    countlist.append(thedf.shape[0]-sum(countlist))
    licensedict = {}
    for i in range(len(languages)):
        licensedict[languages[i]] = countlist[i]
    sorted_d = dict(sorted(licensedict.items(), key=operator.itemgetter(1), reverse=True))
    plot = plt.bar(list(sorted_d.keys())[:toplanguage], list(sorted_d.values())[:toplanguage])
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 height+1000, '%d' % int(height), ha='center', va='bottom', rotation=90)
    print(list(sorted_d.keys())[:toplanguage])
    plt.title("Number of Projects by Primary Languages Top {}".format(toplanguage))
    plt.xticks(np.arange(len(list(sorted_d.keys())[:toplanguage])), list(sorted_d.keys())[:toplanguage], rotation='vertical')
    plt.xlabel("Languages")
    plt.ylabel("Number of Projects")
    plt.savefig('primarylanguageTop{}.png'.format(toplanguage), bbox_inches='tight')
    plt.show()

def displayLOCStatsHistplot_matplotlib(thedf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_loc = thedf.loc[:, ['loc_count']]
    loclist = df_loc.loc[:, 'loc_count'].values.tolist()
    print(max(loclist))
    rangelist = ['<100', '100-500', '501-1k', '1k-5k', '5k-10k', '10k-20k', '20k-100k', '100k-500k', '500k-1m', '1m-5m', '>5m']
    thresholdlist = [0, 100, 500, 1000, 5000, 10000, 20000, 100000, 500000, 1000000, 5000000, max(loclist)]
    countlist = []
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in loclist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by LOC")
    plt.xticks(np.arange(len(rangelist)), rangelist, rotation='vertical')
    plt.xlabel("Number of LOC Ranges")
    plt.ylabel("Number of Projects")
    plt.savefig('locprojects.png', bbox_inches='tight')
    plt.show()

def displayLOCbyLanguageStatsHistplot_matplotlib(thedf, toplanguage):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    languages = list(set(thedf.loc[:, 'primary_language'].values.tolist()))
    languages.remove(np.NaN)
    df_lang = thedf.loc[:, ['primary_language']]
    countlist = []
    for item in languages:
        countlist.append(df_lang.loc[df_lang['primary_language'] == item].shape[0])
    languages.append("Not Specified")
    countlist.append(thedf.shape[0] - sum(countlist))
    licensedict = {}
    for i in range(len(languages)):
        licensedict[languages[i]] = countlist[i]
    sorted_d = dict(sorted(licensedict.items(), key=operator.itemgetter(1), reverse=True))
    selectedlanglist = list(sorted_d.keys())[:toplanguage]
    if "Not Specified" in selectedlanglist:
        selectedlanglist = list(sorted_d.keys())[:toplanguage+1]
        selectedlanglist.remove("Not Specified")
    df_devlanguagedata = merge_csv_language(selectedlanglist)
    df_devlanguagedata.dropna(axis=0, how='all', inplace=True)
    df_devlanguagedata.fillna(0, inplace=True)
    langloclist = []
    for lang in selectedlanglist:
        langloclist.append(sum(df_devlanguagedata.loc[:,lang].values.tolist()))
    loclangdict = {}
    for i in range(len(selectedlanglist)):
        loclangdict[selectedlanglist[i]] = langloclist[i]
    sorted_d = dict(sorted(loclangdict.items(), key=operator.itemgetter(1), reverse=True))
    plot = plt.bar(list(sorted_d.keys()), list(sorted_d.values()))
    #print(sorted_d)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 height + 10000000, str(round(height/1000000000,1))+'b', ha='center', va='bottom', rotation=90)
    plt.title("Lines of Code for Top {} Languages".format(toplanguage))
    plt.xticks(np.arange(len(list(sorted_d.keys()))), list(sorted_d.keys()),
               rotation='vertical')
    plt.xlabel("Languages")
    plt.ylabel("LOC")
    plt.savefig('locbylanguageTop{}.png'.format(toplanguage), bbox_inches='tight')
    plt.show()

def displayRedditPostsStates_matplotlib(theredditdf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_post = theredditdf.loc[:, ['#posts']]
    postlist = df_post.loc[:, '#posts'].values.tolist()
    rangelist = ['=0','<10', '10-50', '50-100', '100-200', '200-500', '501-800', '>800']
    thresholdlist = [0, 10, 50, 100, 200, 500, 800, max(postlist)]
    countlist = []
    countlist.append(len([x for x in postlist if x == 0]))
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in postlist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Number of Reddit Posts")
    plt.xticks(np.arange(len(rangelist)), rangelist)
    plt.xlabel("Number of Posts")
    plt.ylabel("Number of Projects")
    plt.savefig('redditpostsprojects.png', bbox_inches='tight')
    plt.show()

def displayRedditSubscribersStates_matplotlib(theredditdf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_post = theredditdf.loc[:, ['subscribers']]
    postlist = df_post.loc[:, 'subscribers'].values.tolist()
    rangelist = ['=0','<10', '10-50', '50-100', '100-200', '200-500', '501-800', '>800']
    thresholdlist = [0, 10, 50, 100, 200, 500, 800, max(postlist)]
    countlist = []
    countlist.append(len([x for x in postlist if x == 0]))
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in postlist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Number of Reddit Subscribers")
    plt.xticks(np.arange(len(rangelist)), rangelist)
    plt.xlabel("Number of Subscribers")
    plt.ylabel("Number of Projects")
    plt.savefig('redditsubscribers.png', bbox_inches='tight')
    plt.show()

def displayStackoverflowQuestionsStates_matplotlib(thestackdf):
    a4_dims = (11.7, 8.27)
    smaller_dim = (8, 4.5)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    df_post = thestackdf.loc[:, ['questions_count']]
    postlist = df_post.loc[:, 'questions_count'].values.tolist()
    postlist = postlist+[0]*(100000-len(postlist))
    rangelist = ['=0','<50', '50-100', '100-200', '200-500', '501-1k', '1k-5k', '5k-10k', '>10k']
    thresholdlist = [0, 50, 100, 200, 500, 1000, 5000, 10000, max(postlist)]
    print(max(postlist))
    countlist = []
    countlist.append(len([x for x in postlist if x == 0]))
    for i in range(len(thresholdlist) - 1):
        countlist.append(len([x for x in postlist if x > thresholdlist[i] and x <= thresholdlist[i + 1]]))
    plot = plt.bar(rangelist, countlist)
    for value in plot:
        height = value.get_height()
        plt.text(value.get_x() + value.get_width() / 2.,
                 1.002 * height, '%d' % int(height), ha='center', va='bottom')
    plt.title("Number of Projects by Number of StackOverflow Qustions")
    plt.xticks(np.arange(len(rangelist)), rangelist)
    plt.xlabel("Number of Questions on StackOverflow")
    plt.ylabel("Number of Projects")
    plt.savefig('stackquestions.png', bbox_inches='tight')
    plt.show()

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def displayPieChartCompanySize():
    smaller_dim = (8, 4.5)
    labels = ['0-50', '50-250', '250-1k', '>1k']
    interviews = [3,2,7,9]
    explode = (0, 0, 0, 0)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.pie(interviews, explode=explode, labels=labels, autopct=lambda pct: func(pct, interviews), shadow=False, startangle=90)
    ax.axis('equal')
    plt.title("Number of Interviews from Companies of Different Sizes")
    plt.savefig('interviews_companysize.png', bbox_inches='tight')
    plt.show()

def displayPieChartRoles():
    smaller_dim = (8, 4.5)
    labels = ['SW Developer', 'Product Manager', 'Software Architect']
    interviews = [8,7,6]
    explode = (0, 0, 0)
    fig, ax = plt.subplots(figsize=smaller_dim)
    ax.pie(interviews, explode=explode, labels=labels, autopct=lambda pct: func(pct, interviews), shadow=False, startangle=90)
    ax.axis('equal')
    plt.title("Number of Interviews from Different Roles")
    plt.savefig('interviews_roles.png', bbox_inches='tight')
    plt.show()
