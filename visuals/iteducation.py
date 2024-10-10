import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the file path to Final.xlsx
file_path = os.path.join(current_dir, "../Pre-Processing/itjob_headerfinal.xlsx")

#Read the excel file
df = pd.read_excel(file_path)

category_column = 'education_level' 
sizes = df[category_column].value_counts()  # Counts the occurrences of each category
labels = sizes.index  # The unique category labels
sizes = sizes.values  # The corresponding sizes

# Create the pie chart
fig = px.pie(values=sizes, names=labels, title="Education for IT Jobs in Singapore")

# Display pie chart 
st.plotly_chart(fig)
