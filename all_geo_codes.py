import pandas as pd
import numpy as np
import json

def geo_by_yr(df):
    all_sec = df['ctyname'].unique()
    return [{'value': sec, 'label': sec} for sec in all_sec]
    

geo_ref_2012_2016 = pd.read_csv('reference_files/geo_ref_2012_2016.csv')
geo_ref_2002_2011 = pd.read_csv('reference_files/geo_ref_2002_2011.csv')
geo_ref_1996_2001 = pd.read_csv('reference_files/geo_ref_1996_2001.csv')
geo_ref_1992_1995 = pd.read_csv('reference_files/geo_ref_1992_1995.csv')
geo_ref_1989_1991 = pd.read_csv('reference_files/geo_ref_1989_1991.csv')
geo_ref_1988 = pd.read_csv('reference_files/geo_ref_1988.csv')
geo_ref_1987 = pd.read_csv('reference_files/geo_ref_1987.csv')
geo_ref_1986 = pd.read_csv('reference_files/geo_ref_1986.csv')

geo_dict = {}
geo_dict['2012-2016'] = geo_by_yr(geo_ref_2012_2016)
geo_dict['2002-2011'] = geo_by_yr(geo_ref_2002_2011)
geo_dict['1996-2001'] = geo_by_yr(geo_ref_1996_2001)
geo_dict['1992-2005'] = geo_by_yr(geo_ref_1992_1995)
geo_dict['1989-1991'] = geo_by_yr(geo_ref_1989_1991)
geo_dict['1988'] = geo_by_yr(geo_ref_1988)
geo_dict['1987'] = geo_by_yr(geo_ref_1987)
geo_dict['1987'] = geo_by_yr(geo_ref_1986)
geo_dict['1975-1985'] = geo_by_yr(geo_ref_1986)




with open("all_yr_geo.json", "w") as outfile:
    json.dump(geo_dict, outfile)