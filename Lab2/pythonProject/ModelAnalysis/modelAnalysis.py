from sklearn.metrics import mean_squared_error

def evaluateModel(y_test, x_test, y_pred, model):
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2_score = model.score(x_test, y_test)
    print('Root Means Square Error = ', rmse)
    print(f"R² Score: {r2_score}")
