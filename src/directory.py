import os
import pandas as pd
import numpy as np

class Directory:

    def __init__(self, location: str):
        self.location = location

    def getFiles(self):

        try:
            files = [f for f in os.listdir(self.location) if os.path.isfile(os.path.join(self.location, f))]
            folders = [f for f in os.listdir(self.location) if not os.path.isfile(os.path.join(self.location, f))]
        except FileNotFoundError:
            files = []
            folders = []
            print("Invalid Directory")

        self.fileDf = pd.DataFrame(columns=['Title', 'Type', 'Directory', 'Location', 'ID', 'Tags'])
        # =========================================================================================
        # This dataframe ^ MUST match whatever SQL Table is created to store file information later
        # =========================================================================================

        for _file in files:
            splFile = os.path.splitext(_file)

            full_location = str(self.location + "/" + _file)

            new_row = pd.Series({'Title' : splFile[0], 'Type': splFile[1][1:], 'Directory': self.location, 'Location': full_location})

            self.fileDf = pd.concat([
                        self.fileDf, 
                        pd.DataFrame([new_row], columns=new_row.index)]
                ).reset_index(drop=True)
            
        self.folderSeries = pd.Series(folders)
            
        return [self.fileDf, self.folderSeries]