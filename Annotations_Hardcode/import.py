import requests
import os
import zipfile

# --- CONFIGURATION ---
LABEL_STUDIO_URL = "http://localhost:8080"
API_KEY = "5cdbea5c36ba7e3bacf6a6185795ba259478c3c5" 
PROJECT_TITLE = "Cats and Dogs"  
EXPORT_FORMAT = "YOLO"            
OUTPUT_DIR = "Exports"             

# --- HEADERS ---
headers = {
    "Authorization": f"Token {API_KEY}"
}

# --- STEP 1: Find project by title ---
def get_project_id_by_title(title):
    try:
        response = requests.get(f"{LABEL_STUDIO_URL}/api/projects", headers=headers)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict) and "results" in data:
            data = data["results"]

        for project in data:
            if project.get("title") == title:
                return project["id"]

        print(f"Project '{title}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        return None

# --- STEP 2: Export + Extract ---
def export_annotations(project_id):
    print(f"\nExporting project ID {project_id} in YOLO format...")

    export_url = f"{LABEL_STUDIO_URL}/api/projects/{project_id}/export?exportType={EXPORT_FORMAT}"
    try:
        response = requests.get(export_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to trigger export: {e}")
        return

    try:
        result = response.json()
        download_url = result.get("url")
        if not download_url:
            print("Export response missing download URL.")
            return
    except ValueError:
        print("Failed to decode export JSON response.")
        print(response.text)
        return

    try:
        # --- Download the zip ---
        zip_response = requests.get(f"{LABEL_STUDIO_URL}{download_url}", headers=headers)
        zip_response.raise_for_status()

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        zip_filename = f"{PROJECT_TITLE.replace(' ', '_')}.{EXPORT_FORMAT.lower()}.zip"
        zip_path = os.path.join(OUTPUT_DIR, zip_filename)

        with open(zip_path, "wb") as f:
            f.write(zip_response.content)

        print(f"Exported ZIP saved to: {zip_path}")

        # --- Extract the zip ---
        extract_dir = os.path.join(OUTPUT_DIR, f"{PROJECT_TITLE.replace(' ', '_')}_{EXPORT_FORMAT.lower()}")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        print(f"Extracted contents to: {extract_dir}")

    except Exception as e:
        print(f"Failed to download or extract: {e}")

# --- MAIN ---
if __name__ == "__main__":
    project_id = get_project_id_by_title(PROJECT_TITLE)
    if project_id:
        export_annotations(project_id)
