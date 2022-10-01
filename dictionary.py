import pandas as pd
import numpy as np
import website_util as ut
import json


'''
Function which makes a dictionary containing all relevant info (combining functionality
from functions below)
'''
def make_full_dict(df, year, sector):
    out = {}
    out['Year'] = year
    out['Sector'] = sector
    out['Quantiles'] = list(ut.find_percentiles(df[df['Sector'] == sector]['Employment'], 8))
    out['Employment'] = empl_by_sect(df, sector)
    
    return out

'''
Helper for make_full_dict
'''
def empl_by_sect(df, sector):
    copy = df.rename({'Employment': 'Value'}, axis = 1)
    sect = copy[copy['Sector'] == sector][['County', 'State', 'Value', 'Percent']]
    return sect.to_dict(orient = 'records') 


def write_full_dict(years):
    dicts = []
    for year in years:
        df  = pd.read_csv(f'readable/cbp_{year}.csv')
        dicts += [make_full_dict(df, year, sector) for sector in df['Sector'].unique()]

    with open(f'employment_quantiles.json', 'w') as f:
        json.dump(dicts, f)
'''
Makes the JSON string containing the total number and the percentage of each county's workers
employed in a specific sector
'''
def make_dict(year, df, sector):
    sect_df = ut.select_sector(df, sector)[['ctyname','Employment', 'Percent']]
    sect_df['ctyname'] = sect_df['ctyname'].str.replace(' County', '')
    
    empl_str = f'{year} {sector}'
    sect_df[empl_str] =  sect_df.apply(lambda row: str([row['Employment'], row['Percent']]), axis = 1)
    
    pivoted = sect_df.pivot_table(index = 'ctyname', values = empl_str, aggfunc = max)
    return pivoted.to_json()

'''
Makes the JSON string containing only the percentage of each county's workers
employed in a specific sector
'''
def make_dict_percent(year, df, sector):
    sect_df = ut.select_sector(df, sector)[['ctyname','Percent']]
    sect_df['ctyname'] = sect_df['ctyname'].str.replace(' County', '')
    
    empl_str = f'{year} {sector} percentage'
    
    sect_df.rename({'Percent': empl_str},
                   axis = 1, inplace = True)
    
    
    pivoted = sect_df.pivot_table(index = 'ctyname', values = empl_str)
    return pivoted.to_json()

'''
Writes the strings passed in to the given filepath
'''
def write_json(fp, strings):
    
    #could also do this validation when creating the strings
    with open(fp, 'w') as f:
        f.write('[')
        if len(strings) == 1:
            f.write(strings[0])
            f.write(']') 
            return
        
        for i, string in enumerate(strings):
            if i == 0:
                f.write(string[:-1])
                f.write(',')  
                continue
            if i == len(strings) - 1:
                f.write(string[1:])
                continue
            else:
                f.write(string[1:-1])
                f.write(',')
        f.write(']') 

'''
Makes the JSON strings containing full sector employment data for all years passed in
'''
def make_strings(years):
    out = []
    for year in years:
        df = pd.read_csv(f'readable/cbp_{year}.csv')

        for sector in df['Sector'].dropna().unique():
            string = make_dict(year, df, sector)
            if string == '{}':
                continue
            out.append(string)
    return out

'''
Makes the JSON strings containing full sector percentage data for all years passed in
'''
def make_strings_percent(years):
    out = []
    for year in years:
        df = pd.read_csv(f'readable/cbp_{year}.csv')

        for sector in df['Sector'].dropna().unique():
            string = make_dict_percent(year, df, sector)
            if string == '{}':
                continue
            out.append(string)
    return out


'''
Function used to create a dictionary containing the top 10 sectors
in terms of employment in the specified county and year 
'''
def top_10_dict(df, year, dictionary, county):
    key_string = f'{year} {county}'
    dictionary[key_string] = ut.get_top_10(df, county)

'''
Function which converts the top 10 counties dictionary to a json string
for the specified year.
'''
def top_10_json(year):
    df  = pd.read_csv(f'readable/cbp_{year}.csv')
    out = {}

    for county in df['ctyname'].dropna().unique():
        top_10_dict(df, year, out, county)

    return json.dumps(out)

'''
Makes list of top-10 json strings for all years passed in
'''
def make_top_10_strings(years):
    out = []
    for year in years:

        string = top_10_json(year)
        if string == '{}':
            continue
        out.append(string)
    return out

'''
Writes the list of top 10 JSON strings to the provided filepath
'''
def write_top_10_json(fp, strings):
    
    #could also do this validation when creating the strings
    with open(fp, 'w') as f:
        f.write('[')
        if len(strings) == 1:
            f.write(strings[0])
            f.write(']')
            return
        
        for i, string in enumerate(strings):
            if i == 0:
                f.write(string[:-1])
                f.write(',')  
                continue
            if i == len(strings) - 1:
                f.write(string[1:])
                continue
            else:
                f.write(string[1:-1])
                f.write(',')
        f.write(']')


'''
Function which writes a dictionary of the q quantile values
for employment in each sector for a given year. (Used for visualization)
'''
def quantiles_dictionary(year, dictionary, q):
    df = pd.read_csv(f'readable/cbp_{year}.csv')
    for sector in df['Sector'].unique():
        sect_df = df[df['Sector'] == sector]
        dictionary[f'{year} {sector}'] = ut.find_percentiles(sect_df['Employment'], q)
    

'''
Writes the q-quantile dictionary to a json file for all sectors for each year passed in
'''
def json_quantile_ranges(years, q):
    out = {}
    for year in years:
        quantiles_dictionary(year, out, q)
    
    with open(f'employment_quantiles.json', 'w') as f:
        json.dump(out, f)


'''
Function which writes the q-quantile dictionary to a json file
for the specified year. (Used for visualization)
'''
def quantile_json(year, q):
    df = df = pd.read_csv(f'readable/cbp_{year}.csv')
    out = {}

    quantiles_dictionary(year, df, out, q)

    with open(f'employment_quantiles_{year}.json', 'w') as f:
        json.dump(out, f)

'''
Creates a JSON string containing each county's quantile bin within a given year.
(Used for visualization)
'''
def bins_dictionary(year, sector, df):
    df = df[['ctyname', 'Bin']].pivot_table(index = 'ctyname', values = 'Bin')
    df.rename({'Bin': f'{year} {sector} bin'}, inplace = True, axis = 1)
    
    return df.to_json()

'''
Makes the JSON strings containing the bins for all sectors for each of the years
provided. (used for visualization)
'''
def make_bin_strings(years):
    out = []
    for year in years:
        df = pd.read_csv(f'readable/cbp_{year}.csv')

        for sector in df['Sector'].unique():
            string = bins_dictionary(year, sector, df)
            if string == '{}':
                continue
            out.append(string)
    return out

'''
Writes the JSON strings containing the bins for all sectors, for all years, to
a json file (Used for visualization).
'''
def write_bins_json(fp, strings):
    with open(fp, 'w') as f:
        if len(strings) == 1:
            f.write(strings[0])
            return
        
        for i, string in enumerate(strings):
            if i == 0:
                f.write(string[:-1])
                f.write(',')  
                continue
            if i == len(strings) - 1:
                f.write(string[1:])
                continue
            else:
                f.write(string[1:-1])
                f.write(',') 