import os
import json
import chromadb
from neo4j import GraphDatabase

# --- CONFIGURATION ---
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Avinav@45"  

BLUEPRINTS_DIR = "blueprints"

def load_to_chroma(blueprints):
    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="resume_sections")
    
    docs = []
    metadatas = []
    ids = []
    
    for bp in blueprints:
        file_path = bp["file_path"]
        for sec_name, sec_data in bp.get("Sections", {}).items():
            text = sec_data.get("Text", "")
            if text:
                docs.append(text)
                metadatas.append({"file_path": file_path, "section": sec_name})
                ids.append(f"{os.path.basename(file_path)}_{sec_name}")
                
    if docs:
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
    print(f"✅ Successfully loaded {len(docs)} text chunks into ChromaDB Vector Store!")

def load_to_neo4j(blueprints):
    print("Connecting to Neo4j Knowledge Graph...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        for bp in blueprints:
            file_path = bp["file_path"]
            name = bp.get("metadata", {}).get("name", "Unknown")
            
            # Create Resume node
            session.run("""
                MERGE (r:Resume {file_path: $file_path})
                SET r.candidate_name = $name
            """, file_path=file_path, name=name)
            
            # Create Section nodes and connect them
            for sec_name, sec_data in bp.get("Sections", {}).items():
                text = sec_data.get("Text", "")
                if text:
                    session.run("""
                        MATCH (r:Resume {file_path: $file_path})
                        MERGE (s:Section {type: $sec_name, resume_file: $file_path})
                        SET s.text = $text
                        MERGE (r)-[:HAS_SECTION]->(s)
                    """, file_path=file_path, sec_name=sec_name, text=text)
    driver.close()
    print("✅ Successfully built the Knowledge Graph in Neo4j!")

if __name__ == "__main__":
    blueprints = []
    if not os.path.exists(BLUEPRINTS_DIR):
        print("No blueprints folder found!")
        exit(1)
        
    for filename in os.listdir(BLUEPRINTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(BLUEPRINTS_DIR, filename), "r") as f:
                blueprints.append(json.load(f))
                
    print(f"Loaded {len(blueprints)} JSON blueprints.")
    
    # 1. Load to ChromaDB (Local, no password needed)
    load_to_chroma(blueprints)
    
    # 2. Load to Neo4j
    if NEO4J_PASSWORD == "YOUR_NEW_PASSWORD_HERE":
        print("\n⚠️ NEO4J SKIPPED: You must edit load_to_dbs.py and put your actual Neo4j password at the top!")
    else:
        try:
            load_to_neo4j(blueprints)
        except Exception as e:
            print(f"\n❌ Failed to connect to Neo4j. Is the server running? Is the password correct? Error: {e}")
