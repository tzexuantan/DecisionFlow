# main.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt


def initialize_indeed_dataset():
    #Obtain current directory file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    indeed_data_file_path = os.path.join(current_dir, "../dataset/Final.xlsx")
    indeed_df = pd.read_excel(indeed_data_file_path)
    return indeed_df

def initialize_engagement_dataset():
    #Obtain current directory file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    company_engagement_file_path = os.path.join(current_dir, "company engagement.xlsx")
    engagement_df = pd.read_excel(company_engagement_file_path)
    return engagement_df

def initialize_ITJobs_dataset():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    file_path = os.path.join(current_dir, "../Pre-Processing/IT Jobs.xlsx")
    ITJobs_df = pd.read_excel(file_path)
    return ITJobs_df

def initialize_itjob_headerfinal_dataset(): 
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    file_path = os.path.join(current_dir, "../Pre-Processing/itjob_headerfinal.xlsx")
    itjob_headerfinal_df = pd.read_excel(file_path)
    return itjob_headerfinal_df

def initialize_salary_dataset():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    file_path = os.path.join(current_dir, "../dataset/Salary_Data_Based_country_and_race.csv")
    itjob_salary_df = pd.read_excel(file_path)
    return itjob_salary_df

def initialize_skillset_dataset():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    file_path = os.path.join(current_dir, "../dataset/Skillset.xlsx")
    itjob_skillset_df = pd.read_excel(file_path)
    return itjob_skillset_df

def initialize_certificate_dataset():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File path to the dataset
    file_path = os.path.join(current_dir, "../dataset/Certificate.csv")
    itjob_Certificate_df = pd.read_excel(file_path)
    return itjob_Certificate_df

def plot_bar_graph(data, x_col, title):
    plt.figure(figsize=(10, 5))
    plt.xlabel(x_col)
    plt.ylabel()
    plt.title(title)
    
    data.plot(kind='bar', color='skyblue')

def plot_pie_chart(sizes, labels, title):
    plt.figure(figsize=(8,8))
    plt.pie(values=sizes, names=labels, title=title)
    plt.axis('equal')
    plt.plot()

def plot_horizontal_graph(data, col1, col2, title):
    plt.figure(figsize=(10, 6))
    plt.barh(data[col1], data[col2], label=col2)
    plt.xlabel('Salary')
    plt.ylabel('Job Title')
    plt.title(title)
    plt.legend()
    plt.savefig('plot.png')
    st.pyplot(plt)

def plot_histogram(data,col,chosen, title):
    plt.figure(figsize=(10, 6))
    plt.hist(data[col], bins=len(chosen), edgecolor='k', alpha=0.7)
    plt.xlabel('Sub-skill')
    plt.ylabel('Frequency')
    plt.title(title)
    st.pyplot(plt)

def plot_line_chart(data, title):
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data.values, color='b', linestyle='-', linewidth=2, marker='o')
        plt.title(title)
        plt.xlabel('Certificate')
        plt.ylabel('No. of people with the certificate')
        plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
        plt.grid(True)
        st.pyplot(plt)

