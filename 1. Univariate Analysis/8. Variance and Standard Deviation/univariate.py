import pandas as pd
import numpy as np
class univariate():
    
    def quanqual(dataset):
        quan = []
        qual = []
        for columnname in dataset.columns:
            if dataset[columnname].dtype == 'O':
                qual.append(columnname)
            else:
                quan.append(columnname)
        return quan, qual

    def frequencyTable(dataset,columnname):
        frequencyTable=pd.DataFrame(columns=['Unique_values','frequency','relative_frequency','cum_rel_frequency'])
        frequencyTable['Unique_values']=dataset[columnname].value_counts().index
        frequencyTable['frequency']=dataset[columnname].value_counts().values
        frequencyTable['relative_frequency']=frequencyTable['frequency']/frequencyTable['frequency'].count()
        frequencyTable['cum_rel_frequency']=frequencyTable['relative_frequency'].cumsum()
        return frequencyTable
        
    def tableDescripe(dataset,quan):
        df=pd.DataFrame(index=['mean','median','mode','Q1:25%','Q2:50%','Q3:75%','99%','Q4:100%','IQR','1.5rule','lesser','greater','min','max','skewness','kurtosis'],columns=quan)
        for columnname in quan:
            #df[columnname]["mean"]=dataset[columnname].mean()
            df.loc["mean",columnname]=dataset[columnname].mean()
            df.loc["median",columnname]=dataset[columnname].median()
            df.loc["mode",columnname]=dataset[columnname].mode()[0]
            df.loc["Q1:25%",columnname]=dataset.describe()[columnname]['25%']
            df.loc["Q2:50%",columnname]=dataset.describe()[columnname]['50%']
            df.loc["Q3:75%",columnname]=dataset.describe()[columnname]['75%']
            df.loc["99%",columnname]=np.percentile(dataset[columnname],99)
            df.loc["Q4:100%",columnname]=dataset.describe()[columnname]['max']
            df.loc["IQR",columnname]=df.loc["Q3:75%",columnname]-df.loc["Q1:25%",columnname]
            df.loc["1.5rule",columnname]=1.5*df.loc["IQR",columnname]
            df.loc["lesser",columnname]=df.loc["Q1:25%",columnname]-df.loc["1.5rule",columnname]
            df.loc["greater",columnname]=df.loc["Q3:75%",columnname]+df.loc["1.5rule",columnname]
            df.loc["min",columnname]=dataset[columnname].min()
            df.loc["max",columnname]=dataset[columnname].max()
            df.loc["skewness",columnname]=dataset[columnname].skew()
            df.loc["kurtosis",columnname]=dataset[columnname].kurtosis()
        return df

    def outliers(quan,df):
        Lesser=[columnname for columnname in quan if df[columnname]["min"] < df[columnname]["lesser"]]
        Greater=[columnname for columnname in quan if df[columnname]["max"] > df[columnname]["greater"]]
        return Lesser,Greater

    def outliers_replace(Lesser,Greater,dataset,df):
        for col in Lesser:
            dataset.loc[dataset[col] < df[col]["lesser"], col]=df[col]["lesser"]
        for col in Greater:
            dataset.loc[dataset[col] > df[col]["greater"], col]=df[col]["greater"]