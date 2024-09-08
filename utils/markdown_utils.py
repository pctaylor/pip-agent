import mistune
from bs4 import BeautifulSoup
import os
import logging

def clean_markdown(markdown_text):
    try:
        # Use Mistune to convert markdown to HTML
        markdown = mistune.create_markdown(escape=True, hard_wrap=True)
        html = markdown(markdown_text)
        
        # Use BeautifulSoup to add classes and make further modifications
        soup = BeautifulSoup(html, 'html.parser')
        
        # Add classes to elements for styling
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            tag['class'] = tag.name + '-style'
        
        for p in soup.find_all('p'):
            p['class'] = 'paragraph-style'
        
        for ul in soup.find_all('ul'):
            ul['class'] = 'unordered-list-style'
        
        for ol in soup.find_all('ol'):
            ol['class'] = 'ordered-list-style'
        
        for blockquote in soup.find_all('blockquote'):
            blockquote['class'] = 'blockquote-style'
        
        for table in soup.find_all('table'):
            table['class'] = 'table-style'
        
        # Convert back to HTML
        cleaned_html = str(soup)
        
        return cleaned_html
    except Exception as e:
        logging.error(f"Error in clean_markdown: {str(e)}", exc_info=True)
        return f"<p>Error processing markdown: {str(e)}</p>"

# Test the clean_markdown function with the contents of test.md
def test_clean_markdown():
    try:
        print("Current working directory:", os.getcwd())  # Print current working directory
        with open('test.md', 'r') as file:
            md_content = file.read()
        
        cleaned_html = clean_markdown(md_content)
        print("Cleaned HTML output:")
        print(cleaned_html)
    except FileNotFoundError:
        print("Error: test.md file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Call the test function
if __name__ == "__main__":
    test_clean_markdown()
