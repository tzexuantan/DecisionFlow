# what inputs should lead to what outputs?

# Logic
# Handling of text
# Receive user input
# Handle user input

# ML
# Career path 
# Showing the different paths

# what are the skills required if I would like to apply for a particular type of position/role?

import spacy
import json

ROLES_AND_SKILLS_FILE = "roles_and_associated_skills.json"
WELCOME_MESSAGE = """
Welcome to DecisionFlow

Possible Questions:
1. What are the skills required if I would like to apply for a particular type of position/role?
"""

nlp = spacy.load("en_core_web_sm") # Load the spaCy language model

#Obtain job roles and skills association
def getJobRolesFromJSONFile():
    with open(ROLES_AND_SKILLS_FILE, 'r') as file:
        data = json.load(file)

    return list(data['jobRoles'].keys())


def getFirstWordsOfEachJobRoleListGivenJobRolesList(jobRolesList: list):
    return [role.split()[0] for role in jobRolesList]


def doesWordMatchFirstWordOfAnyJobRoleInList(word, jobRolesList):
    firstWordsOfEachJobRoleList = getFirstWordsOfEachJobRoleListGivenJobRolesList(jobRolesList)

    print(firstWordsOfEachJobRoleList)
    print("word: ", word)

    for i in range(len(jobRolesList)):
        if word.lower() in [firstWord.lower() for firstWord in firstWordsOfEachJobRoleList]:
            return True
    return False


def getSecondWordOfJobRoleGivenFirstWordAndJobRolesList(firstWord, jobRolesList):
    for jobRole in jobRolesList:
        words = jobRole.split()

        if words[0].lower() == firstWord:
            return words[1].lower()
    return 0

#Obtain skills required for job role
def extractKeywordsBasedOnUserInputAndCompareWithJobRolesList(userInput, jobRolesList):
    doc = nlp(userInput)

    print("doc: ", doc)
    print(getFirstWordsOfEachJobRoleListGivenJobRolesList(jobRolesList))

    keywords = []
    for i, token in enumerate(doc):
        print(token)
        if doesWordMatchFirstWordOfAnyJobRoleInList(token, jobRolesList):
            secondWord = getSecondWordOfJobRoleGivenFirstWordAndJobRolesList(token, jobRolesList)
            if doc[i+1] == secondWord:
                keywords.append(token.text)
    return keywords


def runChatbot():
    jobRolesList = getJobRolesFromJSONFile()
    print(jobRolesList)

    print(WELCOME_MESSAGE)
    userInput = input("Enter text here: ")
    keywordsInUserInput = extractKeywordsBasedOnUserInputAndCompareWithJobRolesList(userInput, jobRolesList)
    print(keywordsInUserInput)


runChatbot()




