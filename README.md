# Evolution Of AntlrTechnology


## Build instruction
 
The main.py file needs to be executed using any python compiler

## Run instruction

These modification in main.py file needs to be done before running the solution:

1. update link of csv file(sample.csv) which contains the list of repositories to be mined
2. individual github userId and password should be updated(twice one for PyGithub and one for Git Api)

Note: "path" variable is assigned with "pom.xml" as we are only analyzing the pom files. Other file types can be also analyzed by changing the path value. However, custom perser should be created to mine different file type.

The output is written in a local file namely "out.txt" and also in a panda dataframe "df_output". The colums of the dataframe are ["Repo", "File_name", "Download_url", "Commit","Time", "Antlr_version"]

Repo: Name of the repository.
File_name: Specific file analyzed in the repo. e.g "pom.xml"
Download_url: Raw file URL of the file content for each commit.
Commit: SHA code of specific commit
Time: Timestamp of the commit
Antlr_version: Version of antler in the file

## Objective

We tried to anallyze the changes of "antlr version" in each "pom.xml" file in every repository from a predefined list of repositories(sample.csv). Every commit/changes on "pom.xml" file is considered in our case.

## Findings


## Analysis process

These are the steps how we extracted the antlr version in "pom.xml" files
1. For every repository we searched the changes/commits over a specific "pom.xml" file from Git Api.
2. We iterated over each commit to track changes over different commit
3. We got the "download_url" of the file using PyGithub library
4. We analyzed the content of the file using basic string operation based on some generic pattern on "pom.xml" file



