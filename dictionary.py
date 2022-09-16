import pandas as pd
import numpy as np
import website_util as ut
import json


def make_dict(year, df, sector):
    sect_df = ut.select_sector(df, sector)[['ctyname', 'Employment']]
    sect_df['ctyname'] = sect_df['ctyname'].str.replace(' County', '')
    
    empl_str = f'{year} {sector}'
    
    sect_df.rename({'Employment': empl_str},
                   axis = 1, inplace = True)
    
    
    pivoted = sect_df.pivot_table(index = 'ctyname', values = empl_str)
    return pivoted.to_json()


def write_json(fp, strings):
    
    #could also do this validation when creating the strings
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

def make_strings(years):
    out = []
    for year in years:
        df = pd.read_csv(f'data/cbp_{year}.csv')

        for sector in df['Sector'].unique():
            string = make_dict(year, df, sector)
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
    df = df = pd.read_csv(f'data/cbp_{year}.csv')
    out = {}

    for county in df['ctyname'].unique():
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


def write_top_10_json(fp, strings):
    
    #could also do this validation when creating the strings
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


'''
Function which writes a dictionary of the q quantile values
for employment in each sector for a given year. (Used for visualization)
'''
def quantiles_dictionary(year, dictionary, q):
    df = df = pd.read_csv(f'data/cbp_{year}.csv')
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
    df = df = pd.read_csv(f'data/cbp_{year}.csv')
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
        df = pd.read_csv(f'data/cbp_{year}.csv')

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