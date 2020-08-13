import pandas as pd
import os

# PATH_TO_DATABASE kept internal
os.chdir(PATH_TO_DATABASE)

db_file = 'energy_estimate_database.xlsx'
energy_estimates_folder = 'Reviewed Energy Estimates'
error_folder = 'Error'

def compile_energy_estimates():
  db = get_database(db_file)
  energy_estimates = get_energy_estimates_from_folder(energy_estimates_folder)
  updated_db = add_energy_estimates_to_db(db, energy_estimates)
  formatted_db = format_database(updated_db)
  save_database(formatted_db, db_file)
  
def get_database(db_file):
  if os.path.exists(db_file):
    print('Opening ' + db_file)
    db = open_database(db_file)
  else:
    print('No database found.  Creating one.')
    db = create_database()
  return db
  
def open_database(db_file):
  db = pd.read_excel(db_file, dtype='object')
  db = db.iloc[:,1:] # remove index column
  return db
  
def create_database():
  db = pd.DataFrame()
  return db
  
def get_energy_estimates_from_folder(energy_estimates_folder):
  files = os.listdir(energy_estimates_folder)
  print("Energy Estimates to be uploaded:" + str(files))
  energy_estimate_file_paths = [energy_estimates_folder + '/' + file for file in files]
  return energy_estimate_file_paths
  
def add_energy_estimates_to_db(db, energy_estimate_files):
  for energy_estimate in energy_estimate_files:
    print('Reading ' + energy_estimate)
    try:
      df = pd.read_excel(energy_estimate, dtype='object')
      df = format_df(df)
      db = pd.concat([db, df], sort = False)
    except:
      print('An error occurred.  Moving ' + energy_estimate + ' to Error Folder.')
      destination = energy_estimate.replace(energy_estimates_folder, error_folder)
      os.rename(energy_estimate, destination)
      continue
  return db
  
def format_df(df):
  df = df.iloc[:, 1:3].dropna() # pull out correct columns
  df = df.set_index('Unnamed: 1') # Make variable names the index
  df = df.transpose() # Now var names are column names and values in 1 row (Wide Format)
  df = add_sh_prefix(df) # Add SH_ as prefix to all duplicate columns due to Safe Harbor modeling
  return df
  
def add_sh_prefix(df):
  cols=pd.Series(df.columns)
  for dup in cols[cols.duplicated()].unique(): 
    cols[cols[cols == dup].index.values.tolist()] = ['SH_' + dup if i != 0 else dup for i in range(sum(cols == dup))]
  df.columns = cols
  return df
  
def format_database(db):
  database = db.reset_index(drop = True).drop_duplicates(keep = 'first')
  return database
    
def save_database(db, file_path):
  print('Saving ' + file_path)
  db.to_excel(file_path)

if __name__== "__main__":
  compile_energy_estimates()
