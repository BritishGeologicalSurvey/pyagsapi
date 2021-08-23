import os.path
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file) 
    except Error as e:
        print(e)
    
    return conn
            
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)
        
def exec_sql(conn, string_sql):
    """ execute sql from string_sql statement
    :param conn: Connection object
    :param string_sql: a sql statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(string_sql)
        conn.commit()
        c.close()
    except Error as e:
        print(e)
        
def insert_dict_vol(conn, group_str, heading_list, unit_list, type_list):
    """ assemble insert statement from lists for dict_vol table
    :param conn: Connection object
    :param group_str: string specifying group/table
    :param heading_list: list of columns/headings
    :param unit_list: list of units to be inserted
    :param type_list: list of types to be inserted
    :return:
    """
    if len(heading_list) == len(unit_list) and len(heading_list) == len(type_list):
        for i in range(0, len(heading_list)):
            insert_str = 'insert into DICT_VOL (DICT_TYPE, DICT_GRP, DICT_HDNG, DICT_UNIT, DICT_DTYP) values ('
            insert_str = insert_str + '"HEADING",' + '"' + group_str + '","' + heading_list[i] + '","' + unit_list[i] + '","' + type_list[i] + '")' 
            exec_sql(conn, insert_str)
    else:
        print('Error! Problem inserting units and types.')
    
	
        
def get_rows(conn, select_sql):
    """
    select using sl supplied
    :param conn: the Connection object
    :select_sql: some select statement
    :return: rows
    """
    rows = []
    try:
        c = conn.cursor()
        c.execute(select_sql)
        rows = c.fetchall()
    except Error as e:
        print(e)
    return rows

def validate_coords(conn):
    """
    validate spatial coords in LOCA group
    :param conn: the Connection object
    :return: result
    """
    result = 0
    try:
        c = conn.cursor()
        sql_str = """SELECT printf("%.2f", B.THECOUNT/A.THECOUNT * 100) AS PERCENTVALID
				FROM
				(SELECT cast(COUNT(*) as real) AS THECOUNT 
				FROM LOCA) A,
				(SELECT cast(COUNT(*) as real) AS THECOUNT 
				FROM 
				(SELECT * FROM LOCA 
                        CROSS JOIN
                        (SELECT NULL AS LOCA_NATE, NULL AS LOCA_NATN)) BB
				WHERE
				LOCA_NATE <> ''
				AND LOCA_NATN <>''
				AND LOCA_NATE <> 0
				AND LOCA_NATN <> 0
				AND cast(LOCA_NATE as decimal) BETWEEN -100000 AND 800000
				AND cast(LOCA_NATN as decimal) BETWEEN -100000 AND 1400000
				) B """
        c.execute(sql_str)
        result  = c.fetchone()[0]
    except Error as e:
        print(e)
    return result
    
def validate_maprefs(conn):
    """
    validate map reference columns in LOCA group

    Check if northing and eastings are the same as the X and Y.  This can happen if lat/lon
    data have been put into the BNG / Eastings / Northings columns.  BGS looks at BNG first.

    GREF should tell you the coordinate system contains "OSGB" or "OSI" or some other code.
    Almost always null.

    :param conn: the Connection object
    :return: result
    """
    result = []
    try:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        sql_str = """SELECT GREF, LREF, LLZ, LOCXEQNATE, LOCYEQNATN
					FROM
					(SELECT
					SUM(
					CASE WHEN 
					LOCA_NATE  <> '' AND LOCA_NATN <> '' 
					AND LOCA_NATE <> 0 AND LOCA_NATN <> 0
					AND LOCA_GREF = '' THEN 1 ELSE 0 END
					) AS GREF,
					SUM(
					CASE WHEN LOCA_LOCX <> '' AND LOCA_LOCY <> '' 
					AND LOCA_LOCX <> 0 AND LOCA_LOCY <> 0
					AND LOCA_LREF = '' THEN 1 ELSE 0 END
					) AS LREF,
					SUM(
					CASE WHEN LOCA_LAT <> '' AND LOCA_LON <> '' 
					AND LOCA_LAT <> 0 AND LOCA_LON <> 0
					AND LOCA_LLZ = '' THEN 1 ELSE 0 END
					) AS LLZ,
					 SUM(
					CASE WHEN LOCA_LOCX <> ''
					AND
					LOCA_LOCX = LOCA_NATE THEN 1 ELSE 0 END
					) AS LOCXEQNATE,
					SUM(
					CASE WHEN LOCA_LOCY <> ''
					AND
					LOCA_LOCY = LOCA_NATN THEN 1 ELSE 0 END
					) AS LOCYEQNATN
					FROM 
					(SELECT * FROM LOCA 
                        CROSS JOIN
                        (SELECT NULL AS LOCA_NATE, NULL AS LOCA_NATN, NULL AS GREF, 
                        NULL AS LREF, NULL AS LLZ, NULL AS HOLE_LOCX, NULL AS HOLE_LOCY,
                        NULL AS LOCA_LTA, NULL AS LOCA_LON)) AA
					) A """
        c.execute(sql_str)
        result = c.fetchone()
    except Error as e:
        print(e)
    return result
    
        
#prompt for file and db name
db_name = input("Choose a name for the database: ")
file_path = input("Submit the file path for the AGS file: ")

#if no file specified, use a default test file (this is for testing)
if file_path == '':
	file_path = 'example4.ags' 

#if specified path is not valid, then exit 
if not os.path.isfile(file_path):
	print(file_path +' is not a valid file path')
	exit()

# create db with appropriate name
database_name = 'AGSdb_' + db_name
 
conn = create_connection(r""+ database_name + ".db")

#initiate some variables
group = ''
heading_list = []
data_list = []

# TODO - probably could insert some metadata in at this point e.g. filename, date etc.

# Open the file with read only permit
f = open(file_path)

# read the first line 
line = f.readline()

# test if file is correct AGS version
if line[:3] == '"**':
	print('This file appears to be AGS version 3.x. Please use the appropriate converter.')
	exit()

print('Attempting to convert file...')

#create dict_vol table to store units and types
create_table_sql = 'CREATE TABLE DICT_VOL(DICT_TYPE text,DICT_GRP text,DICT_HDNG text,DICT_DTYP text,DICT_UNIT text)'
create_table(conn, create_table_sql)

# loop through lines in file
while line:
	# convert line into list of values
	line_list = line[1:-2].split('","')

	if line_list[0] == 'GROUP':
		group = line_list[1]
		group = group.replace('"','')
		#print('Group: ' + group)
		
	if line_list[0] == 'HEADING':
		heading_list = line_list[1:]
		# create table using group and headings
		create_table_sql = 'CREATE TABLE IF NOT EXISTS ' + group + '('
		for c in heading_list:
			create_table_sql = create_table_sql + c + ' text,'
		# trim last comma
		create_table_sql = create_table_sql[:-1]
		create_table_sql = create_table_sql + ');'
		
		if conn is not None:
			# create group table
			create_table(conn, create_table_sql)
		else:
			print("Error! cannot create the database connection.")
	
	if line_list[0] == 'UNIT':
		unit_list = line_list[1:]
	
	if line_list[0] == 'TYPE':
		type_list = line_list[1:]
		insert_dict_vol(conn, group, heading_list, unit_list, type_list)
	
	if line_list[0] == 'DATA':
		data_list = line_list[1:]
		if len(heading_list) == len(data_list):
			# create insert statement
			insert_sql = 'INSERT INTO ' + group + '('
			for c in heading_list:
				insert_sql = insert_sql + c + ','
			insert_sql = insert_sql[:-1]
			insert_sql = insert_sql + ') values ('
			for d in data_list:
				insert_sql = insert_sql + '"' + d +'",'
			insert_sql = insert_sql[:-1]
			insert_sql = insert_sql + ')'
			
			if conn is not None:
				exec_sql(conn, insert_sql)

		else:
			print('Error! Headings/data mismatch.')
			print(data_list)
	
    # read next line
	line = f.readline()
f.close()
print('File converted. Now validating...')

# validation ###################################

# get a list of groups/tables created
select_sql = "select tbl_name from sqlite_master where tbl_name in ('PROJ','LOCA','ABBR','TYPE','UNIT','GEOL','DICT','FILE') "
groups = get_rows(conn, select_sql)

# set default validaation status
validation = 'Passed!'

print('Groups must include PROJ, LOCA, ABBR, TYPE, UNITS (and GEOL for BGS)')
print('FILE is required if the AGS file is submitted with other supporting non-AGS files')
print('DICT is required if any user defined groups or headings are present, otherwise only standard/default settings are used')

if 'PROJ' not in str(groups):
	print('PROJ group missing from file.')
	validation = 'Failed.'
if 'LOCA' not in str(groups):
	print('LOCA group missing from file.')
	validation = 'Failed.'
if 'ABBR' not in str(groups):
	print('ABBR group missing from file.')
	validation = 'Failed.'
if 'TYPE' not in str(groups):
	print('TYPE group missing from file.')
	validation = 'Failed.'
if 'UNIT' not in str(groups):
	print('UNIT group missing from file.')
	validation = 'Failed.'
if 'GEOL' not in str(groups):
	print('GEOL group missing from file.')
	validation = 'Failed.'
if 'DICT' not in str(groups):
	print('DICT group missing from file.')
if 'FILE' not in str(groups):
	print('FILE group missing from file.')
	
# validate BNG coords - TODO - expand to lat/lon?
valid_coords = validate_coords(conn)
print('Precentage of valid BNG coordinates: ' + str(valid_coords) + '%')
print('Pass is greater than 75%')
if float(valid_coords) < 75:
	validation = 'Failed.'

#check for map references and warn if missing
valid_maprefs = validate_maprefs(conn)

if valid_maprefs['GREF'] > 0:
	print('Warning: National Grid coordinates appear to be present with no GREF (referencing system) specified')
if valid_maprefs['LREF'] > 0:
	print('Warning: local grid coordinates appear to be present with no LREF (referencing system) specified')
if valid_maprefs['LLZ'] > 0:
	print('Warning: LAT/LON coordinates appear to be present with no LLZ (projection format) specified')
#fail if coords appear untranslated
if valid_maprefs['LOCXEQNATE'] > 0 or valid_maprefs['LOCYEQNATN'] > 0:
	print('Warning: it appears that some BNG coordinates are the same as the local coordinates, which suggests that they have not been translated')
	validation = 'Failed.'

#############################################
print('-----------------------------------')
print('File validation status: ' + validation)
	
	
	
