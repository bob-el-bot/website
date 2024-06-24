import os
import sys
import json
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from datetime import datetime

CONFIG_FILE = 'config.json'

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def save_config(config, config_file):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)

def generate_sitemap(directory, base_url, verbose=False):
    config = load_config(CONFIG_FILE)
    
    urlset = ET.Element(
        "urlset", 
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
        attrib={
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.sitemaps.org/schemas/sitemap/0.9 "
                                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
        }
    )
    priorities = config.get("priorities", {})
    default_changefreq = config.get("changefreq", None)
    specific_pages = config.get("specific_pages", {})

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.htm')):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, directory).replace(os.sep, '/')
                url = urljoin(base_url, rel_path)
                
                url_element = ET.Element("url")
                loc = ET.SubElement(url_element, "loc")
                loc.text = url

                lastmod = ET.SubElement(url_element, "lastmod")
                lastmod.text = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d')

                if default_changefreq:
                    changefreq_elem = ET.SubElement(url_element, "changefreq")
                    changefreq_elem.text = default_changefreq
                
                priority_elem = ET.SubElement(url_element, "priority")
                if rel_path in specific_pages:
                    priority_elem.text = specific_pages[rel_path]
                elif file == 'index.html':
                    priority_elem.text = '1.0'
                else:
                    priority = '0.5'  # default priority
                    max_len = 0
                    for path, prio in priorities.items():
                        if rel_path.startswith(path.lstrip('/')) and len(path) > max_len:
                            priority = prio
                            max_len = len(path)
                    priority_elem.text = priority

                urlset.append(url_element)
                
                if verbose:
                    print(f"Added {url} with priority {priority_elem.text} (matched path: {rel_path})")

    tree = ET.ElementTree(urlset)
    tree.write("sitemap.xml", xml_declaration=True, encoding='utf-8', method="xml")
    print("Sitemap generated successfully.")

def view_config(config_file):
    config = load_config(config_file)
    print(json.dumps(config, indent=4))

def add_priority(path, priority, config_file):
    config = load_config(config_file)
    config['priorities'][path] = priority
    save_config(config, config_file)
    print(f"Added priority {priority} for path {path}.")

def delete_priority(path_index, config_file):
    config = load_config(config_file)
    priorities = config['priorities']
    if path_index >= 0 and path_index < len(priorities):
        path = list(priorities.keys())[path_index]
        del priorities[path]
        save_config(config, config_file)
        print(f"Deleted priority for path '{path}'.")
    else:
        print("Invalid path index.")

def edit_changefreq(changefreq, config_file):
    config = load_config(config_file)
    config['changefreq'] = changefreq
    save_config(config, config_file)
    print(f"Set changefreq to {changefreq}.")

def add_specific_page(path, priority, config_file):
    config = load_config(config_file)
    if 'specific_pages' not in config:
        config['specific_pages'] = {}
    config['specific_pages'][path] = priority
    save_config(config, config_file)
    print(f"Added specific priority {priority} for page {path}.")

def delete_specific_page(path_index, config_file):
    config = load_config(config_file)
    specific_pages = config.get('specific_pages', {})
    if path_index >= 0 and path_index < len(specific_pages):
        path = list(specific_pages.keys())[path_index]
        del specific_pages[path]
        save_config(config, config_file)
        print(f"Deleted specific page priority for path '{path}'.")
    else:
        print("Invalid path index or no specific page priorities.")

def list_settings(config_file):
    config = load_config(config_file)
    print("Current settings:")
    print(f"Priorities: {config['priorities']}")
    print(f"Change Frequency: {config['changefreq']}")
    print(f"Specific Page Priorities: {config['specific_pages']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: sitemap_tool.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'generate':
        if len(sys.argv) < 4:
            print("Usage: sitemap.py generate -d <directory> -u <base_url> [-v]")
            sys.exit(1)

        directory_index = sys.argv.index('-d') if '-d' in sys.argv else sys.argv.index('--directory')
        base_url_index = sys.argv.index('-u') if '-u' in sys.argv else sys.argv.index('--url')

        directory = sys.argv[directory_index + 1]
        base_url = sys.argv[base_url_index + 1]

        verbose = '-v' in sys.argv or '--verbose' in sys.argv

        try:
            generate_sitemap(directory, base_url, verbose)
        except FileNotFoundError:
            print(f"Configuration file {CONFIG_FILE} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif command == 'view-config':
        view_config(CONFIG_FILE)

    elif command == 'set-priority':
        if len(sys.argv) != 4:
            print("Usage: sitemap.py set-priority <path> <priority>")
            sys.exit(1)
        path = sys.argv[2]
        priority = sys.argv[3]
        add_priority(path, priority, CONFIG_FILE)

    elif command == 'delete-priority':
        config = load_config(CONFIG_FILE)
        priorities = config['priorities']
        print("Current priorities:")
        for i, path in enumerate(priorities.keys()):
            print(f"{i}: {path}")
        if len(priorities) > 0:
            path_index = int(input(f"Enter the number corresponding to the path to delete (0-{len(priorities)-1}): "))
            delete_priority(path_index, CONFIG_FILE)
        else:
            print("No priorities to delete.")

    elif command == 'set-changefreq':
        if len(sys.argv) != 3:
            print("Usage: sitemap.py set-changefreq <changefreq>")
            sys.exit(1)
        changefreq = sys.argv[2]
        edit_changefreq(changefreq, CONFIG_FILE)

    elif command == 'set-specific-priority':
        if len(sys.argv) != 4:
            print("Usage: sitemap.py set-specific-priority <path> <priority>")
            sys.exit(1)
        path = sys.argv[2]
        priority = sys.argv[3]
        add_specific_page(path, priority, CONFIG_FILE)

    elif command == 'delete-specific-priority':
        config = load_config(CONFIG_FILE)
        specific_pages = config.get('specific_pages', {})
        print("Current specific page priorities:")
        for i, path in enumerate(specific_pages.keys()):
            print(f"{i}: {path}")
        if len(specific_pages) > 0:
            path_index = int(input(f"Enter the number corresponding to the specific page path to delete (0-{len(specific_pages)-1}): "))
            delete_specific_page(path_index, CONFIG_FILE)
        else:
            print("No specific page priorities to delete.")

    elif command == 'list-settings':
        list_settings(CONFIG_FILE)

    else:
        print("Invalid command. Use 'sitemap.py --help' for usage.")

if __name__ == "__main__":
    main()
