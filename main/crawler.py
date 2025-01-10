import requests
from bs4 import BeautifulSoup

def extract_table_data(table):
    rows = table.find_all("tr")[1:]  # Skip the header row
    markdown = []
    markdown.append("| Paper | Author(s) | Description | Source | Date |")
    markdown.append("| --- | --- | --- | --- | --- |")
    
    for row in rows:
        cols = row.find_all("td")
        
        # Extract Paper name
        paper_tag = cols[1].find("a", href=True)
        paper_name = paper_tag.get_text(strip=True) if paper_tag else ""
        
        # Extract Authors
        author_col = cols[2]
        if author_col.find("a"):
            authors = "; ".join([a.get_text(strip=True) for a in author_col.find_all("a")])
        else:
            authors = author_col.get_text(strip=True)  # Fallback for non-standard structure

        # Remove leading ";" and append "et. al." if applicable
        if authors.startswith(";"):
            authors = authors.lstrip(";").strip() + " et. al."

        # Extract Description
        highlight = cols[1].find("i")
        description = highlight.get_text(strip=True).replace("Highlight: ", "") if highlight else ""
        
        # Extract Source with hyperlink
        view_tag = cols[1].find("a", string="View", href=True)
        source_name = paper_tag['href'].split("paper_id=")[-1] if paper_tag else "Unknown"
        source_link = view_tag['href'] if view_tag else ""
        source = f"[{source_name}]({source_link})" if source_link else "N/A"
        
        # Extract Date
        date = cols[4].get_text(strip=True)
        
        # Add row to Markdown
        markdown.append(f"| {paper_name} | {authors} | {description} | {source} | {date} |")
    
    return "\n".join(markdown)

# Fetch the webpage
url = "https://www.paperdigest.org/2020/04/recent-papers-on-algorithmic-trading-high-frequency-trading/"
response = requests.get(url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")

# Extract and format table data
if table:
    markdown_table = extract_table_data(table)
    print(markdown_table)
else:
    print("No table found on the webpage.")
    