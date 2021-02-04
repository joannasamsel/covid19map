import pandas as pd
import geopandas as gpd
from kaggle_api import download_data_files, confirm_cases_path, global_methadata_path, RAW_global_confirm_path, death_cases_path
from shapely.geometry import Point

confirm_cases = pd.read_csv('./' + confirm_cases_path)
death_cases = pd.read_csv('./' + death_cases_path)
global_methadata = pd.read_csv('./' + global_methadata_path)
RAW_confirm_cases = pd.read_csv('./' + RAW_global_confirm_path)
points = global_methadata.apply(lambda row: Point(row.Long, row.Lat), axis=1)


def get_world():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    return world

def get_geo_data():
    geoData = gpd.GeoDataFrame(global_methadata, geometry=points)
    geoData.crs = {'init': 'epsg:4326'}
    geoData = geoData.to_crs(get_world().crs)
    return geoData

def get_cases_per_day(geoData, day):
    confirm = confirm_cases['Country/Region'] != 'Province/State'
    confirm_per_day = confirm_cases[confirm]
    confirm_per_day['Country/Region'] = confirm_per_day['Country/Region'].astype('datetime64[ns]')
    confirm_cases_per_day = confirm_per_day['Country/Region'] == str(day)
    confirm_cases_per_day = confirm_per_day[confirm_cases_per_day]
    if confirm_cases_per_day.empty:
        return confirm_cases_per_day
    index_value = confirm_cases_per_day.index.values
    confirm_cases_per_day = confirm_cases_per_day.transpose()
    geoData_joined = geoData.set_index('Country/Region').join(confirm_cases_per_day)
    #index_value = str(index_value).replace('[', '').replace(']', '')
    #geoData_joined = geoData_joined.rename(columns={161: 'cases'})
    geoData_joined['cases'] = geoData_joined[index_value]
    geoData_joined = geoData_joined[geoData_joined['cases'] != 'cases']
    geoData_joined['cases'] = geoData_joined['cases'].astype('float')
    geoData_joined['size_values'] = geoData_joined['cases'] / 100
    return geoData_joined

def get_death_per_day(geoData, day):
    deaths = death_cases['Country/Region'] != 'Province/State'
    deaths_per_day = death_cases[deaths]
    deaths_per_day['Country/Region'] = deaths_per_day['Country/Region'].astype('datetime64[ns]')
    death_cases_per_day = deaths_per_day['Country/Region'] == str(day)
    death_cases_per_day = deaths_per_day[death_cases_per_day]
    if death_cases_per_day.empty:
        return death_cases_per_day
    index_value = death_cases_per_day.index.values
    death_cases_per_day = death_cases_per_day.transpose()
    geoData_joined = geoData.set_index('Country/Region').join(death_cases_per_day)
    #index_value = str(index_value).replace('[', '').replace(']', '')
    #geoData_joined = geoData_joined.rename(columns={161: 'cases'})
    geoData_joined['cases'] = geoData_joined[index_value]
    geoData_joined = geoData_joined[geoData_joined['cases'] != 'cases']
    geoData_joined['cases'] = geoData_joined['cases'].astype('float')
    geoData_joined['size_values'] = geoData_joined['cases']/10
    return geoData_joined
