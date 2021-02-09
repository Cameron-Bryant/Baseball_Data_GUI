import xlsxwriter
import xlrd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score
#get data from the excel file
wb = xlrd.open_workbook("C://Users//camer//Desktop//ScrapingData//MLB_Data.xlsx")
sheet =  wb.sheet_by_index(0)

players = []
for i in range(sheet.nrows):
    if i > 0:
        players.append(sheet.cell_value(i, 0))

categories = []
for i in range(sheet.ncols):
    if i > 0:
        categories.append(sheet.cell_value(0, i))

data = []
for i in range(sheet.nrows):
    d = []
    for j in range(sheet.ncols):
        if i > 0 and j > 1:
            d.append(sheet.cell_value(i, j))
    data.append(d)
data.pop(0)

def printGood(d):
    for i in range(len(d)):
        print(d[i])

#Step 2: Visualize and Apply a Regression Model
#I am going to use the 6 'core' statistics of baseball for each player
#ab, g, Runs, Hits, Doubles, Triples, Homers, and RBIS
#can't use ab and hits at same time because colinearity
#to predict batting avgs
train_batch = []
test_batch = []
targets = []
test_targets = []#used only to calculate error
for i in range(len(data)):#change which data is selected here to explore 
    if i <= 100:
        train_batch.append(data[i][4:14])
        targets.append(data[i][14])
    else:
        test_batch.append(data[i][4:14])
        test_targets.append(data[i][14])
def plotPlots():
    for i in range(len(train_batch)):
        plt.plot(targets[i], train_batch[i][0], 'ro')
    plt.title("Avg vs " + categories[4])
    plt.show()
    plt.cla()
    for i in range(len(train_batch)):
        plt.plot(targets[i], train_batch[i][1], 'ro')
    plt.title("Avg vs " + categories[5])
    plt.show()
    plt.cla()
    for i in range(len(train_batch)):
        plt.plot(targets[i], train_batch[i][2], 'ro')
    plt.title("Avg vs " + categories[6])
    plt.show()
    plt.cla()
    for i in range(len(train_batch)):
        plt.plot(targets[i], train_batch[i][3], 'ro')
    plt.title("Avg vs " + categories[7])
    plt.show()
    plt.cla()
    for i in range(len(train_batch)):
        plt.plot(targets[i], train_batch[i][4], 'ro')
    plt.title("Avg vs " + categories[8])
    plt.show()
    plt.cla()

plotPlots()
def model():
    lr = LinearRegression()
    lr.fit(train_batch, targets)
    y_pred = lr.predict(test_batch)
    print("MODEL PRED:>")
    print(y_pred)
    print(mse(test_targets, y_pred))
    printGood(test_targets)
    print("coeffs")
    print(lr.coef_)
    print("intercept/const:>" + str(lr.intercept_))
    print("R2 Score:>" + str(r2_score(test_targets, y_pred)))

   
model()

###Summary:> Using multiple linear regression on categories 4-13 yielded
#around .0001 mse. USed 100 training examples and around 40 test examples.
#To do this better I could collect more data from the MLB stats website and try to 
#find different things to predict. By changing the categories used I saw the effect
#of different stats on deciding what the prediction would be. 
#Got an R2 score of around 83, which is pretty good but not the best for making 
#sound predictions
