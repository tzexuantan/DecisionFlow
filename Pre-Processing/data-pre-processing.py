import pandas as pd

import re
from collections import Counter
from tqdm import tqdm

import spacy
from spacy.matcher import PhraseMatcher

#Initialize dataset
df = pd.read_csv("Indeed_Data(10K).csv")
print(len(df))


#Function to remove html tags
def remove_html_tags(text):
    clean = re.sub(r'<.*?>', '', str(text))
    return clean

#Function to remove unwanted symbols
def remove_unwanted_symbols(text):
    return re.sub(r'[â€œ,â€™,â€]', '', str(text))

#remove html tags and unwanted symbols
df['Job Description'] = df['Job Description'].apply(remove_html_tags)
df['Job Description'] = df['Job Description'].apply(remove_unwanted_symbols)

#Extract necessary columns
df.to_excel("Processed.xlsx", index=False, columns = ['Company Name','Job Title','Job Description','Employer Location','Employer City','Employer State','Employer Country','Apply Url','Companydescription'])

#Phrase Matching

#Function to Create Profile
def create_profile(nlp, matcher,company_name, job_title, job_desc, emp_location, emp_city, emp_state, emp_country, apply, company_desc):
    doc = nlp(job_desc)
    matches = matcher(doc)
	# Create a dataframe to return
    d = []
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start : end]
        d.append((rule_id, span.text))
    data = []
    for each,count in Counter(d).items():
        data.append([company_name,job_title,*each,count,job_desc, emp_location, emp_city, emp_state, emp_country, apply, company_desc])
    dataf = pd.DataFrame(data,columns=['Company/Candidate Name','Job Title','Skill','Sub-skill','Count', 'Job Description','Employer Location','Employer City','Employer State','Employer Country','Apply Url','Company Description'])
    return(dataf)

#Load nlp spacy
nlp = spacy.load("en_core_web_sm")

#Read skillset file and find matching keywords
keyword_ = pd.read_excel("Skillset.xlsx")
matcher = PhraseMatcher(nlp.vocab)
for each in keyword_.columns: 
    matcher.add(each, None, *[nlp(text) for text in keyword_[each].dropna(axis = 0)])

#Read Processed job desc 
processed_df = pd.read_excel("Processed.xlsx")

#Find matching skills and append the information to a new df
final_data = []
for each in tqdm(range(len(processed_df))):
    company_name = processed_df.loc[each,'Company Name']
    job_title = processed_df.loc[each, 'Job Title']
    job_desc = processed_df.loc[each,'Job Description']
    emp_location = processed_df.loc[each,'Employer Location']
    emp_city = processed_df.loc[each,'Employer City']
    emp_state = processed_df.loc[each,'Employer State']
    emp_country = processed_df.loc[each,'Employer Country']
    apply = processed_df.loc[each,'Apply Url']
    company_desc = processed_df.loc[each,'Companydescription']
    data = create_profile(nlp,matcher,company_name,job_title,job_desc, emp_location, emp_city, emp_state, emp_country, apply, company_desc)
    final_data.append(pd.DataFrame(data))

# Concatenate all DataFrames in the final_data list
final_df = pd.concat(final_data, ignore_index=True)

#Create excel sheet with final dataset
final_df.to_excel("Final.xlsx", index=False)