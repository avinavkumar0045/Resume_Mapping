from neo4j import GraphDatabase

# IMPORTANT: Update with your password!
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Avinav@45"

def build_ontology_graph():
    print("Connecting to Neo4j to build the Enterprise Data Fabric Ontology...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        # Clear previous ontology if you want a fresh start (optional, commented out)
        # session.run("MATCH (n:DataStore) DETACH DELETE n")
        
        # 1. Create the MySQL Employee Table Node (Generalised)
        session.run("""
            MERGE (empTable:DataStore {type: 'Relational_Table', name: 'MySQL_Employee'})
            SET empTable.columns = 'emp_id, name, address, salary, company_id, resume_file, work_score'
        """)
        
        # 2. Create the MySQL Company Table Node (Generalised)
        session.run("""
            MERGE (compTable:DataStore {type: 'Relational_Table', name: 'MySQL_Company'})
            SET compTable.columns = 'company_id, company_name, city, address, revenue'
        """)
        
        # 3. Create the ChromaDB Unstructured Data Node
        session.run("""
            MERGE (chromaStore:DataStore {type: 'Vector_DB', name: 'ChromaDB_Resumes'})
            SET chromaStore.description = 'Holds extracted resume embeddings and unstructured text'
        """)
        
        # 4. Connect the Structured Data together (Employee -> Company)
        session.run("""
            MATCH (e:DataStore {name: 'MySQL_Employee'}), (c:DataStore {name: 'MySQL_Company'})
            MERGE (e)-[:FOREIGN_KEY_RELATION {key: 'company_id'}]->(c)
        """)
        
        # 5. Connect the Structured Data to the Unstructured Data! (Employee -> ChromaDB)
        session.run("""
            MATCH (e:DataStore {name: 'MySQL_Employee'}), (v:DataStore {name: 'ChromaDB_Resumes'})
            MERGE (e)-[:HAS_UNSTRUCTURED_DATA {link_key: 'resume_file'}]->(v)
        """)
        
    driver.close()
    print("✅ Ontology Graph built successfully in Neo4j!")
    print("Run `MATCH (n:DataStore) RETURN n` in Neo4j to see your data fabric!")

if __name__ == "__main__":
    if NEO4J_PASSWORD == "YOUR_NEW_PASSWORD_HERE":
        print("⚠️ ERROR: Please open database_integration/2_setup_ontology_graph.py and set your Neo4j password!")
    else:
        try:
            build_ontology_graph()
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
