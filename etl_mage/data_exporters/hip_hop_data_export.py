from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage_bucket'
    object_key = 'staging/hip_hop_artists_death.csv'
    # format = 'XML'

    from google.cloud import storage
    
    path_to_private_key = './credentials.json'
    client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)

    # The bucket on GCS in which to write the CSV file
    bucket = client.bucket(bucket_name)
    # The name assigned to the CSV file on GCS
    blob = bucket.blob(object_key)
    blob.upload_from_string(df.to_csv(), 'text/csv')
    
    # GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
    #     df,
    #     bucket_name,
    #     object_key,
    #     'text/csv'
    # )

