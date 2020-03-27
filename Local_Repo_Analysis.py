import os
import io
import git
import csv
import pandas as pd
import xml.etree.ElementTree as ET


path_prefix = r"H:\WS 19-20\Mining Software Repositories\Assignment2"
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
file_name = "pom.xml"
df_out = pd.DataFrame(columns=['repo','file_name','sha','commit_date','antler_version'])

def get_antlr_version(repo_path,sha):
    repo = git.Repo(repo_path)
    commit_data = repo.commit(sha)
    
    try:
        targetfile = commit_data.tree / file_name
        with io.BytesIO(targetfile.data_stream.read()) as f:
            content = f.read().decode('utf-8')
            f.close()
            data_dic = extract_version_from_file(content)
        return data_dic
    except:
        print("get_antlr_version_error for {} in {}".format(sha,repo_path))

    



def extract_version_from_file(file_content):
    try:
        root = ET.fromstring (file_content)
        v_d = {}
        props = root.findall("./xmlns:properties", namespaces=namespaces)
        for p in props:
            antlr4_version = p.find("xmlns:antlr4.version", namespaces=namespaces)
            antlr_version = p.find("xmlns:antlr.version", namespaces=namespaces)
            if antlr4_version is not None:
                v_d["antlr_version"] = antlr4_version.text
            if antlr_version is not None:
                v_d["antlr_version"] = antlr_version.text
                
        if "antlr_version" not in v_d:
            deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
            for d in deps:
                groupId = d.find("xmlns:groupId", namespaces=namespaces)
                version = d.find("xmlns:version", namespaces=namespaces)
                if groupId.text == 'org.antlr' :
                    v_d["antlr_version"] = version.text
                    
        return v_d
    except:
        print("extract_version_from_file_error")



files = os.listdir(path_prefix)

for item in files:
#        owner = item.split("/")[0]
        print("Analyzing repo " + item)
        repo_name = item
        constructed_path = path_prefix + "\\" + repo_name 
        
        try:
            g=git.Git(constructed_path)
            hexshas = g.log('--pretty=%H','--follow','--',file_name).split('\n') 
            commit_date = g.log('--pretty=%cD','--follow','--',file_name).split('\n') 

#            continue
            
            for i in range(len(hexshas)):
    
                dd = get_antlr_version(constructed_path,hexshas[i])
                if dd is None or "antlr_version" not in dd:
                    dd = {}
                    dd["antlr_version"] = "N/A"
                i_loc = len(df_out)
                row = df_out.loc[i_loc] = [item,file_name,hexshas[i],commit_date[i],dd["antlr_version"]]
                with open('output_ha.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
        except:
            ("Error in local repo " + repo_name)
            
print("Operation completed")





    

    
    
    
