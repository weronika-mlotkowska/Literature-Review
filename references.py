from typing import List, Dict
import utils

def get_refCount(data):
    try:
        return data['item']['bibrecord']['tail']['bibliography']['@refcount']
    except Exception as e:
        print(f"Error fetching references count: {str(e)}")
        return ''

def get_id(data:Dict) -> str:
    doi=''
    if 'ref-website' in data and 'ce:e-address' in data['ref-website'] and '$' in data['ref-website']['ce:e-address']:
        doi=data['ref-website']['ce:e-address']['$']
        if 'doi.org/' in doi:
            return doi.split('doi.org/')[-1]
    if 'refd-itemidlist' in data and 'itemid' in data['refd-itemidlist']:
        try:
            item=data['refd-itemidlist']['itemid']
            if type(item)==list:
                for idx, element in enumerate(item):
                    if item[idx]['@idtype']=='DOI':
                        return element['$']
            elif doi=='':
                doi = item['$']
        except Exception as e:
            print(f"No id in refd-itemidlist: {str(e)}")
            pass
    return doi


def get_refIds(data:Dict) -> List[str]:
    dois=[]
    try:
        references=data['item']['bibrecord']['tail']['bibliography']['reference']
        ref_data={}
        print(f"Retrieving {len(references)} references...")            
        for i,ref in enumerate(references,1):
            if i%10==0:
                print(f"[{i}/{len(references)}]")
            try:
                if 'ref-info' in ref:
                    id=get_id(ref['ref-info'])
                    if id!='':
                        dois.append(id)
                        ref_data[id]=ref['ref-info']
            except Exception as e:
                print(f'Error: {str(e)}')
                continue
        if len(ref_data)>0:
            writer = utils.JSONResultWriter()
            writer.write(ref_data,f'references_{work_doi.replace("/","_").replace(".","_")}.json','files_references')
    except Exception as e:
        print(f"No references retrieved for {work_doi} : {str(e)}")
    finally:
        return dois


def get_referencesInfo(entries:Dict,doi:str) -> Dict[str, str]:
    global work_doi
    work_doi=doi
    dois=[]
    ref_count=''
    if entries:
        try:
            ref_url=entries[0]['link'][0]['@href']
            data=utils.get_work('',ref_url)['abstracts-retrieval-response']
            ref_count=get_refCount(data)
            dois=get_refIds(data)
        except Exception as e:
            print(f"Error fetching refDOIs: {str(e)}")
        finally:
            return {'ref_count':ref_count,'ref':dois}
    return {'ref_count':ref_count,'ref':dois}
    