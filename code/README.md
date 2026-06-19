# Dataset Creation and Verification Scripts

This folder contains scripts used during the construction of the following datasets:

- Movie_Script_with_Age_Rating_by_Pratik_Kalamkar-EN
- Movie_Script_with_Age_Rating_by_Pratik_Kalamkar-Hi
- Movie_Script_with_Age_Rating_by_Pratik_Kalamkar-Mr

## Purpose

The scripts were developed to assist in:

- Movie title normalization
- Metadata collection
- Age_Rating verification
- OMDb validation
- Manual review preparation
- Dataset quality assurance

## Files

### cross_check_OMDB.py

Validates movie filenames against OMDb metadata.

Functions:
- Extracts Age_Rating, title, and release year from filenames
- Queries OMDb API
- Verifies metadata consistency
- Identifies mismatches for manual review

### pre_suffix_.py

Generates search queries used to collect Age_Rating information from public sources.

Example query:

year <movie title> hindi movie age rating certificate

### google_search.py

Automates Google searches for English movie certification verification.

### google_search_Hi.py

Automates Google searches for Hindi movie certification verification.

### google_search_Mr.py

Automates Google searches for Marathi movie certification verification.

## Note

These scripts were created as part of the dataset curation workflow and are provided for transparency and reproducibility purposes. They may require modification before reuse in other projects.

## Citation

If you use the datasets associated with these scripts, please cite:

Kalamkar, P. N., Peddi, P., & Sharma, Y. K. (2026).

Lightweight and Explainable Neural Models for Multilingual Movie Script Certification.

DOI: 10.5815/ijitcs.2026.02.09