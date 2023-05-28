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


# write the data to a sqlite table
#users.to_sql('data_data', conn, if_exists='append', index = False)

#print(data[0][0])

for i,data in enumerate(data_all):
    date=data[0].split('/')
    num=str(i)
    week='20'+str(date[2])+'-'+str(date[0])+'-'+str(date[1])
    sku=str(data[1])
    weekly_sales=str(data[2])
    EV=str(data[3])
    color=str(data[4])
    price=str(data[5])
    vendor=str(data[6])
    function=data[7]

    #print(week,sku,weekly_sales,EV,color,price+vendor,function)


    sql = ''' INSERT INTO data_data(number,week,sku,weekly_sales,EV,color,price,vendor,functionality)
                 VALUES('''+'"'+num+'"'+''','''+'"'+week+'"'+''','''+sku+''','''+weekly_sales+''','''+'"' +EV+'"'+''','''+'"'+color+'"'+''','''+price+''','''+vendor+''','''+'"'+function+'"'+''') '''

    c.execute(sql)
    conn.commit()


data=c.execute('''SELECT * FROM data_data''').fetchall() # [(1, 'pokerkid'), (2, 'crazyken')]
print(data)