import os
import json
import requests
import re

EXTRACTED_DIR = "extracted"
NORMALIZED_DIR = "normalized"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder" # Adjust if your model name is different

PROMPT_TEMPLATE = """You are an expert data extractor. Extract the information from the resume text below into a strict JSON object matching this exact structure:
{
  "person": {
    "name": "string or null",
    "email": "string or null",
    "phone": "string or null",
    "location": "string or null",
    "linkedin": "string or null",
    "github": "string or null",
    "portfolio": "string or null"
  },
  "summary": "string or null",
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "field": "string",
      "start_date": "string or null",
      "end_date": "string or null"
    }
  ],
  "experience": [
    {
      "company": "string",
      "role": "string",
      "description": "string"
    }
  ],
  "skills": ["string"],
  "projects": [],
  "certifications": [],
  "images": []
}

Rules:
1. Ensure the output is ONLY valid JSON. No markdown, no explanations.
2. For the "images" array, if you see any text like [IMAGE EXTRACTED: filename.png], extract it and format it as {"path": "extracted_images/filename.png", "context": "header"} in the JSON.
3. Be as accurate as possible extracting companies, roles, and schools.

Resume Text:
"""

def normalize_with_llm(text):
    prompt = PROMPT_TEMPLATE + text
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"  # Forces Ollama to output valid JSON
    }
    
    try:
        # Increased timeout to 120 seconds to prevent the error you saw!
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        result_text = response.json().get('response', '')
        # Clean up any potential markdown formatting
        result_text = result_text.replace('```json', '').replace('```', '').strip()
        
        return json.loads(result_text)
    except Exception as e:
        print(f"LLM extraction error: {e}")
        return None

def run_normalization():
    os.makedirs(NORMALIZED_DIR, exist_ok=True)
    files = [f for f in os.listdir(EXTRACTED_DIR) if f.endswith('.txt')]
    
    print(f"Found {len(files)} files to normalize with Qwen...")
    
    for filename in sorted(files):
        in_filepath = os.path.join(EXTRACTED_DIR, filename)
        out_filename = filename.replace('.txt', '.json')
        out_filepath = os.path.join(NORMALIZED_DIR, out_filename)
        
        print(f"Processing {filename} with Qwen LLM...")
        with open(in_filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        json_blueprint = normalize_with_llm(raw_text)
        
        if json_blueprint:
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                json.dump(json_blueprint, out_f, indent=4)
            print(f"✅ Successfully normalized: {out_filename}")
        else:
            print(f"❌ Failed to parse JSON for {filename}")

if __name__ == "__main__":
    run_normalization()
