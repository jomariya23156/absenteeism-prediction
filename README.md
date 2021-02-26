# absenteeism-prediction
Absenteeism is the behavior that ones are absent during the working time. In this case, we are trying to predict whether ones will have excessive absenteeism or not.  
From our dataset Absenteeism_data.csv, there is a column named 'Absenteeism Time in Hours'. We will use this as labels for our model.  
After we find the mean of the 'Absenteeism Time in Hours', we get a mean of 3. So, we convert all value larger than 3 to be 1 and 0 otherwise.  
If the label is 1, it means that person is likely to be excessive absenteeism and vice versa.  

### Files explanation:  
Data: - Absenteeism_data.csv is the main data before preprocessing  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Absenteeism_preprocessed.csv is the main data after preprocessing  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Absenteeism_new_data.csv is the data for final testing  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Absenteeism_new_data_prediction.csv is the tested data with added prediction column for using in Tableau  
Pickle: - absenteeism_model.pickle for prediction model  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- custom_scaler.pickle for scaling the new data before put in the model  
Database: - db_table_creation.sql for creating the table and columns in the database  
IPynb and Py: - Main for all coding part and name after what that file does

### The processes here:  
1) Preprocess Data  
2) Create the Logistic Regression model and make prediction
3) Export the result to SQL and save as a .csv file
4) Visualize the result in Tableau and integrate the result

### Libraries used:
numpy, pandas, sklearn, pickle, pymysql
