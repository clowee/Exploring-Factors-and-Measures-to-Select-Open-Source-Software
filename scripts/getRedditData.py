"""

    This script gets the Reddit data
    For example, we want to have the data of the first 1000 projects in the projectList.txt
    We call function as:
    getRedditDataProjectsInRange(0,1000)
    *** to change the saving directory, please update it inside the according function ***

"""

####################################################### Imports ########################################################
import os, time
import pandas as pd
import praw
from scripts.updateInfo import reddit_client_id_input, reddit_client_secret_input, reddit_user_agent_input,\
    reddit_username_input, reddit_password_input, github_personal_token_input, your_email
from prawcore import NotFound
import requests, csv
from scripts import updateFlag

####################################################### Configs ########################################################
start_time = time.time()
count = 0
NonExistent = 'No'
Exception = 'Forbidden'
github_token = os.getenv('GITHUB_TOKEN', github_personal_token_input)
github_headers = {'Authorization': f'token {github_token}'}

reddit = praw.Reddit(client_id=reddit_client_id_input,
                     client_secret=reddit_client_secret_input,
                     user_agent=reddit_user_agent_input,
                     username=reddit_username_input,
                     password=reddit_password_input, )


####################################################### Functions ######################################################


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def getRedditDataProjectsInRange(fromN, toN):
    with open("dataset/projectList_old.txt", 'r', encoding='utf-8') as txtfile:
        projectList = [x.strip('\n') for x in txtfile.readlines()][fromN:toN]
    count = fromN+1
    for item in projectList:
        try:
            theProjectQuery = f"https://api.github.com/repos/{item}"
            time.sleep(2)
            p_search = requests.get(theProjectQuery, headers=github_headers)
            project_info = p_search.json()
            project_id = project_info['id']
            projecttitle = item.split('/')[1]
            exist = sub_exists(projecttitle)
            if exist:
                try:
                    subreddit = reddit.subreddit(projecttitle)
                    number_of_posts = countPages(subreddit)
                    thereturn = [project_id, number_of_posts, subreddit.subscribers, subreddit.created]

                except:
                    print("Error received for project: " + projecttitle)
                    thereturn = [project_id, Exception, Exception, Exception]

            else:
                thereturn = [project_id, NonExistent, NonExistent, NonExistent]
            currentdf = pd.read_csv("dataset/redditcsv.csv", index_col='project_id')
            existingprojects = currentdf.index.values.tolist()
            if project_id in existingprojects:
                currentdf.loc[project_id] = thereturn[1:]
                currentdf.reset_index(inplace=True)
                currentdf.to_csv("dataset/redditcsv.csv", encoding='utf-8', index=False)
            else:
                with open("dataset/redditcsv.csv", 'a', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(thereturn)
            print("Reddit {}".format(count))
        except KeyError:
            print("Project {} NOT exist any more... very sad".format(count))
        updateFlag.updateflag("dataset/flag.csv", your_email, 'reddit', count, toN)
        count = count + 1


def countPages(subreddit):
    posts = 0
    for post in subreddit.new(limit=None):
        posts = posts + 1
    return posts

