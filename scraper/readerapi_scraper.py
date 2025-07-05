import time
import json
import os
import requests
import dotenv
from datetime import datetime

# Load environment variables from .env file
dotenv.load_dotenv()


def scrape_with_readerapi(target_url, api_key):
    """
    Scrape website content using JinaAI's ReaderAPI.
    
    Args:
        target_url (str): The URL of the webpage to scrape.
        api_key (str): Your JinaAI ReaderAPI key.
    
    Returns:
        tuple: A tuple containing the paths of the saved JSON and Markdown files.
    """
    print("🚀 Starting ReaderAPI scraper...")
    
    # Set up the Reader API endpoint with the target URL
    # The URL needs to be properly encoded to work with the ReaderAPI
    import urllib.parse
    encoded_url = urllib.parse.quote_plus(target_url)
    reader_url = f'https://r.jina.ai/{encoded_url}'
    
    # Set up the headers with your API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Set parameters to ensure complete content extraction
    params = {
        "wait": "5000",  # Wait for 5 seconds for the page to load fully
        "full": "true",  # Get the full content
        "type": "text",  # Get text content
        "autoExtract": "true"  # Auto-extract meaningful content
    }
    
    try:
        print(f"📄 Sending request to ReaderAPI for URL: {target_url}")
        print("⏳ Waiting for page to fully load (this may take a few seconds)...")
        response = requests.get(reader_url, headers=headers, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # First try to parse as JSON
                data = response.json()
                print("✅ Successfully received JSON data from ReaderAPI")
                
                # Extract content from JSON response
                title = data.get("title", "No Title")
                content = data.get("content", "No content extracted")
                metadata = data.get("metadata", {})
                
            except json.JSONDecodeError:
                # If not JSON, it's likely returning Markdown content directly
                print("📝 Received Markdown content from ReaderAPI")
                raw_content = response.text
                
                # Parse the raw markdown to extract structured data
                title = ""
                content = raw_content
                metadata = {}
                
                # Extract title if available (usually starts with "Title: ")
                title_match = raw_content.split("Title:", 1)
                if len(title_match) > 1:
                    title = title_match[1].split("\n", 1)[0].strip()
                else:
                    # Try alternative format (# or ## heading)
                    lines = raw_content.split("\n")
                    for line in lines:
                        if line.startswith("# ") or line.startswith("## "):
                            title = line.lstrip("# ").strip()
                            break
                    
                    if not title and len(lines) > 0:
                        title = lines[0].strip()  # Use first line as title
            
            # Get source domain from URL
            from urllib.parse import urlparse
            domain = urlparse(target_url).netloc
            
            # Clean up title for filename
            if not title:
                title = "Untitled_" + domain.replace(".", "_")
                
            # Create timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_title = "".join([c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in title])
            sanitized_title = sanitized_title.replace(" ", "_")[:50]  # Limit length
            
            # Create structured data for JSON
            extracted_data = {
                "url": target_url,
                "title": title,
                "source": domain,
                "content": content,
                "metadata": metadata,
                "extraction_date": timestamp
            }
            
            print(f"📄 Content extracted: Title: {title}, Source: {domain}")
            
            # Save as JSON
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-json')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'readerapi_{sanitized_title}_{timestamp}.json')
            output_file = os.path.abspath(output_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, ensure_ascii=False, indent=4)
            
            # Save as Markdown
            output_md_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scraped-data', 'raw-md')
            os.makedirs(output_md_dir, exist_ok=True)
            output_md_file = os.path.join(output_md_dir, f'readerapi_{sanitized_title}_{timestamp}.md')
            output_md_file = os.path.abspath(output_md_file)
            
            with open(output_md_file, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**Source:** {domain}\n")
                f.write(f"**URL:** {target_url}\n\n")
                f.write("## Content\n\n")
                f.write(content)
            
            print(f"✅ Content saved to {output_file} and {output_md_file}")
            return (output_file, output_md_file)
                
        else:
            print(f"❌ Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        return None


