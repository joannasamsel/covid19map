from kaggle.api.kaggle_api_extended import KaggleApi

dataset = 'antgoldbloom/covid19-data-from-john-hopkins-university'
confirm_cases_path = 'CONVENIENT_global_confirmed_cases.csv'
death_cases_path = 'CONVENIENT_global_deaths.csv'
global_methadata_path = 'CONVENIENT_global_metadata.csv'
RAW_global_confirm_path = 'RAW_global_confirmed_cases.csv'


def download_data_files():
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file(dataset=dataset, file_name=confirm_cases_path)
    api.dataset_download_file(dataset=dataset, file_name=global_methadata_path)
    api.dataset_download_file(dataset=dataset, file_name=RAW_global_confirm_path)
    api.dataset_download_file(dataset=dataset, file_name=death_cases_path)
