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
    # Build the file path to Final.xlsx
    file_path = os.path.join(current_dir, "../Pre-Processing/IT Jobs.xlsx")
    ITJobs_df = pd.read_excel(file_path)
    return ITJobs_df

def initialize_itjob_headerfinal_dataset(): 
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the file path to Final.xlsx
    file_path = os.path.join(current_dir, "../Pre-Processing/itjob_headerfinal.xlsx")
    itjob_headerfinal_df = pd.read_excel(file_path)
    return itjob_headerfinal_df

def initialize_companyengagement_dataset():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the file path to Final.xlsx
    file_path = os.path.join(current_dir, "../Pre-Processing/company engagement.xlsx")
    companyengagement_df = pd.read_excel(file_path)
    return companyengagement_df

def plot_bar_graph(data, x_col):
    plt.figure(figsize=(10, 5))
    plt.xlabel(x_col)
    plt.ylabel('No. of People Hired for the Skill')
    plt.title(f'Distribution of Skills in {x_col}')
    
    data.plot(kind='bar', color='skyblue')

def plot_pie_chart(data, column):
    plt.figure(figsize=(8,8))
    plt.pie(values=column, names=data)
    plt.title('IT Entry Level Jobs')
    plt.axis('equal')
    plt.plot()

def plot_pie_chart(data, column):
    plt.figure(figsize=(8,8))
    plt.pie(values=column, names=data)
    plt.title('Education for IT Jobs')
    plt.axis('equal')
    plt.plot()

#Function to display visualzations tab
def visualizations():
    #Initialize dataset
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

def visualisations():
    #Initialize Dataset
    ITJobs_df = initialize_ITJobs_dataset()

    category_column = 'job_title' 
    sizes = ITJobs_df[category_column].value_counts()  # Counts the occurrences of each category
    job = sizes.index  # The unique category 
    sizes = sizes.values  # The corresponding sizes

    # Create the pie chart
    fig = px.pie(values=sizes, names=job, title="IT Entry Level Jobs")

    # Display pie chart 
    st.plotly_chart(fig)

def visualisations():
    #Initialize Dataset
    itjob_df = initialize_itjob_headerfinal_dataset()

    category_column = 'education_level' 
    sizes = itjob_df[category_column].value_counts()  # Counts the occurrences of each category
    labels = sizes.index  # The unique category labels
    sizes = sizes.values  # The corresponding sizes

    # Create the pie chart
    fig = px.pie(values=sizes, names=labels, title="Education for IT Jobs")

    # Display pie chart 
    st.plotly_chart(fig)

def visualisations():
    #Initialize Dataset
    companyengagement_df = initialize_companyengagement_dataset()

    # Prepare data for radar chart
    categories = list(companyengagement_df.columns)
    values = companyengagement_df.mean().tolist()

    # Print categories and values to check them
    st.write("Categories:", categories)
    st.write("Values:", values)

    # Function to create radar chart
    def create_radar_chart(categories, values):
        fig = px.line_polar(r=values, theta=categories, line_close=True)
        fig.update_traces(fill='toself')
        return fig

    # Function to update chart layout with title
    def add_title(fig, title):
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False
        )
        return fig

    # Create radar chart
    fig = create_radar_chart(categories, values)

    # Add title to the chart
    fig = add_title(fig, "Employer Branding Radar Chart")

    # Display chart
    st.plotly_chart(fig)


# ================== Radar Chart Code ==================


# # Load data for radar chart
# if radar_file_path:
#     df_radar = pd.read_excel(radar_file_path)

# # Prepare data for radar chart
# categories = list(df_radar.columns)
# values = df_radar.mean().tolist()

# # Function to create radar chart
# def create_radar_chart(categories, values):
#     fig = px.line_polar(r=values, theta=categories, line_close=True)
#     fig.update_traces(fill='toself')
#     return fig

# # Function to update chart layout with title
# def add_title(fig, title):
#     fig.update_layout(
#         title=title,
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 5]
#             )
#         ),
#         showlegend=False
#     )
#     return fig

# # Create radar chart
# fig = create_radar_chart(categories, values)

# # Add title to the chart
# fig = add_title(fig, "Company Engagement Radar Chart")

# # Display chart
# st.plotly_chart(fig)




