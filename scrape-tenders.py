import json
import time
from alive_progress import alive_bar
import pandas as pd
import requests

csv_file = r'scrapped.csv'

def get_tender_list():
  
  json_content = {
    "financialyr": "2022-2023",
    "pe_id": 0
  }
  
  api_url = 'https://tenders.go.ke/api/contract/Submit/ID/financialyr'
  
  r = requests.post(api_url, json=json_content)
  
  
  return json.loads(r.text)

def get_needed_fields(tender_list):
  NEEDED_FIELDS = (
    'name', 
    'contractnumber',
    'title',
    'supplier_name',
    'amount',
    'startdate',
    'petype',
    'procurementmethod',
    'pin_number',
    'awarddate',
    'enddate',
  )
  
  sorted_tender_list = []
  for tender in tender_list:
    current_sorted_tender = { field: tender[field] for field in NEEDED_FIELDS }
    sorted_tender_list.append(current_sorted_tender)
  
  return sorted_tender_list
  

def main():
  # looping through pages
  print('')
  print(f'fetching tenders... \n')  
  with alive_bar(0) as bar:
    tender_list = get_tender_list()
    sorted_tender_list = get_needed_fields(tender_list)
      
    # creating dataframe
    df = pd.DataFrame(sorted_tender_list)
    # creating csv file
    print('creating csv file...')
    df.to_csv (csv_file, index = None)

      
    print('\n')
    print(len(sorted_tender_list), f'tenders collected. saved in {csv_file}')
    
    time.sleep(.001)
    bar()

if __name__ == "__main__":
  main()