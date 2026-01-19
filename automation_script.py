import os
import requests
import yaml
import pandas as pd
from pathlib import Path

YAML_FILE_PATH = "components.yaml"
EXCEL_REPORT_PATH = "audit_report.xlsx"

FIRST_API_URL = os.getenv("FIRST_API_URL")  # must return container image list
SECOND_API_URL = os.getenv("SECOND_API_URL")  # must return component list by container id

def get_auth_headers():
    token = os.getenv("CI_JOB_TOKEN")
    if not token:
        raise RuntimeError("CI_JOB_TOKEN not found in environment")
    return {
        "JOB-TOKEN": token,
        "PRIVATE-TOKEN": token
    }

def fetch_and_write_yaml():
    headers = get_auth_headers()
    resp = requests.get(FIRST_API_URL, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    with open(YAML_FILE_PATH, "w") as f:
        yaml.safe_dump({"containers": data.get("containers", [])}, f)

def load_yaml():
    if not Path(YAML_FILE_PATH).exists():
        fetch_and_write_yaml()
    with open(YAML_FILE_PATH, "r") as f:
        return yaml.safe_load(f) or {}

def fetch_components(container):
    headers = get_auth_headers()
    final = []
    seen = set()
    page = 1

    while True:
        resp = requests.get(
            SECOND_API_URL,
            headers=headers,
            params={"container_id": container["id"], "page": page, "limit": 1000}
        )
        if resp.status_code != 200:
            break

        data = resp.json()
        components = data.get("components", [])
        if not components:
            break

        for c in components:
            key = (c["name"], c["version"])
            if key not in seen:
                seen.add(key)
                final.append(c)

        if len(components) < 1000:
            break

        page += 1

    return final

def generate_excel():
    data = load_yaml()
    containers = data.get("containers", [])
    rows = []

    for c in containers:
        comps = fetch_components(c)
        for comp in comps:
            rows.append({
                "project_id": c.get("project_id"),
                "app_id": c.get("app_id"),
                "container_name": c.get("name"),
                "container_version": c.get("version"),
                "component_name": comp["name"],
                "component_version": comp["version"]
            })

    df = pd.DataFrame(rows)
    df.to_excel(EXCEL_REPORT_PATH, index=False)

if __name__ == "__main__":
    fetch_and_write_yaml()
    generate_excel()
