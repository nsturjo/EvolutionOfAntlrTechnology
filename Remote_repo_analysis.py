# -*- coding: utf-8 -*-

from datetime import datetime
from github import Github
import pandas as pd
import requests
import time
import json


g = Github("nsturjo@gmail.com", "***")
df = pd.read_csv(r'H:\WS 19-20\Mining Software Repositories\Assignment2\sample.csv')

gh_session = requests.Session()
gh_session.auth = ("nsturjo@gmail.com", "***")



f = open('out.txt','w')

all_repo = df.repository

# iteration over all the repos in csv file
for item in all_repo:
    try:
        repo = g.get_repo(item)
    except:
        print("Error fetching {} repository".format(item), file=f)
    path = "pom.xml"
    owner = item.split("/")[0]
    repo_name = item.split("/")[1]   
    url = "https://api.github.com/repos/{}/{}/commits?path={}".format(owner, repo_name, path)
    # getting all the commits over a specific file path from git api
    r = gh_session.get(url)
    if(r.status_code == 403):
        print("Rate Limit exceeded! Try later.", file=f)
        break
    if(r.status_code == 404):
        print(path + "file doesn't exist.", file=f)
        continue
    time.sleep(0.73)
    
    json_response = json.loads(r.text)
    
    # variables for extracting data from the raw pom.xml file
    maven_model_start_tag_txt = "<modelVersion>"
    maven_model_end_tag_txt = "</modelVersion>"
    antlr_version_start_tag_txt = "<antlr.version>"
    antlr_version_end_tag_txt = "</antlr.version>"
    antlr4_version_start_tag_txt = "<antlr4.version>"
    antlr4_version_end_tag_txt = "</antlr4.version>"
    
    # output data frame declaration
    df_output = pd.DataFrame(columns =  ["Repo", "File_name", "Download_url", "Commit","Time", "Antlr_version"])
    
    
    file_name = "pom.xml"
    for data in json_response:  # iterating over each commit over specific pom.xml file
        
        sha = data["sha"]
        raw_date = data['commit']['author']['date']
        commit_time = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%SZ')
        
        try:
            contents = repo.get_contents(file_name, ref=sha)  # using PyGithub method to fetch the download_url of the pom.xml file
        except:
            print(file_name + " not found for commit " + sha, file=f)
        # getting the file from git api
        raw_file = requests.get(contents.download_url)
        raw_file = raw_file.text
        time.sleep(0.73)
        
        maven_versio_start_index = raw_file.find(maven_model_start_tag_txt) + len(maven_model_start_tag_txt)
        maven_version_end_index = raw_file.find(maven_model_end_tag_txt)
        
        maven_version_no = raw_file[maven_versio_start_index:maven_version_end_index]

        # extracting antlr version from raw_file using string operation
        antlr_version = "N/A"
        if raw_file.find(antlr_version_start_tag_txt) != -1:   
            antlr_version_start_index = raw_file.find(antlr_version_start_tag_txt) + len(antlr_version_start_tag_txt)
            antlr_version_end_index = raw_file.find(antlr_version_end_tag_txt)
            antlr_version = raw_file[antlr_version_start_index:antlr_version_end_index]
                    
        elif raw_file.find(antlr4_version_start_tag_txt) != -1:
            antlr4_version_start_index = raw_file.find(antlr4_version_start_tag_txt) + len(antlr4_version_start_tag_txt)
            antlr4_version_end_index = raw_file.find(antlr4_version_end_tag_txt)
            antlr_version = raw_file[antlr4_version_start_index:antlr4_version_end_index]
            
        else:
            antlr_groupid_tag = "org.antlr"
            
            groupid_tag_index = raw_file.find(antlr_groupid_tag) + 9
            if raw_file.find(antlr_groupid_tag) != -1:
                cropped_file = raw_file[groupid_tag_index:(groupid_tag_index + raw_file[groupid_tag_index:].find("</dependency>"))]
                antlr_version = cropped_file[cropped_file.find("<version>") + 9 : cropped_file.find("</version>")]
            
        # printing output in text file and adding individual revision data into global output dataframe
        print_preview = [item,file_name,contents.download_url,sha,commit_time,antlr_version]
        df_output.loc[len(df_output)] = print_preview
        print(print_preview, file=f)
            
    
