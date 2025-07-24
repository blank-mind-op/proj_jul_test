from src.crawler import crawl
from src.scraper import ParagraphScraper, sherlock_scrape
from src.timeline import create_timeline
from src.crawler import get_html
from src.analysis.image import download_image, recognize_faces
from src.analysis.graph import create_connection_graph, draw_graph
from src.reporting.generator import generate_report
import numpy as np

def main():
    """
    The main function for the command-line interface.
    """
    print("--- OSINT Tool ---")
    print("Welcome to the OSINT tool. Please choose an option to begin.")

    while True:
        print("\n--- Menu ---")
        print("1. Crawl a website and generate a timeline")
        print("2. Find social media accounts with Sherlock")
        print("3. Analyze an image for a person")
        print("4. Create a connection graph from scraped data")
        print("5. Generate a full report")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start_url = input("Enter the starting URL to crawl: ")
            keyword = input("Enter the keyword to search for: ")
            print("\nCrawling and scraping...")
            visited_urls = crawl(start_url)
            all_scraped_data = []
            for url in visited_urls:
                html = get_html(url)
                if html:
                    scraper = ParagraphScraper(html, keyword)
                    scraped_data = scraper.scrape()
                    all_scraped_data.extend(scraped_data)
            print("\nCreating timeline...")
            timeline_df = create_timeline(all_scraped_data)
            print("\n--- Timeline ---")
            for index, row in timeline_df.iterrows():
                print(f"[{row['timestamp'].strftime('%Y-%m-%d')}] {row['text']}")

        elif choice == '2':
            username = input("Enter the username to search for: ")
            print("\nSearching for social media accounts...")
            results = sherlock_scrape(username)
            if results:
                print("\n--- Sherlock Results ---")
                for site, data in results.items():
                    if data.get('url_main'):
                        print(f"- {site}: {data['url_main']}")
            else:
                print("No accounts found.")

        elif choice == '3':
            image_url = input("Enter the URL of the image to analyze: ")
            person_embedding = np.random.rand(128)
            print("\nDownloading and analyzing image...")
            image = download_image(image_url)
            if image is not None:
                if recognize_faces(image, person_embedding):
                    print("The person was recognized in the image.")
                else:
                    print("The person was not recognized in the image.")
            else:
                print("Could not download or process the image.")

        elif choice == '4':
            start_url = input("Enter the starting URL to crawl: ")
            keyword = input("Enter the keyword to search for (e.g., a person's name): ")
            print("\nCrawling and scraping...")
            visited_urls = crawl(start_url)
            all_scraped_data = []
            for url in visited_urls:
                html = get_html(url)
                if html:
                    scraper = ParagraphScraper(html, keyword)
                    scraped_data = scraper.scrape()
                    all_scraped_data.extend(scraped_data)
            print("\nCreating connection graph...")
            G = create_connection_graph(all_scraped_data)
            print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
            draw_graph(G)

        elif choice == '5':
            start_url = input("Enter the starting URL to crawl: ")
            keyword = input("Enter the keyword to search for (e.g., a person's name): ")
            print("\nCrawling and scraping...")
            visited_urls = crawl(start_url)
            all_scraped_data = []
            for url in visited_urls:
                html = get_html(url)
                if html:
                    scraper = ParagraphScraper(html, keyword)
                    scraped_data = scraper.scrape()
                    all_scraped_data.extend(scraped_data)
            print("\nAnalyzing data and generating report...")
            timeline_df = create_timeline(all_scraped_data)
            G = create_connection_graph(all_scraped_data)
            report = generate_report(timeline_df, G)
            print("\n--- Report ---")
            print(report)

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
