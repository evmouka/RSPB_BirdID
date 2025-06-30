import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
import re
from dataclasses import dataclass
import logging
import time
from urllib.parse import urljoin

@dataclass
class RspbBirdData:
    common_name: str
    scientific_name: Optional[str]
    length_cm: Optional[str]
    wingspan_cm: Optional[str]
    description: str
    colors: List[str]
    habitat: List[str]
    url: str
    
class RspbScraper:
    def __init__(self):
        self.base_url = "https://www.rspb.org.uk"
        self.bird_guide_url = "https://www.rspb.org.uk/birds-and-wildlife/wildlife-guides/bird-a-z/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_all_bird_urls(self) -> List[str]:
        """Get URLs for all birds in the RSPB bird guide"""
        self.logger.info("Fetching bird guide index page...")
        response = self.session.get(self.bird_guide_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        bird_urls = []
        # Find all bird links in the A-Z guide
        for link in soup.find_all('a', href=re.compile("/birds-and-wildlife/wildlife-guides/bird-a-z/.+")):
            bird_url = urljoin(self.base_url, link['href'])
            bird_urls.append(bird_url)
            
        self.logger.info(f"Found {len(bird_urls)} bird pages")
        return bird_urls

    def extract_bird_data(self, url: str) -> Optional[RspbBirdData]:
        """Extract bird information from a single RSPB bird page"""
        try:
            self.logger.info(f"Fetching data for: {url}")
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract bird name
            name_element = soup.find('h1', class_='wildlife-header__title')
            if not name_element:
                return None
            common_name = name_element.text.strip()

            # Extract scientific name
            scientific_name = None
            scientific_element = soup.find('em', class_='wildlife-header__latin-name')
            if scientific_element:
                scientific_name = scientific_element.text.strip()

            # Extract description
            description = ""
            desc_element = soup.find('div', class_='wildlife-description')
            if desc_element:
                description = desc_element.text.strip()

            # Extract measurements
            length_cm = None
            wingspan_cm = None
            stats_elements = soup.find_all('div', class_='wildlife-stats__stat')
            for stat in stats_elements:
                label = stat.find('div', class_='wildlife-stats__label')
                value = stat.find('div', class_='wildlife-stats__value')
                if label and value:
                    if 'Length' in label.text:
                        length_cm = self._extract_measurement(value.text)
                    elif 'Wingspan' in label.text:
                        wingspan_cm = self._extract_measurement(value.text)

            # Extract habitat information
            habitats = []
            habitat_section = soup.find('section', class_='wildlife-habitat')
            if habitat_section:
                habitat_items = habitat_section.find_all('div', class_='wildlife-habitat__item')
                habitats = [item.text.strip() for item in habitat_items]

            # Extract colors from description
            colors = self._extract_colors(description)

            return RspbBirdData(
                common_name=common_name,
                scientific_name=scientific_name,
                length_cm=length_cm,
                wingspan_cm=wingspan_cm,
                description=description,
                colors=colors,
                habitat=habitats,
                url=url
            )

        except Exception as e:
            self.logger.error(f"Error processing {url}: {str(e)}")
            return None

    def _extract_measurement(self, text: str) -> Optional[str]:
        """Extract numerical measurements from text"""
        match = re.search(r'(\d+(?:-\d+)?)\s*cm', text)
        if match:
            return match.group(1)
        return None

    def _extract_colors(self, text: str) -> List[str]:
        """Extract color mentions from text"""
        color_words = {
            'blue', 'black', 'brown', 'grey', 'gray', 'green', 'orange',
            'pink', 'purple', 'red', 'yellow', 'white', 'beige', 'buff',
            'cream', 'chestnut'
        }
        
        # Convert text to lowercase and find all words
        words = text.lower().split()
        # Extract colors mentioned in the text
        colors = list(set(word for word in words if word in color_words))
        return colors

    def scrape_all_birds(self) -> pd.DataFrame:
        """Scrape data for all birds and return as a DataFrame"""
        bird_urls = self.get_all_bird_urls()
        bird_data = []

        for url in bird_urls:
            data = self.extract_bird_data(url)
            if data:
                bird_data.append({
                    'common_name': data.common_name,
                    'scientific_name': data.scientific_name,
                    'length_cm': data.length_cm,
                    'wingspan_cm': data.wingspan_cm,
                    'description': data.description,
                    'colors': ','.join(data.colors),
                    'habitat': ','.join(data.habitat),
                    'url': data.url
                })
            # Be nice to RSPB's servers
            time.sleep(1)

        df = pd.DataFrame(bird_data)
        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str = 'rspb_birds.csv'):
        """Save the scraped data to a CSV file"""
        df.to_csv(filename, index=False)
        self.logger.info(f"Data saved to {filename}")

def process_length_range(length_str: Optional[str]) -> tuple:
    """Process length string into min and max values"""
    if not length_str:
        return None, None
    
    if '-' in length_str:
        min_len, max_len = map(float, length_str.split('-'))
        return min_len, max_len
    else:
        try:
            length = float(length_str)
            return length, length
        except ValueError:
            return None, None

def categorize_size(length: float) -> str:
    """Categorize bird size based on length"""
    if length < 15:
        return 'very_small'
    elif length < 25:
        return 'small'
    elif length < 40:
        return 'medium'
    elif length < 70:
        return 'large'
    else:
        return 'very_large'

def main():
    # Initialize scraper
    scraper = RspbScraper()
    
    # Scrape data
    df = scraper.scrape_all_birds()
    
    # Process lengths and add size categories
    df[['min_length', 'max_length']] = df['length_cm'].apply(
        lambda x: pd.Series(process_length_range(x))
    )
    df['mean_length'] = df[['min_length', 'max_length']].mean(axis=1)
    df['size_category'] = df['mean_length'].apply(lambda x: categorize_size(x) if pd.notnull(x) else None)
    
    # Save raw data
    scraper.save_to_csv(df)
    
    print("\nData collection summary:")
    print(f"Total birds processed: {len(df)}")
    print("\nSize categories distribution:")
    print(df['size_category'].value_counts())
    print("\nMost common colors:")
    colors_series = df['colors'].str.split(',').explode()
    print(colors_series.value_counts().head())

if __name__ == "__main__":
    main()