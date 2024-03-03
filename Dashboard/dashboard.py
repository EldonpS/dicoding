import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
current_dir = os.path.dirname(__file__)
data1_path = os.path.join(current_dir, "../Data/guanyuan_data.csv")
guan_df = pd.read_csv(data1_path)

current_dir = os.path.dirname(__file__)
data2_path = os.path.join(current_dir, "../Data/gucheng_data.csv")
gucheng_df = pd.read_csv(data2_path)

combined_df = pd.concat([guan_df, gucheng_df])

# Function to display selected data information
def display_data_hist(data):
    st.subheader("Data Information:")
    st.text(data.hist())

# Function to display selected data description
def display_data_description(data):
    st.subheader("Data Description:")
    st.text(data.describe())

# Function for Question 1 visualization and conclusion
def visualize_question_1():
    max_avg_pm10_per_month = guan_df.groupby("month")["PM10"].mean().idxmax()
    max_avg_pm10_value = guan_df.groupby("month")["PM10"].mean().max()

    min_avg_pm10_per_month = guan_df.groupby("month")["PM10"].mean().idxmin()
    min_avg_pm10_value = guan_df.groupby("month")["PM10"].mean().min()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="month", y="PM10", data=guan_df, marker="o", label="Monthly Trend", ax=ax)
    ax.scatter(x=max_avg_pm10_per_month, y=max_avg_pm10_value, color="green", s=100, label="Max Avg PM10")
    ax.scatter(x=min_avg_pm10_per_month, y=min_avg_pm10_value, color="red", s=100, label="Min Avg PM10")
    ax.set_title("Monthly Trend of PM10 (Guanyuan Station)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg PM10")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Conclusion for Question 1:")
    st.text("Based on the monthly trend, it is observed that there is a significant difference in PM10 levels each month.")
    st.text(f"The highest average PM10 value is in month {max_avg_pm10_per_month} and the lowest is in month {min_avg_pm10_per_month}")

# Function for Question 2 visualization and conclusion
def visualize_question_2():
    fig, axes = plt.subplots(nrows=2, figsize=(12, 10))

    # Plot for PM2.5
    sns.lineplot(x='hour', y='PM2.5', data=guan_df, ax=axes[0], label='PM2.5')
    axes[0].set_title('PM2.5 Trend Throughout Operating Hours (Guanyuan Station)')
    axes[0].set_xlabel('Operating Hours')
    axes[0].set_ylabel('PM2.5')

    # Plot for O3
    sns.lineplot(x='hour', y='O3', data=guan_df, ax=axes[1], label='O3')
    axes[1].set_title('O3 Trend Throughout Operating Hours (Guanyuan Station)')
    axes[1].set_xlabel('Operating Hours')
    axes[1].set_ylabel('O3')

    # Display the plot using st.pyplot
    st.pyplot(fig)

    st.subheader('Conclusion for Question 2:')
    st.text('Based on the correlation analysis, there is no significant correlation between operating hours, PM2.5 levels, and O3 levels.')
    st.text('However, from the trend graph throughout the operation hours, it can be concluded that PM2.5 levels are highest in the morning and evening, while O3 levels are highest in the afternoon to evening.')

# Function for Question 3 visualization and conclusion
    
def visualize_question_3():
    fig, ax = plt.subplots(figsize=(12, 6))  # Use only one row for the subplot

    # Aggregate data to avoid duplicate labels issue
    agg_df = combined_df.groupby(['year', 'station'])['O3'].mean().reset_index()

    # Plot the lineplot using agg_df
    sns.lineplot(x='year', y='O3', hue='station', data=agg_df, err_style=None, ax=ax)

    # Set plot properties
    ax.set_title('Comparison of O3 Levels Over Years (Guanyuan vs Gucheng)')
    ax.set_xlabel('Year')
    ax.set_ylabel('O3 Level')
    ax.legend(title='Station')

    # Display the plot using st.pyplot
    st.pyplot(fig)
    plt.close()  # Close the figure to prevent duplicate plots

    st.subheader('Conclusion for Question 3:')
    st.text("Based on the graph above, it can be seen that year-on-year O3 levels at Guanyuan Station and Gucheng Station have decreased quite significantly.")

    
# Feature 1: Dropdown for sorting data
st.sidebar.header("Feature 1: Sort Data")
selected_data = st.sidebar.selectbox("Select Data", ["Guanyuan", "Gucheng"])
selected_function = st.sidebar.selectbox("Select Function", ["Sort by PM10", "Sort by O3", "Display Histogram", "Display Description",])
selected_columns = st.sidebar.multiselect("Select Columns to Display", guan_df.columns)

# Display sorted data or selected function
st.subheader("Selected Data or Function:")

selected_dataset = guan_df if selected_data == "Guanyuan" else gucheng_df
if "Sort" in selected_function:
    if selected_function == "Sort by PM10":
        sorted_data = selected_dataset.sort_values(by="PM10")
    elif selected_function == "Sort by O3":
        sorted_data = selected_dataset.sort_values(by="O3")
    elif selected_function == "Sort by PM2.5":
        sorted_data = selected_dataset.sort_values(by="PM2.5")
    st.dataframe(sorted_data[selected_columns])

else:
    if selected_function == "Display Histogram":
        display_data_hist(selected_dataset)
    elif selected_function == "Display Description":
        display_data_description(selected_dataset)

# Feature 2: Question and Visualization
st.sidebar.header("Feature 2: Question and Visualization")
selected_question = st.sidebar.selectbox("Select a Question", ["Select a Question", "Question 1", "Question 2", "Question 3"])

if selected_question != "Select a Question":
    if selected_question == "Question 1":
        selected = "In which month did the air quality reach the highest and lowest based on PM10 data in 2013?"
    elif selected_question == "Question 2":
        selected = "Is there a correlation between operating hours and air quality based on PM 2.5 and O3 levels?"
    elif selected_question == "Question 3":
        selected = "How does the O3 level vary from year to year at Guanyuan and Gucheng stations?"
    else:
        selected = "Wrong input"

    st.subheader(f"Selected Question: {selected}")

    # Display visualization and conclusion based on the selected question
    if selected_question == "Question 1":
        visualize_question_1()

    elif selected_question == "Question 2":
        visualize_question_2()

    elif selected_question == "Question 3":
        visualize_question_3()
