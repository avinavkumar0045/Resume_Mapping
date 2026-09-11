import os
import json
import random

NORMALIZED_DIR = "normalized"
SQL_OUTPUT_FILE = "database_integration/mentor_structured_data.sql"

def generate_sql():
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    sql_commands = [
        "DROP DATABASE IF EXISTS MentorDB;",
        "CREATE DATABASE MentorDB;",
        "USE MentorDB;",
        "",
        "CREATE TABLE Employee (",
        "    employee_id VARCHAR(10) PRIMARY KEY,",
        "    name VARCHAR(255),",
        "    role VARCHAR(255),",
        "    salary DECIMAL(10, 2)",
        ");",
        "",
        "CREATE TABLE Performance (",
        "    perf_id INT AUTO_INCREMENT PRIMARY KEY,",
        "    employee_id VARCHAR(10),",
        "    name VARCHAR(255),",
        "    year INT,",
        "    summary TEXT,",
        "    score INT,",
        "    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)",
        ");",
        ""
    ]
    
    emp_inserts = []
    perf_inserts = []
    
    roles = ["Data Engineer", "Frontend Developer", "Product Manager", "Registered Nurse", "Financial Analyst"]
    
    for i, filename in enumerate(sorted(files)):
        with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
            data = json.load(f)
            
        name = data.get("person", {}).get("name", f"Emp_{i}")
        if not name or name == "null": name = f"Emp_{i}"
        name = name.replace("'", "''")
        
        emp_id = f"E{i+1:03d}"
        role = random.choice(roles)
        salary = random.randint(60000, 150000)
        
        emp_inserts.append(f"('{emp_id}', '{name}', '{role}', {salary})")
        
        # Get the actual unstructured summary from the resume to put in the structured DB!
        unstructured_summary = data.get("summary", "")
        if not unstructured_summary or unstructured_summary == "null":
            unstructured_summary = "No unstructured summary available."
        
        # Clean the summary for SQL insertion
        clean_summary = unstructured_summary.replace("'", "''")
        # Truncate if it's too long just to be safe in the SQL statement
        clean_summary = clean_summary[:500] + "..." if len(clean_summary) > 500 else clean_summary
        
        score = random.randint(7, 10)
        year = 2024
        
        perf_inserts.append(f"('{emp_id}', '{name}', {year}, '{clean_summary}', {score})")
            
    sql_commands.append("INSERT INTO Employee (employee_id, name, role, salary) VALUES")
    sql_commands.append(",\n".join(emp_inserts) + ";\n")
    
    sql_commands.append("INSERT INTO Performance (employee_id, name, year, summary, score) VALUES")
    sql_commands.append(",\n".join(perf_inserts) + ";\n")
    
    with open(SQL_OUTPUT_FILE, "w") as f:
        f.write("\n".join(sql_commands))
        
    print(f"✅ Generated {SQL_OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sql()
