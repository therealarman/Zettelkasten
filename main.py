import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = 'C:/Users/Arman/Downloads'

files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
folders = [f for f in os.listdir(directory) if not os.path.isfile(os.path.join(directory, f))]

df = pd.DataFrame(columns=['Title', 'Type'])

for _file in files:
    splFile = os.path.splitext(_file)

    new_row = pd.Series({'Title' : splFile[0], 'Type': splFile[1]})

    df = pd.concat([
                df, 
                pd.DataFrame([new_row], columns=new_row.index)]
           ).reset_index(drop=True)

print(df.head())

# df.to_csv('Downloads.csv', index=False)