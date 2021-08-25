# coding: utf-8

from python_ags4 import AGS4
tables, headings = AGS4.AGS4_to_dataframe('test/files/example1.ags')
tables
type(tables)
tables.keys()
'GEOL' in tables.keys()
headings
headings.keys()
headings['PROJ'].keys()
headings['PROJ']
tables['PROJ'].columns
loca = tables['LOCA']
loca
loca = AGS4.convert_to_numeric(tables['LOCA'])
loca
loca.dtypes()
loca.dtypes
loca
10000 <= loca['LOCA_NATE'] < 1e9
10000 <= loca['LOCA_NATE']
10000 <= loca['LOCA_NATE'] and loca['LOCA_NATE'] > 1e9
10000 <= loca['LOCA_NATE']
tables['ABBR']
loca
loc
loca
for col in ['LOCA_GREF', 'LOCA_LREF', 'LOCA_LLZ']:
    print(loca[col])
    
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/A9093.ags')
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/19684.ags')
loca = AGS4.convert_to_numeric(tables['LOCA'])
tables.keys()
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/19684.ags')
tables
headings
tables, headings = AGS4.AGS4_to_dataframe('test/files/example1.ags')
tables
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/19684.ags')
errors = AGS4.AGS4_check_file('test/files/real/19684.ags')
errors = AGS4.check_file('test/files/real/19684.ags')
errors
errors = AGS4.check_file('test/files/real/JohnStPrimarySchool.ags')
errors = AGS4.check_file('test/files/real/Blackburn Southern Bypass.ags')
errors = AGS4.check_file('test/files/real/43370.ags')
errors
loca = AGS4.convert_to_numeric(tables['LOCA'])
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/43370.ags')
loca = AGS4.convert_to_numeric(tables['LOCA'])
loca
loca.describe()
for col in ['LOCA_GREF', 'LOCA_LREF', 'LOCA_LLZ']:
    print(loca[col])
    
for col in ['LOCA_GREF', 'LOCA_LREF', 'LOCA_LLZ']:
    try:
        print(loca[col])
    except KeyError:
        print(f'{col} not found')
    
loca['LOCA_NATE'] > 1e5
loca['LOCA_NATE'] < 8 * 1e5
loca['LOCA_NATN'] > 1e5
loca['LOCA_NATN'] < 14 * 1e5
loca['LOCA_LAT']
loca['LOCA_LAT'] > -90
loca['LOCA_LAT'] < 90
loca['LOCA_LON] > -180
loca['LOCA_LON'] > -180
loca['LOCA_LON'] < 180
tables.keys()
tables['HDPH']
hole_depth = AGS4.convert_to_numeric(tables['HDPH'])
hole_depth
import numpy as np
np.isnan(hole_depth['HDPH_TOP'])
all(np.isnan(hole_depth['HDPH_TOP']))
all(np.isnan(hole_depth['HDPH_BASE']))
not all(np.isnan(hole_depth['HDPH_TOP']))
not all(np.isnan(hole_depth['HDPH_BASE']))
tables['GEOL']
hole_depth['LOCA_ID'].unique
hole_depth['LOCA_ID'].unique()
geology = AGS4.convert_to_numeric(tables['GEOL'])
geology['LOCA_ID'].unique()
geology['LOCA_ID'].unique() == hole_depth['LOCA_ID'].unique()
all(geology['LOCA_ID'].unique() == hole_depth['LOCA_ID'].unique())
set(geology['LOCA_ID'].unique()) == set(hole_depth['LOCA_ID'].unique())
'LOCA' in tables.keys() or 'HOLE' in tables.keys()
tables.keys()
get_ipython().run_line_magic('save', '0-82 validation_session.py')
get_ipython().run_line_magic('save', '')
get_ipython().run_line_magic('save', 'validation_session.py 0-82')
len(tables['PROJ']) - 3
tables['PRIJ']
tables['PROJ']
len(tables['PROJ']) - 2
len(tables['LOCA']) - 2
len(tables.keys())
project_count = len(tables['PROJ']) - 2
borehole_count = len(tables['LOCA']) - 2
groups_count = len(tables.keys())
get_ipython().system('grep -r test/files/real/ SAMP')
get_ipython().system('grep "SAMP" -r test/files/real/')
get_ipython().system('grep "SAMP_ID" -r test/files/real/')
get_ipython().system('grep "SAMP_ID" -f -r test/files/real/')
get_ipython().system('grep "SAMP_ID" -l  -r test/files/real/')
tables, headings = AGS4.AGS4_to_dataframe('test/files/real/Docklands Light Railway Woolwich Extension.ags')
tables.keys()
samples = AGS4.convert_to_numeric(tables['SAMP'])
samples
samp.columns()
samples.columns
samples['SAMP_ID']
samples['SAMP_ID'][:10]
samples
samples.loc['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']
samples[['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']]
samples[['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']].apply(np.isnan)
samples[['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']].df_apply(np.isnan)
samples[['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']]
sample_info = samples[['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']]
sample_info.unique()
get_ipython().run_line_magic('pinfo', 'sample_info.apply')
sample_info.apply(print)
sample_info.apply(print, axis=1)
sample_info
sample_info.to_string()
sample_info.to_records()
sample_info.to_records().unique()
set(sample_info.to_records())
sample_info.to_records()
sample_info.to_records().tolist()
get_ipython().run_line_magic('pinfo', 'sample_info.to_records')
sample_info.to_records(index=False)
sample_info.to_records(index=False).tolist()
set(sample_info.to_records(index=False).tolist())
len(set(sample_info.to_records(index=False).tolist()))
samples_are_unique = len(set(sample_info.to_records(index=False).tolist())) == len(sample_info.to_records(index=False).tolist())
samples_are_unique
samples['LOCA_ID']
set(samples['LOCA_ID'])
samples
loca = AGS4.convert_to_numeric(tables['LOCA'])
loca
loca.columns
set(samples['LOCA_ID']).issubset(set(loca['LOCA_ID']))
all_samples_have_locations = set(samples['LOCA_ID']).issubset(set(loca['LOCA_ID']))
sample_unique_groups = ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']
tables.keys()
potential_sample_children = ['CMPG', 'CMPT', 'CONG', 'CONS']
tables['CMPG']
cmpg = AGS4.convert_to_numeric(tables['CMPG'])
# check all tables to see if they have SAMP_ID or the other four columns, based on what is in the SAMP table
# if a table has those columns, then check that a collection of values is a subset of those in the SAMP table
get_ipython().run_line_magic('save', 'validation_session.py 0-147')
