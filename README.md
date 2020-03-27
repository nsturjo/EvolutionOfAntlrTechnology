# Evolution Of Antlr Technology

## Objective

The objective is to observe the usage of antlr technology and its evolution. We tried to find out the presence and change of antlr dependency version in a defined set of public repositories by analyzing 'pom.xml' configuration file throughout their lifespan.


## Build instruction
 
The 'Remote_repo_analysis.py' and/or 'Local_Repo_Analysis.py' file needs to be executed seperately using python compiler which supports python 3.7. PyGithub needs to be installed using 'pip install PyGithub' command

## Run instruction

These modification in 'Remote_repo_analysis.py' file needs to be done before running the solution:

1. update link of csv file(sample.csv) which contains the list of repositories to be mined
2. individual github userId and password should be updated(twice one for PyGithub and one for Git Api)

The output file of will be generated in 'out.txt' file

Following changes required to run 'Local_Repo_Analysis.py':

1. all the repositores required to be cloned in locally in specific folder
2. 'path_prefix' should be changed to the parent folder which contains all the repo

The output file will be generated in 'output_ha.csv' file. A sample copy is also uploaded.

Note: "path" variable is assigned with "pom.xml" as we are only analyzing the pom files. Other file types can be also analyzed by changing the path value. However, custom perser should be created to mine different file type.

The output is written in a local file namely "out.txt" and also in a panda dataframe "df_output". The colums of the dataframe are ["Repo", "File_name", "Download_url", "Commit","Time", "Antlr_version"]

Repo: Name of the repository.
File_name: Specific file analyzed in the repo. e.g "pom.xml"
Download_url: Raw file URL of the file content for each commit.
Commit: SHA code of specific commit
Time: Timestamp of the commit
Antlr_version: Version of antler in the file


## Findings

1. pom.xml doesn't exists for some commit
2. antlr version doesn't change frequently 
3. Analyzing local repo is way faster than remote one. However, cloning repo locally require additional costs. 


## Analysis process

These are the steps how we extracted the antlr version in "pom.xml" files
1. For every repository we searched the changes/commits over a specific "pom.xml" file from Git Api.
2. We iterated over each commit to track changes over different commit
3. We got the "download_url" of the file using PyGithub library
4. We analyzed the content of the file using basic string operation based on some generic pattern on "pom.xml" file



