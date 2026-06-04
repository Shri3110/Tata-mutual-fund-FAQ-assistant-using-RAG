import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import io

def scrape_groww_url(url: str) -> str:
    """
    Scrapes the text content from a given Groww mutual fund URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove scripts and styles to avoid noise
    for script in soup(["script", "style"]):
        script.extract()
        
    # Get all text from the body, using newline separator to keep layout somewhat readable
    text = soup.body.get_text(separator='\n', strip=True) if soup.body else soup.get_text(separator='\n', strip=True)
    return text

def parse_pdf_from_url(pdf_url: str) -> str:
    """
    Downloads and extracts text from a PDF given its URL (e.g., KIM, SID, Factsheet).
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(pdf_url, headers=headers)
    response.raise_for_status()
    
    pdf_document = fitz.open(stream=response.content, filetype="pdf")
    text_content = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text_content += page.get_text() + "\n"
        
    return text_content

def parse_local_pdf(file_path: str) -> str:
    """
    Extracts text from a local PDF file.
    """
    pdf_document = fitz.open(file_path)
    text_content = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text_content += page.get_text() + "\n"
        
    return text_content

if __name__ == "__main__":
    # Example usage:
    # groww_text = scrape_groww_url("https://groww.in/mutual-funds/tata-digital-india-fund-direct-growth")
    # print(groww_text[:500])
    pass
