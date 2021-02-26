#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Create custom scaler
from sklearn.base import BaseEstimator, TransformerMixin

# create the Custom Scaler class

class CustomScaler(BaseEstimator,TransformerMixin): 
    
    # init or what information we need to declare a CustomScaler object
    # and what is calculated/declared as we do
    
    def __init__(self,columns,copy=True,with_mean=True,with_std=True):
        
        # scaler is nothing but a Standard Scaler object
        self.scaler = StandardScaler(copy,with_mean,with_std)
        # with some columns 'twist'
        self.columns = columns
        self.mean_ = None
        self.var_ = None
        
    
    # the fit method, which, again based on StandardScale
    
    def fit(self, X, y=None):
        self.scaler.fit(X[self.columns], y)
        self.mean_ = np.mean(X[self.columns])
        self.var_ = np.var(X[self.columns])
        return self
    
    # the transform method which does the actual scaling

    def transform(self, X, y=None, copy=None):
        
        # record the initial order of the columns
        init_col_order = X.columns
        
        # scale all features that you chose when creating the instance of the class
        X_scaled = pd.DataFrame(self.scaler.transform(X[self.columns]), columns=self.columns)
        
        # declare a variable containing all information that was not scaled
        X_not_scaled = X.loc[:,~X.columns.isin(self.columns)]
        
        # return a data frame which contains all scaled features and all 'not scaled' features
        # use the original order (that you recorded in the beginning)
        return pd.concat([X_not_scaled, X_scaled], axis=1)[init_col_order]
    
class AbsenteeismModel():

    def __init__(self, model, scaler):
        with open(model,'rb') as model_file, open(scaler,'rb') as scaler_file:
            self.reg = pickle.load(model_file)
            self.scaler = pickle.load(scaler_file)
            self.data = None
            
    def load_and_clean_data(self, file_name):
        data = pd.read_csv(file_name)
        self.saved_data = data.copy()
        data.drop('ID', axis = 1, inplace = True)
        # to preserve the code we've created in the previous section, we will add a column with 'NaN' strings
        # there is no 'Absenteeism Time' in new data
        data['Absenteeism Time in Hours'] = 'NaN'
        
        # drop first to avoid multicolllinearity
        reasons_dummies = pd.get_dummies(data['Reason for Absence'], drop_first = True)
        data = data.join(reasons_dummies)
        
        # Group reasons
        reason_groups = pd.DataFrame()
        reason_groups['Reason_Group_1'] = reasons_dummies.loc[:,1:14].max(axis = 1)
        reason_groups['Reason_Group_2'] = reasons_dummies.loc[:,15:17].max(axis = 1)
        reason_groups['Reason_Group_3'] = reasons_dummies.loc[:,18:21].max(axis = 1)
        reason_groups['Reason_Group_4'] = reasons_dummies.loc[:,22:].max(axis = 1)
        data = pd.concat([data,reason_groups], axis = 1)
        
        data.drop('Reason for Absence', axis = 1, inplace = True)
        
        rearranged_columns = ['Reason_Group_1',
       'Reason_Group_2', 'Reason_Group_3', 'Reason_Group_4', 'Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']
        
        data = data[rearranged_columns]
        
        data['Date'] = pd.to_datetime(data['Date'], format = '%d/%m/%Y')
        data['Month'] = data['Date'].apply(lambda x: x.month)
        data['Day of week'] = data['Date'].apply(lambda x: x.weekday())
        
        data['Education'] = data['Education'].map({1:0, 2:1, 3:1, 4:1})
        
        data.drop('Date', axis = 1, inplace = True)
        
        rearranged_columns = ['Reason_Group_1', 'Reason_Group_2', 'Reason_Group_3',
       'Reason_Group_4', 'Month',
       'Day of week', 'Transportation Expense', 'Distance to Work',
       'Age', 'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']
        
        data = data[rearranged_columns]
        
        # replace the NaN values
        data = data.fillna(value=0)
        
        data = data.drop(['Absenteeism Time in Hours','Day of week',
                          'Daily Work Load Average','Distance to Work'], axis = 1)
        
        # we have included this line of code if you want to call the 'preprocessed data'
        self.data_preprocessed = data.copy()
        
        # we need this line so we can use it in the next functions
        self.data = self.scaler.transform(data)
        
        
    # we need this line so we can use it in the next functions
    def predicted_probability(self):
        if self.data is not None:
            pred = self.reg.predict_proba(self.data)[:,1]
            return pred
        
    # a function which outputs 0 or 1 based on our model
    def predicted_output_category(self):
        if self.data is not None:
            pred_outputs = self.reg.predict(self.data)
            return pred_outputs
        
    # predict the outputs and the probabilities and 
    # add columns with these values at the end of the new data
    def predicted_outputs(self):
        if self.data is not None:
            self.data_preprocessed['Probability'] = self.reg.predict_proba(self.data)[:,1]
            self.data_preprocessed['Prediction'] = self.reg.predict(self.data)
            return self.data_preprocessed

