import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sqlalchemy import create_engine

# Sample data
# dataframe1 = pd.read_excel('random2.xlsx')
engine = create_engine('sqlite:///test_scores.db')

df = pd.read_sql('SELECT * from test_scores', engine)

st.title("Student Performance Dashboard")

st.write("""
This dashboard provides an overview of the student's performance across different subjects and test categories.
""")

# Select the test number
test_number = st.selectbox('Select Test Number', df['test_no'])

# Filter the data for the selected test
test_data = df[df['test_no'] == test_number]

# Display selected test data
st.write(f"### Performance in Test {test_number}")
st.write(test_data)

# Bar plot for the selected test performance
fig, ax = plt.subplots()
subjects = ['maths', 'science', 'social']
scores = test_data[subjects].values.flatten()
ax.bar(subjects, scores, color=['blue', 'green', 'red'])
ax.set_ylim(0, 4)
ax.set_ylabel('Score')
ax.set_title(f'Scores in Test {test_number}')
st.pyplot(fig)

# Average scores for each subject
avg_scores = df[subjects].mean()

st.write("### Average Scores Across All Tests")
st.write(avg_scores)

# Line plot for performance over tests
fig, ax = plt.subplots()
for subject in subjects:
    ax.plot(df['test_no'], df[subject], marker='o', label=subject)
ax.set_xlabel('Test Number')
ax.set_ylabel('Score')
ax.set_title('Performance Over Tests')
ax.legend()
st.pyplot(fig)

# Category distribution
st.write("### Test Category Distribution")
fig, ax = plt.subplots()
sns.countplot(x='category', data=df, ax=ax)
ax.set_title('Count of Each Category')
st.pyplot(fig)

# Correlation heatmap
st.write("### Correlation Between Subjects")
fig, ax = plt.subplots()
corr = df[subjects].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix')
st.pyplot(fig)

st.write("### Detailed Analysis by Category")
category = st.selectbox('Select Category', df['category'].unique())

# Filter the data by selected category
category_data = df[df['category'] == category]

# Boxplot for selected category
fig, ax = plt.subplots()
sns.boxplot(data=category_data[subjects], ax=ax)
ax.set_title(f'Score Distribution in {category.capitalize()} Category')
st.pyplot(fig)
