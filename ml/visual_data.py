import pandas as pd
import numpy as np

sales = pd.read_csv("data/data_processed.csv")

res = pd.read_csv('data/results.csv')


results=pd.DataFrame()
results['model']=res.columns
results['OOS R2']=res.values.tolist()[0]
results['method-type']=['Traditional','Traditional','Traditional','Traditional','Traditional','Traditional','Traditional',
                 'Tree-based','Tree-based','Tree-based','Tree-based','Tree-based','Tree-based',
                 'Clustering','Clustering']


import matplotlib.pyplot as plt
import seaborn as sns


data = sales[sales.sku==11].sort_values(by=["week"])
colnames = [i for i in data.columns if i not in ["week","weekly_sales","sku"]]


X_primer = data[colnames]
y_primer = data.weekly_sales

X_train_primer,X_test_primer = np.split(X_primer, [int(0.70 *98)])
y_train_primer, y_test_primer = np.split(y_primer, [int(0.70 *98)])


from statsmodels.regression.linear_model import OLS
model = OLS(y_train_primer, X_train_primer)
model = model.fit()
y_pred_primer = list(model.predict(X_test_primer))



plt.rcParams.update({'font.size': 10})

plt.title('Weekly sales SKU 11')
plt.ylabel("Sales")

raw_list=[]
for raw in data.iloc[:68]["week"]:
    print('raw',raw)
    raw_list.append(raw)


predict_list=[]
for pre in data.iloc[68:]["week"]:
    predict_list.append(pre)



print('y_train_primer',len(y_train_primer))

plt.plot(raw_list,y_train_primer,label="Actual Sales (Training)",color=sns.color_palette(palette='colorblind')[3])
plt.plot(predict_list,y_test_primer,label="Actual Sales (Testing)",color=sns.color_palette(palette='colorblind')[2],linestyle="dotted")
plt.plot(predict_list,y_pred_primer,color=sns.color_palette(palette='colorblind')[1],label="Predicted Sales",linestyle='dashdot')

plt.legend(loc='upper right',fontsize='small')

plt.ylim([0,400])
locs, labels=plt.xticks()
x_ticks = []
plt.xticks(locs[2::10],data.week[2::10], rotation=30)


plt.show()

