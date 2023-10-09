import streamlit as st
import pandas as pd
import os
import threading
import rpy2.robjects as robjects

from PIL import Image

# List of packages to install and load
packages_to_install = ["networktools", "smacof", "MPsychoR", "psych", "eigenmodel", "dplyr", "NetworkComparisonTest"]
libraries_to_load = ["networktools", "MPsychoR", "smacof", "qgraph", "psych", "eigenmodel", "dplyr", "ggplot2", "IsingFit"]


import subprocess

# List of packages to install
packages_to_install = ["networktools", "smacof", "MPsychoR", "psych", "eigenmodel", "dplyr", "NetworkComparisonTest"]

# Specify the user library path
user_library_path = "~/.R/library"

# Install necessary packages
for package in packages_to_install:
    subprocess.run(["Rscript", "-e", f'install.packages("{package}", lib="{user_library_path}")'])


# Install necessary packages
for package in packages_to_install:
    robjects.r(f'if(!("{package}" %in% installed.packages())) install.packages("{package}")')

# Load necessary R libraries
for library in libraries_to_load:
    robjects.r(f'library({library})')


def load_file(uploaded_file):
    """Load the uploaded file as a DataFrame."""
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    return df

def display_dataframe_preview(df):
    """Display a preview of the DataFrame."""
    st.write("Preview of the DataFrame:")
    st.write(df)

def display_selected_columns(df, selected_columns):
    """Display the selected columns from the DataFrame."""
    st.write("You selected the following columns:")
    st.write(selected_columns)

    # Display the preview of selected columns
    st.write("Preview of selected columns:")
    st.write(df[selected_columns])


def main():
    st.title("Network Visualizer")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.info("File successfully uploaded!")
        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getvalue())

        # Load the uploaded file as a DataFrame
        df = load_file(uploaded_file)
        display_dataframe_preview(df)

        # Allow users to select columns
        selected_columns = st.multiselect("Select columns", df.columns)

        if selected_columns:
            display_selected_columns(df, selected_columns)

            if len(selected_columns)>1:
                # Read the CSV file
                robjects.r(f'dt <- read.csv("{uploaded_file.name}", header=TRUE)')

                # Define the column names you want to select
                columns_to_select = selected_columns

                # Construct a string with the column names
                columns_to_select_str = ', '.join([f'"{col}"' for col in columns_to_select])

                # Use the constructed string in the R code to select columns
                robjects.r(f'netdt1 <- select(dt, {columns_to_select_str})')

                robjects.r('net1 <- qgraph(cor_auto(netdt1), n = nrow(netdt1), lambda.min.ratio = 0.05, default = "EBICglasso", layout="spring", vsize = 16, gamma = 0.2, tuning = 0.2, refit = TRUE)')


                # # Define the file path for the image
                # image_path = "graph_plot.png"

                # # Delete the existing image file if it exists
                # if os.path.exists(image_path):
                #     os.remove(image_path)

               # Plot the qgraph for the correlation difference and save it as an image
                try:
                    robjects.r(f'png("graph_plot.png", width=800, height=600)')
                    robjects.r('qgraph(net1, maximum=0.29)')
                    robjects.r('dev.off()')  # Close the PNG device
                except:
                  pass
                                                
                if os.path.exists("graph_plot.png"):
                    plot_image = Image.open("graph_plot.png")
                    st.image(plot_image, caption='Network Plot', use_column_width=True)

                # # Display the saved plot as an image
                # Image(filename='/content/qgraph_plot.png')
        

        



if __name__ == "__main__":
    main()
