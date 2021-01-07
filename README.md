# Exploring-Factors-and-Measures-to-Select-Open-Source-Software

The Project presents the scripts for automatic data crawling of OSS projects on Github, as well as the relevant data of such from other public sources, e.g., Reddit, StackOverflow, and NVD. The main features include: 1) get the list of projects from Github with the stars in a particular range, 2) get the relevant Github data for the projects on the previously obtained list, 3) get the Reddit data for such projects, 4) get the StackOverflow data for such projects, 5) get the NVD data for such projects, 6) save and read the crawling status enabling continuation from poetential breakpoints 7) assign crawling tasks to multiple users for collaboration and efficiency.

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
-> If any issue remains after rerunning, manually +1 to the start_point of the targeting task in dataset/flag.csv
