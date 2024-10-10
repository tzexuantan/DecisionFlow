import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Title of the app
st.title("Distributions of Skills")

# Define the path to your Excel file 
# file_path = "../Pre-Processing/Final.xlsx"

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the file path to Final.xlsx
file_path = os.path.join(current_dir, "../dataset/Final.xlsx")

# Read the Excel file
df = pd.read_excel(file_path)

# Display the dataframe
# st.write("Data from the Excel file:")
# st.dataframe(df)

# Show the data types of each column
st.write("Data types:")
st.write(df.dtypes)

# Auto-select a fixed column (replace 'Skills' with the actual column name in your file)
column_to_plot = "Skill"  # Set this to the column name for skills in your Excel file

if column_to_plot not in df.columns:
    st.error(f"Column '{column_to_plot}' not found in the Excel file.")
else:
    # Check if the column contains object-type data
    if df[column_to_plot].dtype == 'object':
        # Count occurrences of each category (sub-skills)
        category_counts = df[column_to_plot].value_counts()

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

                # Function to plot the graph
                def plot_graph(data):
                    plt.figure(figsize=(10, 5))
                    data.plot(kind='bar', color='skyblue')
                    plt.xlabel(column_to_plot)
                    plt.ylabel('No. of People Hired for the Skill')

                # Function to add title
                def add_title(title):
                    plt.title(title)

                # Create a bar chart for the filtered sub-skills
                if not filtered_counts.empty:
                    plot_graph(filtered_counts)
                    add_title(f'Distribution of Skills in {column_to_plot}')
                    st.pyplot(plt)
                else:
                    st.warning("No data available for the selected count range.")
            else:
                st.warning("No skills selected or found.")
        else:
            st.warning("Please select at least one skill to visualize.")
    else:
        st.warning("Please select a non-numeric column for plotting.")
