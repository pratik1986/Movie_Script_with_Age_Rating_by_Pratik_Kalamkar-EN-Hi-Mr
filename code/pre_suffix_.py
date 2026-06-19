# Open the input and output files
with open('hindi_movie_list.txt', 'r') as infile, open('output_hin.txt', 'w') as outfile:
    # Define the prefix and suffix
    prefix = "year "
    suffix = " hindi movie age rating certificate"
    
    # Iterate through each line in the input file
    for line in infile:
        # Remove any leading/trailing whitespace from the line
        line = line.strip()
        
        # Write the prefixed and suffixed line to the output file
        outfile.write(f"{prefix}{line}{suffix}\n")

print("Prefix and suffix added to each line.")
