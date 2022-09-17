import pandas as pd
import numpy as np
import website_util as ut

geo_ref_2012_2016 = pd.read_csv('reference_files/geo_ref_2012_2016.csv')
geo_ref_2002_2011 = pd.read_csv('reference_files/geo_ref_2002_2011.csv')
geo_ref_1996_2001 = pd.read_csv('reference_files/geo_ref_1996_2001.csv')
geo_ref_1992_1995 = pd.read_csv('reference_files/geo_ref_1992_1995.csv')
geo_ref_1989_1991 = pd.read_csv('reference_files/geo_ref_1989_1991.csv')
geo_ref_1988 = pd.read_csv('reference_files/geo_ref_1988.csv')
geo_ref_1987 = pd.read_csv('reference_files/geo_ref_1987.csv')
geo_ref_1986 = pd.read_csv('reference_files/geo_ref_1986.csv')


naics_ref_2012_2016 = pd.read_csv('reference_files/naics_2012_2016.csv')
naics_ref_2008_2011 = pd.read_csv('reference_files/naics_2008_2011.txt', delimiter = '  ')
naics_ref_2003_2007 = pd.read_csv('reference_files/naics_2003_2007.txt', delimiter = '  ')
naics_ref_1998_2002 = pd.read_csv('reference_files/naics_1998_2002.txt', delimiter = '  ')
naics_ref_1988_1997 = pd.read_csv('reference_files/naics_1988_1997.txt', delimiter = '  ')
naics_ref_1987 = pd.read_csv('reference_files/naics_1987.txt', delimiter = '    ')
naics_ref_1986 = pd.read_csv('reference_files/naics_1986.txt', delimiter = '    ')

def save_readable(year):
    df = pd.read_csv(f'data/efsy_cbp_{year}.csv')
    
    if year >= 2012:
        naics_ref = naics_ref_2012_2016
    elif 2008 <= year < 2012:
        naics_ref = naics_ref_2008_2011
    elif 2003 <= year < 2008:
        naics_ref = naics_ref_2003_2007
    elif 1998 <= year < 2003:
        naics_ref = naics_ref_1998_2002
    elif 1988 <= year < 1998:
        naics_ref = naics_ref_1988_1997
    elif year == 1987:
        naics_ref = naics_ref_1987
    elif year == 1986:
        naics_ref = naics_ref_1986
    else: print('year not currently supported for naics')
        
    if year >= 2012:
        geo_ref = geo_ref_2012_2016
    elif 2002 <= year < 2012:
        geo_ref = geo_ref_2002_2011
    elif 1996 <= year < 2002:
        geo_ref = geo_ref_1996_2001
    elif 1992 <= year < 1996:
        geo_ref = geo_ref_1992_1995
    elif 1989 <= year < 1992:
        geo_ref = geo_ref_1989_1991
    elif year == 1988:
        geo_ref = geo_ref_1988
    elif year == 1987:
        geo_ref = geo_ref_1987
    elif year == 1986:
        geo_ref = geo_ref_1986
    else: print('year not currently supported for geo')
    
    
    read = ut.make_readable(df,
                 geo_ref, naics_ref)
    
    read.groupby('ctyname').apply(ut.make_percent).to_csv(
        f'readable/cbp_{year}.csv', index = False
        )

years = [i for i in range(1986, 2017)]
for year in years:
    try:
        save_readable(year)
    except Exception as e:
        print((e, year))