import requests
from dataclasses import dataclass
from typing import Callable, List, Dict, Protocol
import pandas as pd
import json

API_KEY = '' #your API key
Insttoken='' #your Institution Token

HEADERS = {
    "Accept": "application/json",
    "X-ELS-APIKey": API_KEY,
    "X-ELS-Insttoken":Insttoken
}

@dataclass
class Config:
    input_file: str
    output_file:str

class InputReader(Protocol):
    def read(self, file: str) -> List: ...


class CSVReader:
    def read(self, file: str) -> List:
        dois=pd.read_csv(file)
        return list(dois['doi'])

class JSONReader:
    def read(self, file: str) -> List:
        with open(file,'r') as f:
            data=json.load(f)
        return list(data.keys())
    
class JSONResultWriter():
    def write(self, report: Dict[str, object], output_file: str) -> None:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

class MetadataExtractor:
    def __init__(
        self, reader: InputReader, metrics: List[Callable]
    ):
        self.reader = reader
        self.metrics = metrics

    def extract(self, config: Config) -> Dict[str, object]:
        dois = self.reader.read(config.input_file)
        result={}
        for i, doi in enumerate(dois, 1):
            print(f"[{i}/{len(dois)}] Processing DOI: {doi}")
            metadata = {}
            url=f"https://api.elsevier.com/content/search/scopus?query=DOI({doi})"
            entries=get_work(doi,url)["search-results"]["entry"]
            for metric in self.metrics:
                metadata.update(metric(entries))
            result[doi]=metadata
        return result
    
def get_work(doi:str,url:str) -> Dict:
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        print(f"Error fetching work for {doi}: {str(e)}")
        return {}

def get_publicationName(entries:Dict) -> Dict[str, str]:
    try:
        if entries:
            return {'venue':entries[0]['prism:publicationName']}
        else:
            return {'venue':'-'}
    except Exception as e:
        print(f"Error fetching publicationName: {str(e)}")
        return {'venue':'-'}
    
def get_year(entries:Dict) -> Dict[str, str]:
    try:
        if entries:
            return {'year':entries[0]['prism:coverDate'][:4]}
        else:
            return {'year':'-'}
    except Exception as e:
        print(f"Error fetching year: {str(e)}")
        return {'year ':'-'}
    
def get_title(entries:Dict) -> Dict[str, str]:
    try:
        if entries:
            return {'title':entries[0]['dc:title']}
        else:
            return {'title':'-'}
    except Exception as e:
        print(f"Error fetching title: {str(e)}")
        return {'title':'-'}

def get_citedbyCount(entries:Dict) -> Dict[str, str]:
    try:
        if entries:
            return {'citedby_count':entries[0]['citedby-count']}
        else:
            return {'citedby_count':'-'}
    except Exception as e:
        print(f"Error fetching citedbyCount: {str(e)}")
        return {'citedby_count':'-'}

def get_refDOIs(entries:Dict) -> Dict[str, str]:
    #to do
    pass

def main():
    config = Config(
        input_file="files_input/dois_test.csv",
        output_file='files_output/data_test.json'
    )
    preprocessing_steps = [
        get_publicationName,
        get_year,
        get_title,
        get_citedbyCount
    ]
    reader = CSVReader()
    if not API_KEY:
        raise ValueError("API_KEY and/or Insttoken must be set before running.")
    else:
        extractor = MetadataExtractor(reader, preprocessing_steps)
        report = extractor.extract(config)
        writer = JSONResultWriter()
        writer.write(report, config.output_file)

if __name__ == "__main__":
    main()