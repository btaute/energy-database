import pandas as pd
import os

# PATH_TO_DATABASE kept internal
os.chdir(PATH_TO_DATABASE)

from compile_energy_estimates import *

table_file = 'energy_estimate_table.xlsx'

def update_energy_estimate_table():
  db = get_database(db_file)
  db = format_database(db)
  db = consolidate_variables_with_different_names(db)
  db = sort_database(db)
  save_energy_estimate_table(db, table_file)
  
def consolidate_variables_with_different_names(database):
  db = database
  db = merge_columns(db, 'Project Variant/Run Notes', 'Run Notes')
  db = merge_columns(db, 'Module Modeled', 'Module Model')
  return db
  
def merge_columns(db, primary_col, secondary_col):
  db[primary_col] = db[primary_col].fillna(db[secondary_col])
  db = db.drop(secondary_col, axis = 1)
  return db

def sort_database(db):
  db = db.sort_values(by=['Project Name', 'Run Date'], ascending=[True, False])
  return db

def save_energy_estimate_table(db, file_path):
  print('Saving ' + file_path)
  db.to_excel(file_path)
  
if __name__== "__main__":
  update_energy_estimate_table()
