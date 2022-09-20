import pandas as pd
import numpy as np
import json

def sectors_by_yr(df):
    all_sec = df['DESCRIPTION'].unique()
    return [{'value': sec, 'label': sec} for sec in all_sec]
    

naics_ref_2012_2016 = pd.read_csv('reference_files/naics_2012_2016.csv')
naics_ref_2008_2011 = pd.read_csv('reference_files/naics_2008_2011.txt', delimiter = '  ')
naics_ref_2003_2007 = pd.read_csv('reference_files/naics_2003_2007.txt', delimiter = '  ')
naics_ref_1998_2002 = pd.read_csv('reference_files/naics_1998_2002.txt', delimiter = '  ')
naics_ref_1988_1997 = pd.read_csv('reference_files/naics_1988_1997.txt', delimiter = '  ')
naics_ref_1987 = pd.read_csv('reference_files/naics_1987.txt', delimiter = '    ')
naics_ref_1986 = pd.read_csv('reference_files/naics_1986.txt', delimiter = '    ')
naics_ref_1975_1985 = pd.read_csv('reference_files/naics_1975_1985.txt', delimiter = '    ')

sec_dict = {}
sec_dict['2012-2016'] = sectors_by_yr(naics_ref_2012_2016)
sec_dict['2008-2011'] = sectors_by_yr(naics_ref_2008_2011)
sec_dict['2003-2007'] = sectors_by_yr(naics_ref_2003_2007)
sec_dict['1998-2002'] = sectors_by_yr(naics_ref_1998_2002)
sec_dict['1988-1997'] = sectors_by_yr(naics_ref_1988_1997)
sec_dict['1987'] = sectors_by_yr(naics_ref_1987)
sec_dict['1986'] = sectors_by_yr(naics_ref_1986)
sec_dict['1975-1985'] = sectors_by_yr(naics_ref_1975_1985)

with open("all_yr_sectors.json", "w") as outfile:
    json.dump(sec_dict, outfile)