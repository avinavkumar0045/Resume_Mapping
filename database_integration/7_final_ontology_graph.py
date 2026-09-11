import os
import json
from neo4j import GraphDatabase

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_PASSWORD = "Avinav@45" # UPDATE THIS

NORMALIZED_DIR = "normalized"

def build_final_ontology():
    driver = GraphDatabase.driver(NEO4J_URI, auth=("neo4j", NEO4J_PASSWORD))
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith('.json')]
    
    with driver.session() as session:
        # Clear old graph
        session.run("MATCH (n) DETACH DELETE n")
        
        # ==========================================
        # 1. BUILD THE STRUCTURED SCHEMA (METADATA)
        # ==========================================
        session.run("""
            // Create Tables
            MERGE (t_emp:Table {name: 'Employee Dimension'})
            MERGE (t_comp:Table {name: 'Company Dimension'})
            MERGE (t_perf:Table {name: 'Performance'})
            
            // Connect Tables
            MERGE (t_emp)-[:CONNECTED_TO]->(t_comp)
            MERGE (t_emp)-[:CONNECTED_TO]->(t_perf)
            
            // Create Columns
            MERGE (c_emp_id:Column {name: 'Employee ID'})
            MERGE (c_emp_name:Column {name: 'Employee Name'})
            MERGE (c_perf_rating:Metric {name: 'Performance Rating'})
            
            // Connect Tables to Columns
            MERGE (t_emp)-[:HAS_COLUMN]->(c_emp_id)
            MERGE (t_emp)-[:HAS_COLUMN]->(c_emp_name)
            MERGE (t_perf)-[:HAS_METRIC]->(c_perf_rating)
        """)
        
        # ==========================================
        # 2. BUILD THE UNSTRUCTURED ENTITY CLASSES
        # ==========================================
        session.run("""
            MERGE (uc_name:EntityClass {name: 'Candidate Name'})
            MERGE (uc_skill:EntityClass {name: 'Skill'})
            MERGE (uc_edu:EntityClass {name: 'Education'})
            
            // THE BRIDGE: MAPPING STRUCTURED COLUMN TO UNSTRUCTURED ENTITY
            WITH uc_name
            MATCH (c:Column {name: 'Employee Name'})
            MERGE (c)-[:MAPPED_TO]->(uc_name)
        """)
        
        # ==========================================
        # 3. POPULATE THE ACTUAL UNSTRUCTURED VALUES
        # ==========================================
        for filename in sorted(files):
            with open(os.path.join(NORMALIZED_DIR, filename), "r") as f:
                data = json.load(f)
                
            name = data.get("person", {}).get("name", "Unknown")
            if not name or name == "null": name = "Unknown"
            
            # Create Actual Name Instance
            session.run("""
                MATCH (uc_name:EntityClass {name: 'Candidate Name'})
                MERGE (inst_name:Instance:Candidate {value: $name})
                MERGE (uc_name)-[:HAS_ACTUAL_VALUE]->(inst_name)
            """, name=name)
            
            # Create Actual Skill Instances
            for skill in data.get("skills", []):
                if skill.strip():
                    session.run("""
                        MATCH (uc_skill:EntityClass {name: 'Skill'})
                        MATCH (inst_name:Instance:Candidate {value: $name})
                        MERGE (inst_skill:Instance:Skill {value: $skill_name})
                        MERGE (uc_skill)-[:HAS_ACTUAL_VALUE]->(inst_skill)
                        MERGE (inst_name)-[:HAS_SKILL]->(inst_skill)
                    """, name=name, skill_name=skill.strip())
                    
    driver.close()
    print("✅ Successfully built the Semantic Data Fabric!")
    print("Run this query in Neo4j to see the exact structure your faculty requested:")
    print("MATCH (n) RETURN n")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEO4J_PASSWORD":
        print("⚠️ ERROR: Open database_integration/7_final_ontology_graph.py and set your Neo4j password!")
    else:
        build_final_ontology()
