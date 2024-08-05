import os
import pandas as pd
import numpy as np
import traceback
import sqlite3

from globals import ZETTLE_FOLDER

class Library():
    
    def __init__(self):
        self.current_dir: str = None
        self.dataframe: pd.DataFrame = None
        self.conn = None

    def create_library(self, path: str) -> int:

        path = os.path.normpath(path).rstrip("\\")
        
        try:
            self.clear_variables()
            self.current_dir = path
            self.create_library_files()
            self.save_library()
            self.open_library(self.current_dir)
        except:
            traceback.print_exc()
            return 2

        return 0
    
    def clear_variables(self):
        self.current_dir: str = None
        self.dataframe: pd.DataFrame = pd.DataFrame(columns=['Title', 'Type', 'Directory', 'Location', 'ID', 'Tags'])

    def create_library_files(self):

        folder_path = os.path.normpath(f"{self.current_dir}/{ZETTLE_FOLDER}")
        # self.lib = Library()

        cur = self.conn.cursor()
        cur.execute('INSERT INTO libraries (path) VALUES (?)', (self.current_dir,))
        self.conn.commit()
        cur.close()

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

    def save_library(self):

        self.dataframe.to_csv(f"{self.current_dir}/{ZETTLE_FOLDER}/zk_library.csv", encoding='utf-8')


        cur = self.conn.cursor()
        cur.execute('SELECT id FROM libraries WHERE path = ?', (self.current_dir,))
        library_id = cur.fetchone()[0]

        for _, row in self.dataframe.iterrows():
            name = row['Title']
            type = row['Type']
            path = row['Location']

            cur.execute('SELECT id FROM files WHERE library_id = ? AND path = ? AND name = ?', (library_id, path, name))
            result = cur.fetchone()

            if result:
                cur.execute('UPDATE files SET name = ?, type = ? WHERE id = ?', (name, type, result[0]))
            else:
                cur.execute('INSERT INTO files (library_id, name, type, path) VALUES (?, ?, ?, ?)', (library_id, name, type, path))

        self.conn.commit()
        cur.close()

        # if os.path.exists(f"{self.current_dir}/{ZETTLE_FOLDER}/zk_library.csv"):
        #     self.dataframe.to_csv(f"{self.current_dir}/{ZETTLE_FOLDER}/zk_library.csv", encoding='utf-8')
        # else:
        #     print("Save location has been obstructed")
        #     # TODO: Prompt user to give new save location
    
    def open_library(self, path):

        path = os.path.normpath(path).rstrip("\\")

        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM libraries WHERE path = ?', (path,))
        library_exists = cur.fetchone()[0]

        if library_exists:

            cur.execute('SELECT id FROM libraries WHERE path = ?', (path,))
            library_id = cur.fetchone()[0]
            cur.close()

            self.dataframe = self.push_to_df(library_id)

            return 1

            # self.current_dir = path
            # library_path = os.path.normpath(f"{path}/{ZETTLE_FOLDER}/zk_library.csv")

            # if os.path.exists(library_path):
            #     try:     
            #         with open(library_path, 'r', encoding='utf-8') as lib_file:
            #             self.dataframe = pd.read_csv(lib_file, encoding='utf-8')
            #             return 1
            #     except:
            #         traceback.print_exc()

            # return 2
        else:
            cur.close()
            return 3
    
    def populate_library(self):

        files = [f for f in os.listdir(self.current_dir) if os.path.isfile(os.path.join(self.current_dir, f))]
        folders = [f for f in os.listdir(self.current_dir) if not os.path.isfile(os.path.join(self.current_dir, f))]

        # self.dataframe: pd.DataFrame = pd.DataFrame(columns=['Title', 'Type', 'Directory', 'Location', 'ID', 'Tags'])
        # library_df = pd.DataFrame(columns=['Title', 'Type', 'Directory', 'Location', 'ID', 'Tags'])

        cur = self.conn.cursor()
        cur.execute('SELECT id FROM libraries WHERE path = ?', (self.current_dir,))
        library_id = cur.fetchone()[0]

        for _file in files:
            splFile = os.path.splitext(_file)
            full_location = str(f"{self.current_dir}/{_file}")

            cur.execute('SELECT id FROM files WHERE library_id = ? AND path = ?', (library_id, full_location))
            result = cur.fetchone()

            if result:
                cur.execute('UPDATE files SET name = ?, type = ? WHERE id = ?', (splFile[0], splFile[1][1:], result[0]))
            else:
                cur.execute('INSERT INTO files (library_id, name, type, path) VALUES (?, ?, ?, ?)', (library_id, splFile[0], splFile[1][1:], full_location))

            self.conn.commit()

            # new_row = pd.Series({'Title' : splFile[0], 'Type': splFile[1][1:], 'Directory': self.current_dir, 'Location': full_location})

            # library_df = pd.concat([
            #             library_df, 
            #             pd.DataFrame([new_row], columns=new_row.index)]
            #     ).reset_index(drop=True)
        
        # self.dataframe = library_df

        cur.close()
        self.dataframe = self.push_to_df(library_id)

    def query_lib(self, query):
        print(query)

    def push_to_df(self, library_id):

        cur = self.conn.cursor()
        cur.execute('SELECT * FROM files WHERE library_id = ?', (library_id,))

        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        
        cur.close()

        df.rename(columns={
            'id': 'File ID',
            'library_id': 'Library ID',
            'name': 'Title',
            'type': 'Type',
            'path': 'Location'
        }, inplace=True)

        return df

