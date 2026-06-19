"""
Movie Script Validator and Organizer

This script:
1. Validates movie script filenames in format: {RATING}_{TITLE}_{YEAR}.txt
2. Checks against OMDB API for official rating and year
3. Handles equivalent ratings (PG-13/PG13, NC-17/NC17)
4. Moves mismatched files to manual_veri folder
5. Provides detailed verification summary
"""

import os
import requests
import shutil
from urllib.parse import quote
from dotenv import load_dotenv
import re

# Configuration
folder_path = r"G:\My Drive\PhDWorks\4_Final_Writing_Papers\05_ConferencePaper_3\dataset\English_unbal"
manual_veri_path = os.path.join(folder_path, "manual_veri")
env_file = r"G:\My Drive\PhDWorks\4_Final_Writing_Papers\05_ConferencePaper_3\dataset\key_.env"

# Ensure manual_veri folder exists
os.makedirs(manual_veri_path, exist_ok=True)

def load_api_key(env_path):
    """Load OMDB API key from .env file"""
    try:
        load_dotenv(env_path)
        return os.getenv("OMDB_API_KEY")
    except Exception as e:
        print(f"Error loading .env file: {str(e)}")
        return None

def parse_filename(filename):
    """Extract rating, title, and year from filename"""
    pattern = r"^(G|PG|PG-13|R|NC-17)_(.+?)_(\d{4})\.txt$"
    match = re.match(pattern, filename)
    if match:
        return match.groups()  # (rating, title, year)
    return None, None, None

def normalize_rating(rating):
    """Standardize ratings (PG-13 → PG13, NC-17 → NC17)"""
    return rating.replace("-", "").upper()

def get_movie_info(title, api_key):
    """Query OMDB API for movie information"""
    base_url = "http://www.omdbapi.com/"
    encoded_title = quote(title.replace("_", " "))  # Convert underscores to spaces
    url = f"{base_url}?t={encoded_title}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)  # Added timeout
        data = response.json()
        if data.get("Response") == "True":
            year = data.get("Year", "").split("–")[0]  # Handle year ranges
            rating = data.get("Rated", "")
            return normalize_rating(rating), year  # Return normalized rating
        return None, None
    except Exception as e:
        print(f"API request failed for '{title}': {str(e)}")
        return None, None

def verify_files():
    """Main verification workflow"""
    api_key = load_api_key(env_file)
    if not api_key:
        print("Failed to load API key. Exiting.")
        return

    stats = {
        "total_files": 0,
        "correct": 0,
        "incorrect": [],
        "api_errors": 0,
        "skipped": 0
    }

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        stats["total_files"] += 1
        file_rating, file_title, file_year = parse_filename(filename)

        if not all([file_rating, file_title, file_year]):
            stats["skipped"] += 1
            print(f"Skipped (invalid format): {filename}")
            continue

        # Query OMDB (returns normalized rating)
        omdb_rating, omdb_year = get_movie_info(file_title, api_key)
        
        if not omdb_rating or not omdb_year:
            stats["api_errors"] += 1
            print(f"API error/no data: {filename}")
            continue

        # Compare normalized ratings and years
        is_correct = (
            omdb_rating == normalize_rating(file_rating) and 
            omdb_year == file_year
        )

        if is_correct:
            stats["correct"] += 1
            print(f"✓ Correct: {filename}")
        else:
            stats["incorrect"].append(filename)
            src = os.path.join(folder_path, filename)
            dst = os.path.join(manual_veri_path, filename)
            shutil.move(src, dst)
            print(f"✗ Moved (mismatch): {filename} | OMDB: {omdb_rating}/{omdb_year}")

    # Generate report
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Correct: {stats['correct']}")
    print(f"Incorrect (moved to manual_veri): {len(stats['incorrect'])}")
    print(f"API errors: {stats['api_errors']}")
    print(f"Skipped (invalid format): {stats['skipped']}")
    
    if stats["incorrect"]:
        print("\nINCORRECT FILES:")
        for i, name in enumerate(stats["incorrect"], 1):
            print(f"{i}. {name}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    verify_files()