#Function to display visualzations tab
def visualizations():

    indeed_df = initialize_indeed_dataset()

    # Bar Graph
    st.title("Distributions of Skills")

    # Auto-select a fixed column (replace 'Skills' with the actual column name in your file)
    column_to_plot = "Skill"  # Set this to the column name for skills in your Excel file

    if column_to_plot not in indeed_df.columns:
        st.error(f"Column '{column_to_plot}' not found in the Excel file.")
    else:
        # Check if the column contains object-type data
        if indeed_df[column_to_plot].dtype == 'object':
            # Count occurrences of each category (sub-skills)
            category_counts = indeed_df[column_to_plot].value_counts()

            # Check if category_counts is not empty
            if not category_counts.empty:
                # Multiselect filter for sub-skills
                selected_skills = st.multiselect(
                    'Select specific skills to visualize',
                    options=category_counts.index.tolist(),
                    default=category_counts.index.tolist()  # Default to show all
                )

                # Create a filtered data series based on selected skills
                filtered_counts = category_counts[selected_skills]

                # Ensure that filtered_counts is not empty before using min() and max()
                if not filtered_counts.empty:
                    # Add a slider for selecting the range of counts to filter
                    min_count, max_count = int(filtered_counts.min()), int(filtered_counts.max())
                    selected_range = st.slider(
                        'Select count range for filtering',
                        min_value=min_count,
                        max_value=max_count,
                        value=(min_count, max_count)
                    )

                    # Further filter the counts based on the selected range
                    filtered_counts = filtered_counts[(filtered_counts >= selected_range[0]) & (filtered_counts <= selected_range[1])]

                    # Create a bar chart for the filtered sub-skills
                    if not filtered_counts.empty:
                        plot_bar_graph(filtered_counts, column_to_plot)
                        st.pyplot(plt)
                    else:
                        st.warning("No data available for the selected count range.")
                else:
                    st.warning("No skills selected or found.")
            else:
                st.warning("Please select at least one skill to visualize.")


    #Initialize Dataset
    entryleveljobs_df = initialize_ITJobs_dataset()

    category_column1 = 'job_title' 
    sizes1 = entryleveljobs_df[category_column1].value_counts()  # Counts the occurrences of each category
    job1 = sizes1.index  # The unique category 
    sizes1 = sizes1.values  # The corresponding sizes

    # Create the pie chart
    fig = px.pie(values1=sizes1, names1=job1, title1="IT Entry Level Jobs")

    # Display pie chart 
    st.plotly_chart(fig)


    #Initialize Dataset
    education_df = initialize_itjob_headerfinal_dataset()

    category_column2 = 'education_level' 
    sizes2 = education_df[category_column2].value_counts()  # Counts the occurrences of each category
    labels2 = sizes2.index  # The unique category labels
    sizes2 = sizes2.values  # The corresponding sizes

    # Create the pie chart
    fig = px.pie(values2=sizes2, names2=labels2, title="Education for IT Jobs")

    # Display pie chart 
    st.plotly_chart(fig)


    #Initialize Dataset
    indeed_df = initialize_indeed_dataset()
    
    # Bar Graph
    st.title("Companies that are hiring the IT roles")
    column_to_plot3 = "Company/Candidate Name"  # Replace this with your specific column name

    if indeed_df[column_to_plot3].dtype == 'object':
        # Count occurrences of each category
        category_counts3 = indeed_df[column_to_plot3].value_counts()

        # Display the top 3 companies hiring the most IT roles for the entire dataset
        top3_companies = category_counts3.nlargest(3)
        st.write("**Top 3 companies that are hiring the most IT roles:**")
        for company, count in top3_companies.items():
            st.write(f"{company}: {count} roles")

        # Check if category_counts is not empty
        if not category_counts3.empty:
            # Multi-select to choose specific data
            selected_skills = st.multiselect(
                'Select companies to visualize',
                options3=category_counts3.index.tolist(),  # Provide the list of options
                default=[]  # Default to show none
            )

    #Initialize Dataset
    itjob_salary_df = initialize_salary_dataset
    
    st.title("Salary ranges for IT jobs")
    column1 = 'Job Title'
    column2 = 'Salary'

    # Convert Salary column to numeric
    itjob_salary_df[column2] = pd.to_numeric(itjob_salary_df[column2], errors='coerce')

    # Handle missing values
    itjob_salary_df[column1].fillna('', inplace=True)
    itjob_salary_df[column2].fillna(0, inplace=True)

    # Add number inputs for filtering salary range
    min_salary = itjob_salary_df[column2].min()
    max_salary = itjob_salary_df[column2].max()
    min_value = st.number_input('Min Salary', min_value=min_salary, max_value=max_salary, value=min_salary)
    max_value = st.number_input('Max Salary', min_value=min_salary, max_value=max_salary, value=max_salary)

    # Filter the DataFrame based on the salary range
    filtered_df4 = itjob_salary_df[(itjob_salary_df[column2] >= min_value) & (itjob_salary_df[column2] <= max_value)]

    # Update job titles based on the filtered DataFrame
    job_titles = filtered_df4[column1].unique()
    selected_job_titles = st.multiselect('Select Job Titles', job_titles, default=[])

    # Further filter the DataFrame based on selected job titles
    filtered_df4 = filtered_df4[filtered_df4[column1].isin(selected_job_titles)]


    itjob_skillset_df = initialize_skillset_dataset

    st.title("Most Commonly Required IT Competencies in the Industry")
    column = 'Sub-skill' 

    # Handle missing values
    itjob_skillset_df[column].fillna('Unknown', inplace=True)

    # Update sub-skills based on the DataFrame
    sub_skills = filtered_df5[column].unique()
    selected_sub_skills = st.multiselect('Select Sub-skills', sub_skills, default=[])

    # Further filter the DataFrame based on selected sub-skills
    filtered_df5 = filtered_df5[filtered_df5[column].isin(selected_sub_skills)]


    itjob_Certificate_df = initialize_certificate_dataset
    
    st.title("Distribution of Certificates in the Data File")
    if 'certification_text' in itjob_Certificate_df.columns:
    # Count occurrences of each certificate
        certificate_counts = itjob_Certificate_df['certification_text'].value_counts().sort_index()

    # Display the top 3 most common certificates
        top3_certificates = certificate_counts.nlargest(3)
        st.write("**Top 3 Most Common Certificates:**")
        for certificate, count in top3_certificates.items():
            st.write(f"{certificate}: {count} people")

        # Multi-select to filter certificates
        selected_certificates = st.multiselect(
            'Select certificates to visualize',
            options6=certificate_counts.index.tolist(),  # Provide the list of options
            default=[]  # Default to show none
        )

        # Filter the data based on selected certificates
        filtered_counts = certificate_counts[selected_certificates]
