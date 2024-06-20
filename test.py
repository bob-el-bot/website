import os
import json
from datetime import datetime

# Directory containing the blog posts
BLOGS_DIR = 'assets/blogs/'

# Function to generate blog card HTML
def generate_blog_card(metadata):
    title = metadata["title"]
    description = metadata["description"]
    date_of_publication = datetime.fromisoformat(metadata["date_of_publication"]).strftime('%Y-%m-%d')
    html_name = metadata.get("html_name", "page")  # Default to 'page.html' if not specified
    blog_path = f"./blogs/{os.path.basename(BLOGS_DIR)}/{html_name}.html"
    
    blog_card_html = f'''
    <div class="blog-card" onclick="window.location.href='{blog_path}'">
        <h2>{title}</h2>
        <p>{description}</p>
        <p class="publication-date"><span>{date_of_publication}</span></p>
    </div>
    '''
    return blog_card_html

# Main script
if __name__ == '__main__':
    blog_cards_html = ''
    
    # Iterate through the directories in the BLOGS_DIR
    for blog_dir in os.listdir(BLOGS_DIR):
        blog_dir_path = os.path.join(BLOGS_DIR, blog_dir)
        if os.path.isdir(blog_dir_path):
            metadata_file = os.path.join(blog_dir_path, 'details.json')
            if os.path.exists(metadata_file):
                print(f"Processing {metadata_file}")
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    try:
                        metadata = json.load(f)
                        blog_cards_html += generate_blog_card(metadata)
                    except json.JSONDecodeError as e:
                        print(f"Error reading JSON file {metadata_file}: {e}")
            else:
                print(f"Metadata file not found: {metadata_file}")
        else:
            print(f"Not a directory: {blog_dir_path}")
    
    # Read the current blog.html content
    with open('blog.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find the start and end markers for blog-stream
    start_marker = '<div class="blog-stream">'
    end_marker = '</div>'
    
    # Locate the position of blog-stream in the HTML content
    start_pos = html_content.find(start_marker)
    end_pos = html_content.find(end_marker, start_pos + len(start_marker)) if start_pos != -1 else -1
    
    if start_pos != -1 and end_pos != -1:
        # Remove existing blog cards between start and end markers
        updated_html_content = (
            html_content[:start_pos + len(start_marker)]
            + blog_cards_html
            + html_content[end_pos:]
        )
        
        # Print the updated HTML content for debugging
        print("Updated HTML Content:")
        print(updated_html_content)
        
        # Save the updated HTML content back to the file
        with open('blog.html', 'w', encoding='utf-8') as f:
            f.write(updated_html_content)

        print("Blog cards have been updated successfully.")
    else:
        print("Error: Could not find start or end marker in blog.html. Content not updated.")
