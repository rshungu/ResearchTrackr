# **ResearchTrackr**
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/streamlit-1.x-red.svg)]()


## Overview
ResearchTrackr is a Streamlit-based web application designed to track student research papers, supervisors, and publication statuses using PostgreSQL as the database backend. The app provides an intuitive interface for filtering
research data, visualizing key metrics, and analyzing supervisor contributions.

### Features

1. Search & Filters:
     - Search research by title or student number
     - Filter by university level, degree program, research category, supervisor, publication 
       status, dataset availability, and date range.

2. Dashboard Metrics:
     - Total research papers, published and unpublished papers, total students, and supervisors        with the most students/publications.

3. Visualizations:
    - Research distribution by category, degree program, and lead supervisor.
    - Bar charts showing research and publication trends over the years.
    - Supervisor leaderboard based on student supervision count.

4. Expandable Research Table:
    - Displays full research details with dynamic filtering.

## Database Schema


## Installation Steps

1. **Clone the repository**:
   First, clone the repository to your local machine.
   ```bash
   git clone https://github.com/your-username/ResearchTrackr.git
   cd ResearchTrackr
2. Install dependencies: Install the necessary Python libraries using pip:
    ```bash
    pip install -r requirements.txt
3. Set up PostgreSQL and Ensure PostgreSQL is running
4. Update the DATABASE_URL in the Streamlit app:
   ```bash
   DATABASE_URL = "postgresql://your_username:your_password@localhost:5432/research_publications```
6. Run the Streamlit app:
   ```bash
   streamlit run app.py
