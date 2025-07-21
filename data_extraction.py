import requests

def title_year(paper):
    if 'message' in paper:
        try:
            if 'published-print' in paper['message']:
                year= paper['message']['published-print']['date-parts'][0][0]  
            elif 'created' in paper['message']:
                    year= paper['message']['created']['date-parts'][0][0]
            else: year='-'
        except Exception as e:
            print(f"Error fetching year for {paper['message']['DOI']}: {str(e)}")
            year='-'
        try:
            if 'title' in paper['message']:
                title=paper['message']['title'][0]
            else: title='-'
        except Exception as e:
            print(f"Error fetching title for {paper['message']['DOI']}: {str(e)}")
            title='-'
    else:
        return '-','-'
    return title,year  

def references(paper,doi):
    try:
        if paper and 'message' in paper and 'reference' in paper['message']:
            return [ref.get('DOI') for ref in paper['message']['reference'] if ref.get('DOI')]
    except Exception as e:
        print(f"Error fetching references for {doi}: {str(e)}")
    return []
    
def get_data(doi):
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data for {doi}: {str(e)}")
