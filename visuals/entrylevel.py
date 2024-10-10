import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Define the path to your Excel file 

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the file path to Final.xlsx
file_path = os.path.join(current_dir, "../Pre-Processing/IT Jobs.xlsx")

#Read the excel file
df = pd.read_excel(file_path)

category_column = 'job_title' 
sizes = df[category_column].value_counts()  # Counts the occurrences of each category
job = sizes.index  # The unique category 
sizes = sizes.values  # The corresponding sizes

# Create the pie chart
fig = px.pie(values=sizes, names=job, title="IT Entry Level Jobs")

# Display pie chart 
st.plotly_chart(fig)
