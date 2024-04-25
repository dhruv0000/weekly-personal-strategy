import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
import numpy as np

# Function to parse markdown file
def parse_markdown(md_content):
    slu_data = []
    for line in md_content.split('\n'):
        if '|' in line:
            parts = line.split('|')
            slu_name = parts[0].strip()
            attributes = {attr.split(':')[0].strip(): int(attr.split(':')[1].strip()) for attr in parts[1:]}
            slu_data.append({
                'Name': slu_name,
                **attributes
            })
    return slu_data

# Function to generate and save the bubble chart
def generate_bubble_chart(data, folder_path):
    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Normalize Time for the bubble size
    df['BubbleSize'] = (df['Time'] / 100) * 500  # Adjusted size multiplier

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Generate a color array
    colors = plt.cm.tab20(np.linspace(0, 1, len(df)))

    # Generate the scatter plot without names on bubbles
    scatter = ax.scatter(df['Satisfaction'], df['Importance'], s=df['BubbleSize'], c=colors, alpha=0.5)

    # Create the legend next to the plot
    legend_labels = df['Name'].tolist()
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, 
                                  markersize=10, markerfacecolor=color) for label, color in zip(legend_labels, colors)]
    ax.legend(handles=legend_handles, title="SLUs", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Set axis limits and labels
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel('Satisfaction')
    ax.set_ylabel('Importance')
    ax.set_title('Strategic Life Portfolio')
    ax.set_aspect('equal')

    # Tight layout to fit the legend
    plt.tight_layout()

    # Determine the year and week for folder naming
    current_year = datetime.datetime.now().strftime('%Y')
    current_week = datetime.datetime.now().strftime('%U')

    # Create the directory structure based on year and week
    directory = os.path.join(folder_path, current_year)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the plot as a PNG file
    plt.savefig(os.path.join(directory, 'Week_' + current_week + '_Strategic_Life_Portfolio.png'), bbox_inches='tight')
    plt.close()

# Read the markdown file
with open('input.md', 'r') as file:
    md_content = file.read()

# Parse the markdown content to get the data
data = parse_markdown(md_content)

# Define the output folder path (e.g., the current working directory)
output_folder_path = os.getcwd()

# Generate and save the bubble chart
generate_bubble_chart(data, output_folder_path)
