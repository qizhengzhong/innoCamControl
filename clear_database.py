import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


import pandas as pd
# load the data into a Pandas DataFrame
users = pd.read_csv('data_raw_truck body.csv')

data_all=users.values.tolist()



sql = 'DELETE FROM data_data'
c.execute(sql)
conn.commit()


data=c.execute('''SELECT * FROM data_data''').fetchall() # [(1, 'pokerkid'), (2, 'crazyken')]
print(data)