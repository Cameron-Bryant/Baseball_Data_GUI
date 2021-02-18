import tkinter as tk
import xlrd
import xlsxwriter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

#load default data. Change path here for your computer or input in the GUI
mlb_data = []
workb = xlrd.open_workbook('C://Users//camer//Desktop//ScrapingData//MLB_Data.xlsx')
wksheet = workb.sheet_by_index(0)
for i in range(wksheet.nrows):
    mlb_data.append(wksheet.row_values(i))

#make window and set width and height
window = tk.Tk()
window.title("MLB Data Analysis Tool")
window.geometry("800x800")
#widgets
#title = tk.Label(window, text="MLB Data Analysis Tool")
#labels
tk.Label(window, text= "File Location (Optional)").grid(row=1)
tk.Label(window, text= "X Attribute").grid(row=2)
tk.Label(window, text= "Y Attribute").grid(row=3)
tk.Label(window, text= "Attributes: Player, Team, G, AB, R, H, 2B, 3B, HR, RBI, BB, SO, SB, CS, AVG, OBP, SLG").grid(row=5)
tk.Label(window, text= "Analysis Options").grid(row=6)
#entries
loc_entry = tk.Entry(window)
loc_entry.grid(row=1, column = 1)
rows_entry = tk.Entry(window)
rows_entry.grid(row=2, column = 1)
cols_entry = tk.Entry(window)
cols_entry.grid(row=3, column = 1)
type_entry=tk.Entry(window)
#drop down menu

optionList = ('Linear Regression', '2nd Deg Polynomial Regression', '3rd Deg Polynomial Regression')
variable = tk.StringVar()
variable.set(optionList[0])
analysis_option_menu = tk.OptionMenu(window, variable, *optionList)
analysis_option_menu.grid(row=6, column=1)

def make_path_readable(path):
    splt = path.split('\\')
    print(splt)
    file_type = splt[-1].split('.')
    file_type = file_type[1] 
    new = '//'.join(splt)
    
    return new, file_type
#get the data from the file
def fetchData():
    #get the data dependent on the filetype, if none do mlb data default
    if len(loc_entry.get()) > 1:
            location, filetype = make_path_readable(loc_entry.get())
            if filetype == 'txt':
                loc = open(location)
                data = loc.read()
            elif filetype == 'xlsx' or filetype == 'xls':
                data = []
                wb = xlrd.open_workbook(location)
                sheet = wb.sheet_by_index(0)
                print(sheet.nrows)
                for i in range(sheet.nrows):
                    data.append(sheet.row_values(i))
    else:
        data = mlb_data
    
    #allow text or index for the attrs:
    try:
        r = int(rows_entry.get())
        c = int(cols_entry.get())
    except ValueError:
        r = data[0].index(rows_entry.get())
        c = data[0].index(cols_entry.get())
    
    x = []
    y = []
    for i in range(100):
        if i > 0:
            x.append(float(data[i][int(c)]))
            y.append(float(data[i][int(r)]))

    labs = [data[0][int(c)], data[0][int(r)]]
    return x, y, labs

def visualize_and_analyze(x, y, labs):
    figure = plt.Figure(figsize=(5,5), dpi=100)
    ax = figure.add_subplot(111)
    #plot data
    ax.scatter(x,y)
    ax.set_xlabel(labs[0])
    ax.set_ylabel(labs[1])
    #plot analysis line
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    analysis_choice = variable.get()
    if analysis_choice == 'Linear Regression':
        lr = LinearRegression()
        lr.fit(x,y)
        ax.plot(x, lr.predict(x), color='k')
    elif analysis_choice == '2nd Deg Polynomial Regression':
        poly_feat = PolynomialFeatures(degree=2)
        x_poly = poly_feat.fit_transform(x)
        lr = LinearRegression()
        lr.fit(x_poly, y)
        ax.plot(x, lr.predict(x_poly), color='k')
    elif analysis_choice == '3rd Deg Polynomial Regression':
        poly_feat = PolynomialFeatures(degree=3)
        x_poly = poly_feat.fit_transform(x)
        lr = LinearRegression()
        lr.fit(x_poly, y)
        ax.plot(x, lr.predict(x_poly), color='k')

    canvas = FigureCanvasTkAgg(figure, window)
    canvas.get_tk_widget().grid(row=11)
    canvas.draw()
    figure.clf()
    
    ax.set_title('Data')

def run():
    x,y, labels = fetchData()
    visualize_and_analyze(x, y, labels)

enter_button = tk.Button(window, text="Enter", command = run).grid(row=7, column=1)

window.mainloop()
