from os              import system
from pandas          import read_csv, to_numeric
from sklearn         import linear_model
from sklearn.metrics import mean_squared_error
from statsmodels.api import OLS, add_constant


system("clear")

data = read_csv("cyberpuerta.csv")

data = data[data.proccessor       != "Not found"]
data = data[data.proccessor_turbo != "Not found"]

data["proccessor"]       = to_numeric(data["proccessor"])
data["proccessor_turbo"] = to_numeric(data["proccessor_turbo"])
#print(data.info())

x = data[["size", "proccessor", "proccessor_turbo", "ram", "hdd"]]
y = data["price"]

regr = linear_model.LinearRegression()
regr.fit(x, y)


print("Intercept: ", regr.intercept_)
print("Coeff: ", regr.coef_)
print("Score: ", regr.score(x,y))

new_size             = 15.6
new_proccessor       = 1.6
new_proccessor_turbo = 3.9
new_ram              = 12
new_hdd              = 1250 

predicted = regr.predict([[new_size, new_proccessor, new_proccessor_turbo, new_ram, new_hdd]])
print("Predicted: ", predicted)

x = add_constant(x)
model = OLS(y,x).fit()
predicted = model.predict([[1, new_size, new_proccessor, new_proccessor_turbo, new_ram, new_hdd]])
print(model.summary())