import webbrowser
import time

# File containing the lines you want to search
input_file = 'output_mr.txt'

# Open the input file and read each line
with open(input_file, 'r') as infile:
    for line in infile:
        # Strip leading/trailing whitespaces from the line
        query = line.strip()
        
        # Create the Google search URL
        search_url = f"https://www.google.com/search?q={query}"
        
        # Open the search in a new browser tab
        webbrowser.open_new_tab(search_url)
        
        # Wait for 5 seconds before opening the next search
        time.sleep(5)

print("All searches are done!")
