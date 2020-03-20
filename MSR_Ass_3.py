# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:28:06 2020

@author: nstur
"""
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
#github_api = "https://api.github.com"
#gh_session = requests.Session()
#gh_session.auth = ("nsturjo@gmail.com", "***")

#gh_session.get(url = url)

all_repo = df.repository

for item in all_repo:
    repo = g.get_repo(item)
    path = "pom.xml"
    owner = item.split("/")[0]
    repo_name = item.split("/")[1]   
    url = "https://api.github.com/repos/{}/{}/commits?path={}".format(owner, repo_name, path)
    
#    repo = g.get_repo(item)
    
    
    
    r = gh_session.get(url)
    if(r.status_code == 403):
        print("Rate Limit exceeded! Try later.")
        break
    if(r.status_code == 404):
        print("File {} doesn't exist.".format(path))
        continue
    time.sleep(1)
    
    json_response = json.loads(r.text)
    
    
    maven_model_start_tag_txt = "<modelVersion>"
    maven_model_end_tag_txt = "</modelVersion>"
    antlr_version_start_tag_txt = "<antlr.version>"
    antlr_version_end_tag_txt = "</antlr.version>"
    antlr4_version_start_tag_txt = "<antlr4.version>"
    antlr4_version_end_tag_txt = "</antlr4.version>"
    
    
    df_output = pd.DataFrame(columns =  ["Repo", "File_name", "Download_url", "Commit","Time", "Antlr_version"])
    
    
    file_name = "pom.xml"
    for i, data in enumerate(json_response):
        
        sha = data["sha"]
        raw_date = data['commit']['author']['date']
        commit_time = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%SZ')
        
        
        try:
            contents = repo.get_contents(file_name, ref=sha)
        except:
            print("{} not found for commit {}".format(file_name,sha))
        
        raw_file = requests.get(contents.download_url)
        raw_file = raw_file.text
        time.sleep(1)
        
        maven_versio_start_index = raw_file.find(maven_model_start_tag_txt) + len(maven_model_start_tag_txt)
        maven_version_end_index = raw_file.find(maven_model_end_tag_txt)
        
        maven_version_no = raw_file[maven_versio_start_index:maven_version_end_index]

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
            
        print_preview = df_output.loc[i] = [item,file_name,contents.download_url,sha,commit_time,antlr_version]
        print(print_preview)   
            
            

#print(all_repo)
