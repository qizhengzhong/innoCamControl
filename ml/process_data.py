import pandas as pd
import numpy as np
import os

def evaluation():

    #print('path----------------------------------',os.getcwd())
    #sales = pd.read_csv("ml/data/data_processed.csv")
    res = pd.read_csv('ml/data/results.csv')


    results=pd.DataFrame()
    results['model']=res.columns
    results['OOS R2']=res.values.tolist()[0]
    results['method-type']=['Traditional','Traditional','Traditional','Traditional','Traditional','Traditional','Traditional',
                     'Tree-based','Tree-based','Tree-based','Tree-based','Tree-based','Tree-based',
                     'Clustering','Clustering']

    

    #import matplotlib.pyplot as plt
    #import seaborn as sns

    #plt.rcParams.update({'font.size': 15})

    #fig, ax = plt.subplots(figsize=(20,8))

    #g = sns.barplot(data=results, x='model', y='OOS R2', ax=ax, hue='method-type', palette='dark', dodge=False)
    #ax.set_ylabel('OOS $R^2$', size = 14)
    #ax.set_xticklabels(list(res.columns),rotation=45,ha='right')

    #ax.set_ylim([0,0.8])
    #ax.yaxis.grid(True)
    #plt.xticks(size = 15)
    #plt.yticks(size = 15)
    #plt.savefig("results_plot.png",dpi=400,bbox_inches = 'tight')
    #plt.show()


    return list(results['OOS R2']), list(results['model'])


def predict():

    #print('path----------------------------------',os.getcwd())
    sales = pd.read_csv("ml/data/data_processed.csv")
    #res = pd.read_csv('ml/data/results.csv')

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

    raw_list=list(data.iloc[:68]["week"])
    #for raw in data.iloc[:68]["week"]:
    #    raw_list.append(raw)


    predict_list=list(data.iloc[68:]["week"])
    #for pre in data.iloc[68:]["week"]:
    #    predict_list.append(pre)

    return raw_list,predict_list,list(y_train_primer),list(y_test_primer),list(y_pred_primer)


    #plt.rcParams.update({'font.size': 10})
    #plt.title('Weekly sales SKU 11')
    #plt.ylabel("Sales")
    #plt.plot(raw_list,y_train_primer,label="Actual Sales (Training)",color=sns.color_palette(palette='colorblind')[3])
    #plt.plot(predict_list,y_test_primer,label="Actual Sales (Testing)",color=sns.color_palette(palette='colorblind')[2],linestyle="dotted")
    #plt.plot(predict_list,y_pred_primer,color=sns.color_palette(palette='colorblind')[1],label="Predicted Sales",linestyle='dashdot')
    #plt.legend(loc='upper right',fontsize='small')
    #plt.ylim([0,400])
    #locs, labels=plt.xticks()
    #x_ticks = []
    #plt.xticks(locs[2::10],data.week[2::10], rotation=30)
    #plt.show()


def read_churn():
    with open('ml/data/churn.txt') as f:
        lines = f.readlines()
        
        x1=[]
        y1=[]
        for line in lines:
            a,b=line.strip().split(' ')
            x1.append(int(a))
            y1.append(int(b))

        #print(x1)
        #print(y1)

        return x1[0:200],y1[0:200],x1[200:],y1[200:]


