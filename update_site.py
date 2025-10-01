import os, yaml

def update_resources(config_path="config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    resources_dir = config.get("resources_dir", "data/resources")
    output_file = config.get("resources_output", "resources.html")

    resources = os.listdir(resources_dir)
    resources_html = "<ul>" + "".join([f'<li><a href="{resources_dir}/{r}">{r}</a></li>' for r in resources]) + "</ul>"

    with open(output_file, "r") as f:
        content = f.read()

    new_content = content.replace("<p>All PDFs, screenshots, and images will be listed here automatically.</p>", resources_html)

    with open(output_file, "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_resources()
