"""
@author: Oren Ciolli
"""
import pandas as pd
import numpy as np


'''
Changes dataframe to readable form (displays county, state, and sector names),
and displays a single value for employment instead of bounds.
'''
def make_readable(empl, geo_ref, naics_ref):
    empl['Employment'] = empl['lb']
    
    #making geographic reference table readable
    geo_ref[['County', 'State']] = geo_ref['ctyname'].str.split(', ', expand = True)
    
    #merging geographic reference and employment data
    readable = (
        empl.merge(geo_ref, left_on = ['fipstate', 'fipscty'], 
                   right_on = ['fipstate', 'fipscty'], how = 'outer')
    )
    
    #merging naics reference and readable dataframe
    readable = readable.merge(naics_ref, left_on = 'naics', right_on = 'NAICS', how = 'outer') #should this be inner join
    
    
    ak_mask = (readable['State'] == 'AK')
    #readable.loc[ak_mask, 'ctyname'] = name_only(readable['ctyname'])
    
    readable.loc[ak_mask, 'ctyname'] = readable[ak_mask]['ctyname'].apply(name_only)
    
    return readable.rename({'DESCRIPTION': 'Sector'}, axis = 1)[['County', 'State', 'ctyname', 'Sector', 'Employment']]
    
    
def name_only(string):
    bor = string.replace(' Borough', '')
    mu = bor.replace(' Municipality', '')
    ca = mu.replace(' Census Area', '')
    city = ca.replace(' City and', ' City')
    
    no_city = city.replace(' City', '')

    return no_city

'''
Returns a dataframe which includes only the specified sector
'''
def select_sector(df, sector):
    return df[df['Sector'] == sector]

'''
Returns a subset of the dataframe containing only the specified county and state
'''
def get_county(df, ctyname):
    
    return df[df['ctyname'] == ctyname]

'''
Returns the employment number for the chosen sector in the county and state specified.
If the employment number cannot be calculated (possibly because the sector did not exist at the time), output 0
'''
def get_data(df, sector, ctyname):
    geo_df = get_county(df, ctyname)
    
    try:
        return select_sector(geo_df, sector)['Employment'].iloc[0]
    except:
        #print('Error loading data!') ##check what desired output is, validate input?
        return 0


'''
Takes in a list of geographical regions and returns a dataframe 
containing only the information from these regions.
Input dataframe can regard only one industry or more than one.
'''
def select_region(regions, df):
    return df[df['County'].isin(regions)]

'''
Passed in a dataframe (pertaining to the relevant year), a county, and state,
and returns the 10 sectors with the largest number of employees.
'''
def get_top_10(df, county):
    geo_df = df[df['ctyname'] == county].set_index('Sector')
    sorted_empl = geo_df['Employment'].sort_values(ascending = False)
    
    highest = []
    i = 0
    while len(highest) < 10 and i < len(sorted_empl):
        if sorted_empl.index[i] == 'Total for all sectors':
            i += 1
            continue
        elif f'{sorted_empl.index[i]}: {sorted_empl.values[i]}' in highest:
            i += 1
            continue
        else:
            highest.append(f'{sorted_empl.index[i]}: {sorted_empl.values[i]}')
            i += 1
    
    return highest

'''
Returns a Python list containing all sectors in the dataframe
'''
def all_sectors(df):
    return df['Sector'].unique().tolist()

'''
Returns an array of length q containing the partition values of the q-quantiles
of the input series. Used to create the gradient in visualization.
'''
def find_percentiles(ser, q):
    perc_arr = []
    for n in np.arange(1, q+1):
        perc_arr.append(np.nanpercentile(ser, ((n/q) * 100)))
        
    return perc_arr

'''
Computes the bin that a given county falls into (Used for visualization)
'''
def find_bin(val, percs):
    if val >= percs[-1]:
        return len(percs)+1
    out = 1
    i = 0
    while val > percs[i]:
        out += 1
        i += 1
    return out
    