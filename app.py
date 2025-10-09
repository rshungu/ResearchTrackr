import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

projects_url = "https://raw.githubusercontent.com/rshungu/ResearchTrackr/main/data/research_projects.csv"
students_url = "https://raw.githubusercontent.com/rshungu/ResearchTrackr/main/data/students.csv"
supervisors_url = "https://raw.githubusercontent.com/rshungu/ResearchTrackr/main/data/supervisors.csv"
logo_path = r"https://raw.githubusercontent.com/rshungu/ResearchTrackr/main/researchtrackr_logo.png"


projects_df = pd.read_csv(projects_url)
students_df = pd.read_csv(students_url)
supervisors_df = pd.read_csv(supervisors_url)

# -------------------------------
# Streamlit Page Config
# -------------------------------
# --- 🌐 Set Page Configuration ---
st.set_page_config(
    page_title="ResearchTrackr",       # Browser tab title
    page_icon="📚",                    # Emoji or image as favicon
    layout="wide",                     # Use full screen width
    initial_sidebar_state="expanded"   # Sidebar visible by default
)

st.markdown("""
<style>
.custom-header {
    font-family: 'Calibri Light', Calibri Light, Calibri Light;
    font-size: 28px;
    font-weight: 400;
    color: #2C3E50;
    margin-top: 20px;
    margin-bottom: 10px;
}
.custom-header-bold {
    font-family: 'Calibri Light', Calibri Light, Calibri Light;
    font-size: 30px;
    font-weight: 700; /* Bold weight */
    color: #1A252F;
    margin-top: 25px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


apptitle = "ResearchTrackr"
st.set_page_config(page_title=apptitle, page_icon=logo_path, layout="wide")
st.image(logo_path, use_container_width=True )

# -------------------------------
## About / How to Use Section
# -------------------------------
_, exp_col, _ = st.columns([1, 3, 1])  # center the content

with exp_col:
    with st.expander("**About ResearchTrackr**"):
        st.markdown("""
        **ResearchTrackr** is a comprehensive dashboard for tracking student research projects, supervisors, 
        and publication statuses at your institution.  

        **Key Features:**
        - **Search & Filters:** Filter research by category, supervisor, year, or project status.
        - **Dashboard Metrics:** View total projects, ongoing/completed projects, and total students.
        - **Visualizations:** Explore research distribution, trends over years, and supervisor contributions.
        - **Leaderboards:** Identify top supervisors overall and per year, as well as those with the most completed projects.
        - **Expandable Table:** Inspect full project details dynamically.
        - **Download Option:** Export filtered data as CSV for further analysis.

        This tool is ideal for students, academic staff, and research administrators to **monitor, analyze, and visualize research activities** efficiently.
        """)

# -------------------------------
## Sidebar Filters
# -------------------------------
st.sidebar.caption("Made by an [Rehema Shungu](https://www.linkedin.com/in/rehema-shungu/)")
st.sidebar.caption(
    "Check out the full ResearchTrackr project on GitHub Source Code [here](https://github.com/rshungu/ResearchTrackr.git)."
)

st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Category", projects_df['category'].unique())
program_filter = st.sidebar.multiselect("Level",students_df['program'].unique())
status_filter = st.sidebar.multiselect("Status", projects_df['status'].unique())
year_filter = st.sidebar.slider("Year Published", 2021, 2024, (2021, 2024))
supervisor_filter = st.sidebar.multiselect("Supervisor", supervisors_df['name'].tolist())
students_df['year_of_study_date'] = pd.to_datetime(students_df['year_of_study'], format='%Y')

# -------------------------------
## Filter dataframe
# -------------------------------
filtered_df = projects_df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
if year_filter:
    filtered_df = filtered_df[
        filtered_df['year_published'].between(year_filter[0], year_filter[1])
    ]
if supervisor_filter:
    sup_ids = supervisors_df[supervisors_df['name'].isin(supervisor_filter)]['supervisor_id']
    filtered_df = filtered_df[filtered_df['supervisor_id'].isin(sup_ids)]

st.markdown("<h2 class='custom-header-bold'> Dashboard Metrics</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Ongoing Projects", len(filtered_df[filtered_df['status']=="Ongoing"]))
col2.metric("Completed Projects", len(filtered_df[filtered_df['status']=="Completed"]))
col3.metric("Total Students", students_df['student_id'].nunique())

st.markdown("<h2 class='custom-header-bold'> Student & Research Category Insights</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

# --- Left: Student Program Distribution ---
with col1.container(border=True, height="stretch"):
    student_counts = students_df.groupby("program")["student_id"].nunique().reset_index()
    student_counts.columns = ["Program", "Number of Students"]

    fig_program = px.bar(
        student_counts,
        x="Program",
        y="Number of Students",
        color="Program",
        text="Number of Students",
        title="Student Distribution by Program",
    )
    fig_program.update_layout(
        showlegend=False,
        height = 600,
        width = 600,
        title=dict(
            text="Student Distribution by Program",
            font=dict(size=22, family="Calibri Light", color="#2C3E50"),
            x=0.5,           # ✅ Centers the title horizontally
            xanchor="center", # Keeps it properly centered
            yanchor="top"
        ),
        xaxis=dict(side="bottom"),
        # legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center",x=0.5,maxheight=0.1, title_text="Category"),
        )
    st.plotly_chart(fig_program, use_container_width=True)

# --- Right: Research Category Distribution ---
with col2.container(border=True,height="stretch"):
    category_counts = projects_df["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]

    fig_category = px.pie(
        category_counts,
        values="Count",
        names="Category",
        title="Research Distribution by Category",
        hole=.45
    )
    fig_category.update_traces(textposition = "inside",textinfo="percent+label")
    fig_category.update_layout(
        showlegend=False,
        height = 600,
        width = 600,
        title=dict(
            text="Research Distribution by Category",
            font=dict(size=22, family="Calibri Light", color="#2C3E50"),
            x=0.5,           # ✅ Centers the title horizontally
            xanchor="center", # Keeps it properly centered
            yanchor="top"
        ),
        xaxis=dict(side="top"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center",x=0.5,maxheight=0.1, title_text="Category"),
        )
    st.plotly_chart(fig_category, use_container_width=True)

col3, col4 = st.columns(2)
# --- Container with border and stretch effect ---
with col3.container(border=True,height="stretch"):
    # --- Research Output Trend Over the Years (Line Chart)
    yearly_trends = projects_df.groupby("year_published")["project_id"].count().reset_index()
    yearly_trends.columns = ["Year Published", "Number of Projects"]

    fig_trend = px.line(
        yearly_trends,
        x="Year Published",
        y="Number of Projects",
        title="Research Output Over the Years",
        markers=True,
    )
    fig_trend.update_traces(textposition="bottom right")
    fig_trend.update_layout(
        title=dict(x=0.5, xanchor="center", font=dict(size=22, family="Calibri Light", color="#2C3E50")),
        xaxis_title="Year",
        yaxis_title="Number of Research Projects",
        xaxis=dict(showgrid=True, gridcolor="LightGrey"),
        yaxis=dict(showgrid=True, gridcolor="LightGrey"),
        plot_bgcolor="white",
        hovermode="x unified",
    )

    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4.container(border=True,height="stretch"):
    # --- Step 1: Aggregate total projects per supervisor ---
    supervisor_total = projects_df.groupby("supervisor_id")["project_id"].count().reset_index()
    supervisor_total = supervisor_total.merge(supervisors_df[['supervisor_id', 'name']], on='supervisor_id')
    supervisor_total.rename(columns={"name": "Supervisor", "project_id": "Total Projects"}, inplace=True)

    # --- Step 2: Optional: Sort descending ---
    supervisor_total = supervisor_total.sort_values(by="Total Projects", ascending=False)

    # --- Step 3: Plot Bar Chart ---
    fig_supervisor_bar = px.bar(
        supervisor_total,
        x="Supervisor",
        y="Total Projects",
        text="Total Projects",
        title="Overall Supervisor Project Count",
        color="Total Projects",
        color_continuous_scale="Blues"
    )

    # --- Step 4: Styling ---
    fig_supervisor_bar.update_layout(
        height = 550,
        width = 550,
        title=dict(x=0.5, xanchor="center", font=dict(size=22, family="Calibri Light", color="#2C3E50")),
        xaxis_title="Supervisor",
        yaxis_title="Number of Projects",
        xaxis_tickangle=-90,
        plot_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="LightGrey"),
        hovermode="x unified"
    )

    fig_supervisor_bar.update_traces(textposition='outside')

    # --- Step 5: Display in Streamlit ---
    st.plotly_chart(fig_supervisor_bar, use_container_width=True)

with st.container(border=True,height="stretch"):
    # --- Step 1: Find Top 5 Supervisors by total projects ---
    top_supervisors = projects_df.groupby("supervisor_id")["project_id"].count().reset_index()
    top_supervisors = top_supervisors.sort_values(by="project_id", ascending=False).head(5)

    # Merge with supervisor names
    top_supervisors = top_supervisors.merge(supervisors_df[['supervisor_id', 'name']], on='supervisor_id')
    top_supervisor_ids = top_supervisors['supervisor_id'].tolist()

    # --- Step 2: Filter projects_df for top 5 supervisors ---
    top_projects = projects_df[projects_df['supervisor_id'].isin(top_supervisor_ids)]

    # --- Step 3: Aggregate yearly trends ---
    supervisor_yearly = top_projects.groupby(["supervisor_id", "year_published"])["project_id"].count().reset_index()
    supervisor_yearly = supervisor_yearly.merge(supervisors_df[['supervisor_id', 'name']], on='supervisor_id', how='left')
    supervisor_yearly.rename(columns={"name": "Supervisor", "project_id": "Number of Projects"}, inplace=True)

    # --- Step 4: Plot Line Chart ---
    fig_top_supervisors = px.line(
        supervisor_yearly,
        x="year_published",
        y="Number of Projects",
        color="Supervisor",
        markers=True,
        title="Top 5 Supervisor Publication Trends Over Time"
    )

    # Styling
    fig_top_supervisors.update_layout(
        title=dict(x=0.5, xanchor="center", font=dict(size=22, family="Calibri Light", color="#2C3E50")),
        xaxis_title="Year",
        yaxis_title="Number of Projects",
        xaxis=dict(showgrid=True, gridcolor="LightGrey"),
        yaxis=dict(showgrid=True, gridcolor="LightGrey"),
        plot_bgcolor="white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center",x=0.5,maxheight=0.1, title_text="Supervisors")
    )

    # --- Step 5: Display in Streamlit ---
    st.plotly_chart(fig_top_supervisors, use_container_width=True)


with st.container(border=True,height="stretch"):
    merged_df = projects_df.merge(students_df, on="student_id")
    cat_by_level = merged_df.groupby(["category", "program"]).size().reset_index(name="count")
    fig_cat_level = px.bar(
        cat_by_level,
        x="category",
        y="count",
        color="program",
        barmode="group",
        title="Top Research Areas by Student Level"
        )
    fig_cat_level.update_layout(
        showlegend=True,
        height = 600,
        width = 600,
        title=dict(
            text="Top Research Areas by Student Level",
            font=dict(size=22, family="Calibri Light", color="#2C3E50"),
            x=0.5,           # ✅ Centers the title horizontally
            xanchor="center", # Keeps it properly centered
            yanchor="top"
        ),
        xaxis=dict(side="bottom"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center",x=0.5,maxheight=0.1, title_text="program"),
        )
    st.plotly_chart(fig_cat_level, use_container_width=True)


# -------------------------------
## Download Button
# -------------------------------
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_research_projects.csv',
    mime='text/csv'
)
