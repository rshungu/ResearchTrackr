import streamlit as st
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import matplotlib.pyplot as plt


DATABASE_URL = "postgresql://postgres:tanzania08@localhost:5432/research_publications"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=0)  # Ensures fresh data loading

def load_data():
    query = "SELECT * FROM hematology.hematology_dataset;"
    return pd.read_sql(query, engine)  # ✅ Uses SQLAlchem

df = load_data()

st.title("Tracking Research Publications")

# ---- SIDEBAR ----
st.sidebar.title("🔍 Filter Research")
search_query = st.sidebar.text_input("Search by Research Title or Student Number")

# Filters
university_level = st.sidebar.selectbox("University Level", ["All"] + sorted(df["university_level"].unique()))
degree_filter = st.sidebar.selectbox("Degree Program", ["All"] + sorted(df["degree_program"].unique()))
category_filter = st.sidebar.selectbox("Research Category", ["All"] + sorted(df["research_category"].unique()))
supervisor_filter = st.sidebar.selectbox("Lead Supervisor", ["All"] + sorted(df["lead_supervisor"].unique()))
publication_filter = st.sidebar.radio("Publication Status", ["All", "Published", "Not Published"])
dataset_filter = st.sidebar.radio("Dataset Available?", ["All", "Yes", "No"])

# Apply Filters
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df["research_title"].str.contains(search_query, case=False)]
if university_level != "All":
    filtered_df = filtered_df[filtered_df["university_level"] == university_level]
if degree_filter != "All":
    filtered_df = filtered_df[filtered_df["degree_program"] == degree_filter]
if category_filter != "All":
    filtered_df = filtered_df[filtered_df["research_category"] == category_filter]
if supervisor_filter != "All":
    filtered_df = filtered_df[filtered_df["lead_supervisor"] == supervisor_filter]
if publication_filter == "Published":
    filtered_df = filtered_df[filtered_df["is_paper_published"] == True]
elif publication_filter == "Not Published":
    filtered_df = filtered_df[filtered_df["is_paper_published"] == False]
if dataset_filter == "Yes":
    filtered_df = filtered_df[filtered_df["is_dataset_available"] == True]
elif dataset_filter == "No":
    filtered_df = filtered_df[filtered_df["is_dataset_available"] == False]


# ---- DASHBOARD ----

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("📄 Total Papers", len(df))
col2.metric("✅ Published Papers", len(df[df["is_paper_published"] == True]))
col3.metric("🚀 Unpublished Papers", len(df[df["is_paper_published"] == False]))

# Extracting the data for completed papers per year and published papers per year
completed_papers_per_year = df.groupby('completion_year').size().reset_index(name='completed_papers').sort_index()

# Create the bar charts using Plotly Express (horizontal bars)
fig4 = px.bar(completed_papers_per_year, 
              x='completed_papers', 
              y='completion_year', 
              orientation='h', 
              title="Completed Papers per Year", 
              labels={'completed_papers': 'Number of Papers', 'completion_year': 'Year'},
              color='completed_papers', 
              color_continuous_scale='viridis')

published_papers_per_year = df.groupby('published_year').size().reset_index(name='published_papers').sort_index()

# Create the bar charts using Plotly Express (horizontal bars)
fig5 = px.bar(published_papers_per_year, 
              x='published_papers', 
              y='published_year', 
              orientation='h', 
              title="Published Papers per Year", 
              labels={'published_papers': 'Number of Papers', 'published_year': 'Year'},
              color='published_papers', 
              color_continuous_scale='viridis')

# Display the charts side by side in Streamlit
st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Research Insights")
col4,col5,col6 = st.columns(3)
col4.metric("📊 Total Categories", len(df["research_category"].unique()))
col5.metric("📊 Total Degree Programs", len(df["degree_program"].unique()))
col6.metric("📊 Total Supervisors", len(df["lead_supervisor"].unique()))

# Charts
fig1 = px.bar(df["research_category"].value_counts(), title="Research Papers by Category")
fig2 = px.bar(df["degree_program"].value_counts(), title="Research Papers by Degree Program")
fig3 = px.bar(df["lead_supervisor"].value_counts(), title="Research Papers by Lead Supervisor")

# Group by both 'degree_program' and 'research_category', then count occurrences
df_grouped = df.groupby(['degree_program', 'research_category']).size().reset_index(name='count')

# Create a bar chart using Plotly Express
fig = px.bar(df_grouped, 
             x="degree_program", 
             y="count", 
             title="Study Design by Degree Program", 
             labels={"degree_program": "Degree Program", "count": "Number of Research Papers", "research_category": "Research Category"},
             barmode='stack',
             color="research_category",
             color_discrete_sequence=px.colors.qualitative.Prism             
            )

st.plotly_chart(fig, use_container_width=True)

# Count number of students per supervisor
supervisor_count = df.groupby('lead_supervisor')['student_register_number'].nunique().reset_index()
supervisor_count.columns = ['lead_supervisor', 'num_students']
supervisor_count = supervisor_count.sort_values(by='num_students', ascending=False)  # Sort in descending order


# Streamlit section
st.subheader("Number of Students Supervised by Each Supervisor")

# Create the bar chart (horizontal)
fig = px.bar(supervisor_count, 
             x='num_students', 
             y='lead_supervisor', 
             orientation='h', 
             labels={'num_students': 'Number of Students', 'lead_supervisor': 'Supervisor'}, 
             title="Supervisors and Their Number of Students",
             color='num_students',
             color_continuous_scale='viridis')


# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# ---- DETAILED TABLE ----
st.subheader("📄 Research Papers")

column_mapping = {
    "student_register_number": "Student ID",
    "university_level": "University Level",
    "degree_program": "Degree Program",
    "research_title": "Research Title",
    "research_category": "Study Design",
    "research_subcategory": "Research Category",
    "lead_supervisor": "Supervisor",
    "start_year": "Start Date",
    "completion_year": "Completion Date",
    "is_paper_published": "Published?",
    "published_year":"Publication Date",  
    "is_dataset_available": "Dataset Available?",
}

# Rename the DataFrame columns
filtered_df = filtered_df.rename(columns=column_mapping)

# Display in Streamlit with the new headers and hide index
st.dataframe(filtered_df, hide_index=True)