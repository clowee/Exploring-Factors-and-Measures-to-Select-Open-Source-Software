# Raw-Data for the paper "Exploring-Factors-and-Measures-to-Select-Open-Source-Software"

<p>The Project presents the scripts for automatic data crawling of OSS projects on Github, as well as the relevant data of such from other public sources, e.g., Reddit, StackOverflow, and NVD. The main features include: 
   <ol>
   <li>get the list of projects from Github with the stars in a particular range, </li>
   <li>get the relevant Github data for the projects on the previously obtained list, </li>
   <li>get the Reddit data for such projects, </li>
   <li>get the StackOverflow data for such projects, </li>
   <li>get the NVD data for such projects, </li>
   <li>save and read the crawling status enabling continuation from poetential breakpoints, </li>
   <li>assign crawling tasks to multiple users for collaboration and efficiency.</li>
   </ol>
</p>
</br>
Content Description:</br>
1) Dataset:</br>
<ul>
<li>flag.csv: The tracking of data crawling tasks<\li>
<li>githubData.csv: The dataset for the selected Github projects information<\li>
<li>info.csv: The recording of relevant keys and tokens that authorize data collection<\li>
<li>nvdData.csv: The dataset for the vulnerability information related to the selected Github projects<\li>
<li>projectList.txt: The list of fullnames of the selected OSS projects from Github<\li>
<li>redditData.csv: The dataset for the information on Reddit related to the selected Github projects<\li>
<li>stackoverflowData.csv: The dataset for the information on StackOverflow related to the selected Github projects<\li>
d<li>evlangData: The datasets for the stats of lines of code for the developing languages used in the selected Github projects<\li>
<ul>
2) Scripts:<\br>
<ul>
<li>dataMergeVisualize.py: The script to merge distributedly collected data and to visualize<\li>
<li>getGithubData.py: The script to crawl Github data using Github API<\li>
<li>getNVDData.py: The script to crawl NVD data using NVD api<\li>
<li>getProjectList.py: The script to get a list of project names fron Github based on particular criteria<\li>
<li>getRedditData.py: The script to crawl Reddit data using Reddit API<\li>
<li>getStackOverflowData.py: The  script to crawl StackOverflow data using StackOverflow API<\li>
<li>updateFlag.py: The script to track the crawling task status<\li>
<li>updateInfo.py: The script to store and update the crawler's keys and tokens<\li>
</ul>


1. Preparation:

-> Follow the instruction written in How to Get all the Tokens and Keys.pdf to get the required keys and tokens.

-> Add obtained tokens to dataset/info.csv behind your email (task identifier) separated by comma.

-> Assign your email at script/updateInfo.py to the your_email variable.

-> Clarify your crawling tasks in dataset/flag.csv by adding email, datatype, start_point, and end_point.

   For example, crawling nvd data for the first 1000 projects -> add a line youremail@email.com,nvd,0,1000 in flag.csv
   
** NOTE: don't add multiple lines of tasks for the same datatype.

2. Start Crawling:

-> Run main.py to start crawling

3. Potential Fixes:

-> For any reason, the crawling process is ceased, run main.py again to restart

-> If any issue remains after rerunning, manually +1 to the start_point of the targeting task in dataset/flag.csv to skip the problematic project
