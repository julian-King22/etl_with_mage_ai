if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import requests
from bs4 import BeautifulSoup

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    response = requests.get("https://en.wikipedia.org/wiki/List_of_murdered_hip_hop_musicians")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_rows = soup.find('table')
    
    headers = [header.text.strip() for header in table_rows.find_all('th')]

    # print(headers[:6])

    rows = []

    # Find all `tr` tags
    data_rows = table_rows.find_all('tr')

    for row in data_rows[1:]:
        header = row.find_all('th')

        value = row.find_all('td')
        beautified_name = [ele.text.strip() for ele in header]
        beautified_value = [val.text.strip() for val in value]
        
        beautified_value.insert(0,beautified_name[0])
        
       
        rows.append(beautified_value)


    import pandas as pd

    hip_hop_df = pd.DataFrame(rows, columns = headers[:6])

    # print(hip_hop_df.head())

    from google.cloud import storage
    
    path_to_private_key = './credentials.json'
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)

    # The bucket on GCS in which to write the CSV file
    bucket = client.bucket('mage_bucket')
    # The name assigned to the CSV file on GCS
    blob = bucket.blob('raw/hip_hop_artist_death.csv')
    blob.upload_from_string(hip_hop_df.to_csv(), 'text/csv')
    
    
    # import csv

    # with open('hip_hop_deat.csv', 'w', newline="") as output:
    #     writer = csv.writer(output)
    #     writer.writerow(headers[:6])
    #     writer.writerows(rows)
    
    return True

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
