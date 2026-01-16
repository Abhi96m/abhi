import requests
import yaml
import pandas as pd

# Paths to the YAML file and the Excel report
YAML_FILE_PATH = 'components.yaml'
EXCEL_REPORT_PATH = 'audit_report.xlsx'

# Load container images from YAML
def load_container_images():
    with open(YAML_FILE_PATH, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('containers', [])

# Save updated container images back to YAML
def save_container_images(containers):
    with open(YAML_FILE_PATH, 'w') as file:
        yaml.dump({'containers': containers}, file)

# Fetch components for a given container image
def fetch_components(container):
    components = []
    page = 1
    seen_components = set()
    component_api_url = 'https://example.com/api/components'
    
    while True:
        response = requests.get(component_api_url, params={'container_id': container['id'], 'page': page, 'limit': 1000})
        if response.status_code != 200:
            break
        
        data = response.json()
        if not data or 'components' not in data:
            break
        
        for component in data['components']:
            key = (component['name'], component['version'])
            if key not in seen_components:
                components.append(component)
                seen_components.add(key)
        
        if len(data['components']) < 1000:
            break  # No more pages
        
        page += 1
    
    return components

# Main function to generate the audit report
def generate_audit_report():
    containers = load_container_images()
    all_components = []
    
    for container in containers:
        components = fetch_components(container)
        for component in components:
            all_components.append({
                'container_name': container['name'],
                'component_name': component['name'],
                'component_version': component['version']
            })
    
    # Create a DataFrame and save to Excel
    df = pd.DataFrame(all_components)
    df.to_excel(EXCEL_REPORT_PATH, index=False)
    
    # Optionally, update the YAML file if needed
    save_container_images(containers)

if __name__ == '__main__':
    generate_audit_report()


containers:
  - id: "container_1"
    name: "my-app-image"
    organization: "my-org"
    repository: "my-repo"
    version: "1.0"
    app_id: "app-123"
    project_id: "proj-456"

  - id: "container_2"
    name: "another-app-image"
    organization: "another-org"
    repository: "another-repo"
    version: "2.1"
    app_id: "app-789"
    project_id: "proj-012"

# Add more container images as needed
