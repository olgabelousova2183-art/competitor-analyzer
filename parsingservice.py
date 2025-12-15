"""Selenium-based parsing service for competitor websites"""
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from config import COMPETITOR_URLS, SELENIUM_HEADLESS, SELENIUM_TIMEOUT, HISTORY_DIR
import os


class ParsingService:
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        if SELENIUM_HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(SELENIUM_TIMEOUT)
        except Exception as e:
            print(f"Error setting up driver: {e}")
            raise
    
    def parse_url(self, url: str) -> Dict[str, Any]:
        """
        Parse a single URL and extract relevant data
        """
        if not self.driver:
            self.setup_driver()
        
        result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "data": {}
        }
        
        try:
            print(f"Parsing URL: {url}")
            self.driver.get(url)
            time.sleep(3)  # Wait for dynamic content to load
            
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract key information
            title = soup.find('title')
            result["data"]["title"] = title.get_text().strip() if title else "No title"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            result["data"]["meta_description"] = meta_desc.get('content', '') if meta_desc else ""
            
            # Extract headings
            headings = {}
            for i in range(1, 7):
                h_tags = soup.find_all(f'h{i}')
                headings[f'h{i}'] = [h.get_text().strip() for h in h_tags]
            result["data"]["headings"] = headings
            
            # Extract main text content
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                # Remove script and style elements
                for script in main_content(["script", "style"]):
                    script.decompose()
                text_content = main_content.get_text(separator=' ', strip=True)
                result["data"]["text_content"] = text_content[:5000]  # Limit to 5000 chars
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                if href and text:
                    links.append({"url": href, "text": text[:100]})
            result["data"]["links"] = links[:50]  # Limit to 50 links
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                alt = img.get('alt', '')
                if src:
                    images.append({"src": src, "alt": alt})
            result["data"]["images"] = images[:20]  # Limit to 20 images
            
            # Extract meta keywords
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                keywords = meta_keywords.get('content', '').split(',')
                result["data"]["keywords"] = [k.strip() for k in keywords]
            
            result["success"] = True
            print(f"Successfully parsed: {url}")
            
        except TimeoutException:
            result["error"] = "Page load timeout"
        except WebDriverException as e:
            result["error"] = f"WebDriver error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
        
        return result
    
    def parse_all_competitors(self) -> List[Dict[str, Any]]:
        """Parse all competitor URLs from config"""
        results = []
        for url in COMPETITOR_URLS:
            result = self.parse_url(url)
            results.append(result)
            time.sleep(2)  # Be polite with delays
        
        return results
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def save_to_history(self, results: List[Dict[str, Any]]):
        """Save parsing results to history"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(HISTORY_DIR, f"parsing_results_{timestamp}.json")
        
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history_entry, f, ensure_ascii=False, indent=2)
        
        print(f"Results saved to: {filename}")
        return filename


def get_parsing_service() -> ParsingService:
    """Get or create parsing service instance"""
    return ParsingService()

