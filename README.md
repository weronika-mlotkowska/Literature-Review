## Metadata Extraction Pipeline

A modular Python pipeline for extracting publication metadata from the Elsevier Scopus API based on a list of DOIs.

### Features
- Reads input DOIs from CSV or JSON
- Queries the Elsevier Scopus API for each DOI
- Extracts metadata such as:
    Publication venue
    Year
    Title
    Citation count
- Writes results to JSON output

### Usage
1. Prepare a CSV file containing a `doi` column, e.g.:
   ```csv
   doi
   10.1145/3706598.3714276
    10.1145/3706598.3714095
    10.1145/3706598.3713835
   ```

2. Run the script:
   ```bash
   python data_extraction.py
   ```

3. The results will be saved in:
   ```
   files_output/data_test.json
   ```

Example output:

```json
{
  "10.1145/3706598.3714276": {
    "venue": "Conference on Human Factors in Computing Systems Proceedings",
    "year": "2025",
    "title": "PCB Renewal: Iterative Reuse of PCB Substrates for Sustainable Electronic Making",
    "citedby_count": "2"
  }
}
```

### Important
- Requires an active **Elsevier API Key** (X-ELS-APIKey) and (in most cases) **Institution Token** (X-ELS-Insttoken)
    If you are accessing the API outside your institution’s network, you may need to include the Institution Token to authenticate.
- Rate limits imposed by Elsevier may apply