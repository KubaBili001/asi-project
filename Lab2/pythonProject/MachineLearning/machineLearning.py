from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
def praperSets(df, label_name):
    y = df[label_name]
    x = df.drop(label_name, axis=1)
    y.head()
    x.head()
    return x, y

def splitData(x, y, train_size, random_state):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=train_size, random_state=random_state)
    return x_train, x_test, y_train, y_test

def trainLinearRegression(x_train, y_train):
    lin_reg = LinearRegression()
    lin_reg.fit(x_train, y_train)
    return lin_reg

def predictLinearRegression(lin_reg, x_test):
    y_pred = lin_reg.predict(x_test)
    return y_pred

def trainDecisionTree(x_train, y_train, random_state):
    regressor = DecisionTreeRegressor(random_state=random_state)
    regressor.fit(x_train, y_train)
    return regressor

def predictDecisionTree(regressor, x_test):
    y_pred = regressor.predict(x_test)
    return y_pred

