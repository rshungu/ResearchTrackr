import pandas as pd
import random
from faker import Faker

fake = Faker()

# --- CONFIGURATION ---
num_supervisors = 100
num_students = 1000
categories = [
    "Blood Disorders", "Transfusion Medicine", "Hematologic Malignancies",
    "Sickle Cell Disease", "Clinical Hematology", "Laboratory Hematology",
    "Stem Cell Research", "Immunohematology"
]

# Example phrasing templates
templates = [
    "Molecular Mechanisms of {} in {} Patients",
    "Impact of {} Protocols on {} Outcomes",
    "Clinical Outcomes of {} in {}",
    "Evaluation of {} Techniques in {}",
    "Advances in {} for {} Management",
    "Correlation between {} and {} in {}",
    "Genetic Factors Influencing {} in {}",
    "Epidemiology of {} in {} Populations"
]

# Possible modifiers to add diversity
modifiers = ["Adult", "Pediatric", "Hospital", "Laboratory", "Community", "Experimental"]

# --- SUPERVISORS DATA ---
supervisors = []
for i in range(1, num_supervisors + 1):
    supervisors.append({
        "supervisor_id": i,
        "name": fake.name(),
        "title": random.choice(["Dr.", "Prof.", "Mr.", "Ms."]),
        "specialization": random.choice(categories)
    })

supervisors_df = pd.DataFrame(supervisors)

# --- STUDENTS DATA ---
students = []
for i in range(1, num_students + 1):
    students.append({
        "student_id": i,
        "name": fake.name(),
        "year_of_study": random.choice([2021, 2022, 2023, 2024]),
        "program": random.choice(["BMLS", "MD", "MSc Hematology"])
    })

students_df = pd.DataFrame(students)

# --- RESEARCH PROJECTS DATA ---
# Generate unique titles per category
category_topics = {}
for cat in categories:
    titles = set()
    while len(titles) < 20:  # 20 unique titles per category
        template = random.choice(templates)
        num_placeholders = template.count("{}")
        
        if num_placeholders == 2:
            mod1 = cat
            mod2 = random.choice(modifiers)
            title = template.format(mod1, mod2)
        elif num_placeholders == 3:
            mod1 = cat
            mod2 = random.choice(modifiers)
            mod3 = random.choice(modifiers)
            title = template.format(mod1, mod2, mod3)
        else:
            # fallback: just replace with category
            title = template.format(cat)
            
        titles.add(title)
    category_topics[cat] = list(titles)

# Flatten and shuffle
all_titles = []
for cat, topics in category_topics.items():
    for t in topics:
        all_titles.append({"title": t, "category": cat})
random.shuffle(all_titles)

# Assign titles to students uniquely
projects = []
for i in range(num_students):
    # To ensure we don't run out of titles, cycle through all_titles
    title_entry = all_titles[i % len(all_titles)]
    projects.append({
        "project_id": i + 1,
        "student_id": i + 1,
        "supervisor_id": random.randint(1, num_supervisors),
        "title": title_entry["title"],
        "category": title_entry["category"],
        "status": random.choice(["Ongoing", "Completed"]),
        "year_published": random.choice([2021, 2022, 2023, 2024]),
        "dataset_available": random.choice(["Yes", "No"])
    })

projects_df = pd.DataFrame(projects)

# --- SAVE FILES ---
supervisors_path = r"C:\Users\Dell\Desktop\Work\Personal\Projects\1. ResearchTrackr\supervisors.csv"
students_path = r"C:\Users\Dell\Desktop\Work\Personal\Projects\1. ResearchTrackr\students.csv"
projects_path = r"C:\Users\Dell\Desktop\Work\Personal\Projects\1. ResearchTrackr\research_projects.csv"

supervisors_df.to_csv(supervisors_path, index=False)
students_df.to_csv(students_path, index=False)
projects_df.to_csv(projects_path, index=False)

print("Data simulation completed successfully!")
