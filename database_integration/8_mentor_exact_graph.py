import os
import json
from neo4j import GraphDatabase

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_PASSWORD = "Avinav@45" # UPDATE THIS

NORMALIZED_DIR = "normalized"

def build_mentor_exact_graph():
    driver = GraphDatabase.driver(NEO4J_URI, auth=("neo4j", NEO4J_PASSWORD))
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    with driver.session() as session:
        # Clear old graph
        session.run("MATCH (n) DETACH DELETE n")
        
        # 1. Create the Schema / Metadata Nodes exactly as seen in the screenshot
        session.run("""
            // MySQL Tables (Yellow nodes in screenshot)
            MERGE (tbl_emp:MySQLTable {name: 'employees'})
            MERGE (tbl_comp:MySQLTable {name: 'companies'})
            MERGE (tbl_perf:MySQLTable {name: 'employee_ratings'})
            
            // Entities / Properties (Orange nodes in screenshot)
            MERGE (ent_emp:Entity {name: 'Employee'})
            MERGE (ent_comp:Entity {name: 'Company'})
            MERGE (ent_rating:Entity {name: 'Rating', description: 'calculated rating stored in MySQL employee_ratings'})
        """)
        
        # 2. Iterate through each person to build their specific web
        for i, filename in enumerate(sorted(files)):
            with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
                data = json.load(f)
                
            emp_id = f"EMP{i+1:03d}"
            
            # The original PDF filename (Unstructured Data)
            pdf_filename = filename.replace('.json', '.pdf')
            
            session.run("""
                // A. Create the Unstructured Source Document (Green node in screenshot)
                MERGE (doc:SourceDocument {file_name: $pdf_filename})
                
                // B. Create the Structured Record (Pink node in screenshot like EMP001)
                MERGE (emp_rec:StructuredRecord {name: $emp_id})
                
                // C. Bridge Unstructured -> Structured exactly like the screenshot
                MERGE (doc)-[:SOURCE_FOR]->(emp_rec)
                
                // D. Connect Structured Record to the MySQL Table
                WITH emp_rec
                MATCH (tbl_emp:MySQLTable {name: 'employees'})
                MERGE (emp_rec)-[:STORED_IN]->(tbl_emp)
                
                // E. Connect Structured Record to Entities (INSTANCE_OF, WORKS_FOR, HAS_RATING)
                WITH emp_rec
                MATCH (ent_emp:Entity {name: 'Employee'})
                MATCH (ent_comp:Entity {name: 'Company'})
                MATCH (ent_rating:Entity {name: 'Rating'})
                
                MERGE (emp_rec)-[:INSTANCE_OF]->(ent_emp)
                MERGE (emp_rec)-[:WORKS_FOR]->(ent_comp)
                MERGE (emp_rec)-[:HAS_RATING]->(ent_rating)
                
            """, pdf_filename=pdf_filename, emp_id=emp_id)
            
            # Optional: Map the actual skills from the blueprint directly to the Source Document
            for skill in data.get("skills", []):
                if skill.strip():
                    session.run("""
                        MATCH (doc:SourceDocument {file_name: $pdf_filename})
                        MERGE (s:Entity:Skill {name: $skill_name})
                        MERGE (doc)-[:HAS_PROPERTY]->(s)
                    """, pdf_filename=pdf_filename, skill_name=skill.strip())
                    
    driver.close()
    print("✅ Successfully built the EXACT graph from your mentor's screenshot!")
    print("Run this query in Neo4j to see it exactly like the picture:")
    print("MATCH path = (source:SourceDocument)-[]->(record:StructuredRecord) RETURN path")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEO4J_PASSWORD":
        print("⚠️ ERROR: Open database_integration/8_mentor_exact_graph.py and set your Neo4j password!")
    else:
        build_mentor_exact_graph()
