import pandas as pd
import os

# PATH_TO_DATABASE kept internal
os.chdir(PATH_TO_DATABASE)

from compile_energy_estimates import *
from update_energy_estimate_table import *

def update_database():
  compile_energy_estimates()
  update_energy_estimate_table()
  move_energy_estimates_to_folder('Archive')
  
def move_energy_estimates_to_folder(destination_folder):
  source = get_energy_estimates_from_folder(energy_estimates_folder)
  destination = [file.replace(energy_estimates_folder, destination_folder) for file in source]
  for i in range(len(source)):
    os.rename(source[i], destination[i])
    
if __name__ == "__main__":
  update_database()
