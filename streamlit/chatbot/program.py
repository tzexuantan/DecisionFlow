import pandas as pd

#Read job dataset
job_data = pd.read_excel("Pre-Processing/Final.xlsx")

#Function to filter jobs based on skills
def filter_jobs(user_skills):
    # Convert user input into a list of skills (split by commas)
    skills_list = [skill.strip().lower() for skill in user_skills.split(',')]
    
    # Filter jobs by checking if any of the user's skills match the job's required skills
    filtered_jobs = job_data[job_data['Sub-skill'].apply(lambda x: any(skill in x.lower() for skill in skills_list))]
    
    # Return the filtered job results as a dictionary
    return filtered_jobs.to_dict(orient='records')

#Trial to see if able to filter
# user_input = input("Please enter skills:")

# filter_jobs(user_input)








# import pandas as pd

# # Load your dataset (make sure it includes new columns like location, salary, experience, etc.)
# data = pd.read_csv('job_data.csv')

# # Function to filter jobs based on user input
# def filter_jobs(user_input):
#     # Split and process user input (e.g., skills, location, etc.)
#     skills_input = [skill.strip().lower() for skill in user_input.get('skills', '').split(',')]
#     location_input = user_input.get('location', '').lower()
#     salary_input = user_input.get('salary', 0)
#     experience_input = user_input.get('experience', 0)

#     # Start filtering by skills (other columns can be added with conditional logic)
#     filtered_jobs = data[
#         data['skills'].apply(lambda x: any(skill in x.lower() for skill in skills_input)) &
#         (data['location'].str.lower() == location_input if location_input else True) &
#         (data['salary'] >= int(salary_input)) &
#         (data['experience'] >= int(experience_input))
#     ]

#     # Return the filtered job results as a dictionary
#     return filtered_jobs.to_dict(orient='records')
