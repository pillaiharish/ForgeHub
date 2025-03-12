import pandas as pd
import time
import random
import logging
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from typing import List, Optional, Dict, Any

class GoogleTrendsHistoricalFetcher:
    def __init__(
        self, 
        keywords: List[str],
        timeframes: Optional[List[str]] = None,
        geo: str = "US"
    ):
        """
        Initialize Google Trends Historical Data Fetcher
        
        Args:
            keywords (List[str]): Keywords to fetch trends for
            timeframes (List[str], optional): Custom timeframes to fetch
            geo (str, optional): Geographic region
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

        # Validate and prepare inputs
        self.keywords = keywords
        self.geo = geo

        # Default timeframes if not specified
        self.timeframes = timeframes or [
            # Recent historical periods
            "today 1-m",   # Last 1 month
            "today 3-m",   # Last 3 months
            "today 1-y",   # Last 1 year
            "2024-01-01 2024-03-31",  # Specific date range example
        ]

        # Initialize pytrends
        self._initialize_pytrends()

    def _initialize_pytrends(self):
        """Initialize PyTrends with robust configuration"""
        try:
            self.pytrends = TrendReq(
                hl='en-US',      # English (US)
                tz=360,          # Timezone offset
                timeout=(10, 15) # Increased timeout
            )
        except Exception as e:
            self.logger.error(f"PyTrends initialization failed: {e}")
            raise

    def _generate_safe_filename(self, prefix: str) -> str:
        """
        Generate a safe, timestamped filename
        
        Args:
            prefix (str): Filename prefix
        
        Returns:
            str: Formatted filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keywords = "_".join(
            [k.replace(" ", "_").lower() for k in self.keywords[:3]]
        )
        return f"{prefix}_{safe_keywords}_{timestamp}.csv"

    def fetch_interest_over_time(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch interest over time for multiple timeframes
        
        Returns:
            Dict of DataFrames with interest data
        """
        results = {}

        for timeframe in self.timeframes:
            try:
                # Random delay to prevent rate limiting
                time.sleep(random.uniform(2, 5))

                # Build payload
                self.pytrends.build_payload(
                    self.keywords, 
                    timeframe=timeframe, 
                    geo=self.geo
                )

                # Fetch interest over time
                interest_df = self.pytrends.interest_over_time()

                if not interest_df.empty:
                    # Add timeframe as a column
                    interest_df['timeframe'] = timeframe
                    results[timeframe] = interest_df
                    self.logger.info(f"Successfully fetched data for timeframe: {timeframe}")
                else:
                    self.logger.warning(f"No data found for timeframe: {timeframe}")

            except Exception as e:
                self.logger.error(f"Error fetching data for timeframe {timeframe}: {e}")

        return results

    def fetch_related_topics(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch related topics for each timeframe
        
        Returns:
            Dict of DataFrames with related topics
        """
        results = {}

        for timeframe in self.timeframes:
            try:
                # Random delay
                time.sleep(random.uniform(2, 5))

                # Build payload
                self.pytrends.build_payload(
                    self.keywords, 
                    timeframe=timeframe, 
                    geo=self.geo
                )

                # Fetch related topics
                related_topics = self.pytrends.related_topics()

                if related_topics:
                    topics_data = []
                    for keyword, topics in related_topics.items():
                        rising = topics.get('rising')
                        top = topics.get('top')

                        if rising is not None and not rising.empty:
                            rising['topic_type'] = 'rising'
                            rising['original_keyword'] = keyword
                            topics_data.append(rising)

                        if top is not None and not top.empty:
                            top['topic_type'] = 'top'
                            top['original_keyword'] = keyword
                            topics_data.append(top)

                    if topics_data:
                        combined_df = pd.concat(topics_data, ignore_index=True)
                        combined_df['timeframe'] = timeframe
                        results[timeframe] = combined_df
                        self.logger.info(f"Successfully fetched related topics for timeframe: {timeframe}")
                else:
                    self.logger.warning(f"No related topics found for timeframe: {timeframe}")

            except Exception as e:
                self.logger.error(f"Error fetching related topics for timeframe {timeframe}: {e}")

        return results

    def save_to_csv(self, data: Dict[str, pd.DataFrame], prefix: str) -> List[str]:
        """
        Save collected data to CSV files
        
        Args:
            data (Dict[str, pd.DataFrame]): Data to save
            prefix (str): Filename prefix
        
        Returns:
            List of saved filenames
        """
        saved_files = []

        if not data:
            self.logger.warning("No data to save")
            return saved_files

        for timeframe, df in data.items():
            try:
                filename = self._generate_safe_filename(f"{prefix}_{timeframe.replace(' ', '_')}")
                df.to_csv(filename, index=True)
                saved_files.append(filename)
                self.logger.info(f"Saved data to {filename}")
            except Exception as e:
                self.logger.error(f"Error saving data for timeframe {timeframe}: {e}")

        return saved_files

def main():
    # Example keywords - replace with your desired topics
    keywords = [
        "python dev", 
        "Python", 
        "Machine Learning", 
        "AI Development"
    ]

    # Create fetcher instance
    fetcher = GoogleTrendsHistoricalFetcher(
        keywords=keywords,
        geo="US"  # Optional: specify geographic region
    )

    # Fetch and save interest over time
    interest_data = fetcher.fetch_interest_over_time()
    interest_files = fetcher.save_to_csv(interest_data, "interest_over_time")

    # Fetch and save related topics
    related_topics = fetcher.fetch_related_topics()
    topic_files = fetcher.save_to_csv(related_topics, "related_topics")

    # Print saved files
    print("Saved Interest Over Time Files:", interest_files)
    print("Saved Related Topics Files:", topic_files)

if __name__ == "__main__":
    main()