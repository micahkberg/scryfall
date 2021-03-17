import pandas as pd
import xml.etree.ElementTree as ET

def read_scry(fname):
    df = pd.read_json(fname)
    cols_keep = pd.Index(['object','id','mtgo_id','mtgo_foil_id','name','mana_cost','type_line','prices'])
    small_df = df[cols_keep]
    
    #scryfall database doesn't have entry for event tickets, but it seems like a good thing to include for calculating account value
    ticket = pd.DataFrame({'mtgo_id':1,'name':'Event Ticket','prices': [{'tix':1,'usd':1}]})
    small_df = small_df.append(ticket)
    
    return small_df
    
def read_dek(fname):
    file = open(fname, 'r')
    dek_xml = file.read()
    etree = ET.fromstring(dek_xml)
    cols = ['mtgo_id','Quantity','Name']
    dek_df = pd.DataFrame(columns=cols)
    for i in etree:
        row = pd.Series([i.get("CatID"),i.get('Quantity'),i.get('Name')],index=cols)
        dek_df = dek_df.append(row,ignore_index=True)
        
    dek_df = dek_df.dropna().astype({"mtgo_id": int})
    
    return(dek_df)