#imports
from DataCollection import datacollection
from DataVerification import dataVerification, dataCleaning
from MachineLearning import machineLearning
from ModelAnalysis import modelAnalysis

#data collection
path = 'Extended_Employee_Performance_and_Productivity_Data.csv'
df = datacollection.gatherData(path)

#displaying data verification
dataVerification.verifyData(df)

# Data cleaning/Encoding Categorical Variables/Scaling values in dataset
df = dataCleaning.dropColumns(df, ['Employee_ID', 'Hire_Date'])

df = dataCleaning.encodingData(df, ['Department', 'Gender', 'Job_Title', 'Education_Level'])

df = dataCleaning.addRatio(df, 'Overtime_Ratio', 'Overtime_Hours', 'Work_Hours_Per_Week')

# Feature and Target Variable Selection

x,y = machineLearning.praperSets(df, 'Employee_Satisfaction_Score')
x_train, x_test, y_train, y_test = machineLearning.splitData(x, y, 0.7, 42)


# Linear Regression Model training and evaluation
lin_reg = machineLearning.trainLinearRegression(x_train, y_train)
y_pred = machineLearning.predictLinearRegression(lin_reg, x_test)

# Linear Regression Model evaluation

modelAnalysis.evaluateModel(y_test, x_test, y_pred, lin_reg)


# Decision Tree Regressor Model training and evaluation
regressor = machineLearning.trainDecisionTree(x_train, y_train, 42)
y_pred = machineLearning.predictDecisionTree(regressor, x_test)

# Decision Tree Regressor Model evaluation
modelAnalysis.evaluateModel(y_test, x_test, y_pred, regressor)