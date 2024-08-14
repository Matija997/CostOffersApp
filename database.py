import sqlite3


def get_connection(db_name='data.db'):

    return sqlite3.connect(db_name)


def create_table(conn, table_name):

    query = f'''CREATE TABLE IF NOT EXISTS {table_name}
        (material_part_designation TEXT, designation_raw TEXT,
        imputed_costs NUMERIC,
        number_part NUMERIC, material_scrap NUMERIC,
        manufacturing_part_designation TEXT,
        direct_manufacturing_costs NUMERIC,
        manufacturing_costs NUMERIC, scrap_per_process NUMERIC,
        billing_method TEXT, inputed_device_cost NUMERIC,
        total_material NUMERIC)
    '''
    conn.execute(query)


def insert_data(table_name):

    data_insert_query = f'''INSERT INTO {table_name}
        (material_part_designation, designation_raw, imputed_costs,
        number_part, material_scrap, manufacturing_part_designation,
        direct_manufacturing_costs, manufacturing_costs, scrap_per_process,
        billing_method, inputed_device_cost, total_material) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    return data_insert_query
