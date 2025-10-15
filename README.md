# ResearchTrackr

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue)]()
[![ETL](https://img.shields.io/badge/ETL-Pipelines-yellow)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

ResearchTrackr is a web-based application built with Streamlit to help students and academic staff explore past research projects across departments.It enables users to avoid topic duplication, discover research trends, and identify active supervisors, supporting transparency and informed academic planning.

## Key Features
1.  Search & Filter
     - Search research titles by keyword or filter by category to check if a topic has already been explored
     - Users can search research titles by keyword or filter by category to check if a topic has already been explored.
     - The tool helps students avoid proposing duplicate research topics.
     - Supports multiple filters (e.g., department, year, or supervisor) for deeper exploration.
     - Designed to encourage collaborative and informed topic selection

2. Interactive Visualizations by exploring visual insights such as:
     - Number of research papers per category to understand which fields or departments are most active in research.
     - Supervisors with the most students by identifying highly active supervisors or research mentors.
  
3. Dynamic Data Updates
     - Automatically updates with new research data to ensure accuracy, freshness, and reliability.
     - Can be integrated with live databases or CSV uploads for automated synchronization.
     - Helps maintain long-term usability as research data grows over time.
       
5. Clean and Reusable Codebase
      - Developed with scalability and maintainability in mind, allowing easy adaptation for new datasets or institution
      - Modular structure using separate Python scripts for data cleaning, visualization, and utilities.
      - Easily adaptable for new datasets, departments, or institutions.
      - Follows clean coding principles and reusable function design for collaboration and extension
        
> Example Use Cases:
> 
>   a. Students: Check if their proposed research topic has been done before
> 
>   b. Supervisors: Track their supervision record and research trends

# Teck Stack 

| Category                      | Tools & Libraries                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| **Frontend**                  | Streamlit                                                                            |
| **Backend / Logic**           | Python                                                                               |
| **Data Processing**           | Pandas                                                                               |
| **Data Visualization**        | Plotly                                                                               |
| **Database**                  | PostgreSQL, MySQL                                                                    |
| **Additional Skills Applied** | Data Cleaning, Web Scraping, SQL Database Design, Data Analytics, Project Management |

# Installation and Setup
To run the app locally
```
# Clone the repository
git clone https://github.com/<your-username>/ResearchTrackr.git

# Navigate into the project folder
cd ResearchTrackr

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```
# Folder Structure
```
ResearchTrackr/
│
├── app.py                     # Main Streamlit application
├── data/
│   ├── research_projects.csv   # Sample dataset
│   └── supervisors.csv
|   └── students.csv
|   └── researchtrackr_logo.py
│   └── data_simulation.py             
│   └── Creating Tables and Data Importing.sql       # Data cleaning and helper functions
├── requirements.txt
└── README.md
```
## Future Enhancements
1. Add user authentication for personalized dashboards
2. Integrate predictive models for emerging research topic trends
3. Enable data upload for multiple institutions

## Contributions
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to create a pull request or open an issue
