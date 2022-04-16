import tkinter as tk
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from PIL import Image, ImageTk
from skimage import io
from skimage import transform
from sklearn.ensemble import RandomForestClassifier

################################################################################
#                         INITIALIZE DRAWING CONSTANTS                         #
################################################################################

# The user will be drawing on canvas but we can't just dump the pixels.
# Instead, we must either use platform-dependent code to take a screenshot or
# come up with some alternative. Our alternative is that we will generate an
# internal 2D array of pixels at the same time as we are drawing them.
black_pixel = np.full((1, 3), 0, dtype=np.uint8)
white_pixel = np.full((1, 3), 255, dtype=np.uint8)
test_sample = np.full((140, 140, 3), black_pixel, dtype=np.uint8)

################################################################################
#                      BUTTON HANDLERS AND FUNCTIONS                           #
################################################################################

def clear_drawing():
    ''' Clears the drawing canvas and internal array. '''

    cvs_drawspace.delete('all')  # drawing canvas
    lbl_result.config(text = "")
    test_sample[:] = black_pixel # internal representation of drawing

def draw_handwriting(event):
    ''' Draws on the canvas and internal array based on mouse coordinates. '''

    # xy-coordinates and radius of the circle being drawn
    x = event.x
    y = event.y
    r = 2
    cvs_drawspace.create_oval(x - r, y - r, x + r+1, y + r+1, fill='black')
    test_sample[y-2:y+3,x-2:x+3] = white_pixel

def classify_number():
    '''
    Runs Format Number and predicts using the already existing model
    '''
    test_num = format_number()
    prediction = forest.predict(test_num)
    lbl_result.config(text=f"Result: {prediction}", background='green')

def format_number():
    '''
    Takes test_sample data from user handwriting, and formats it 
    into a 1X784 dataframe so RFC can use it

    This sucks and is inefficient, but it's the best I can do for now.
    '''
    newTest = transform.resize(test_sample, output_shape=(28, 28))
    
    for x in newTest:
        for y in range(len(x)):
            x[y] = x[y] * 255

    newTest = newTest.astype(int)
    temp = []

    for x in newTest:
        for y in x:
            temp.append(y)

    columnNames = []
    for x in range(784):
        columnNames.append("pixel" + str(x))

    df = pd.DataFrame(temp)
    cols = [1,2]
    df = df.drop(df.columns[cols], axis=1)
    df = df.swapaxes("index", "columns")
    df.columns = columnNames
    return df

def getAccuracy():
    '''
    Uses the pre-established RFC model to get an accuracy score based off of the test data which was also previously split.
    '''
    accPreds = forest.predict(X_test)
    acc = accuracy_score(y_test, accPreds)
    acc = round(acc * 100)
    return acc

################################################################################
#                                 DRAW THE GUI                                 #
################################################################################

# Create a GUI window with a certain size and title
window = tk.Tk()
window.geometry("450x380")
window.config(bg='#86e1ef')
window.wm_title('Handwriting Recognition')
window.grid_columnconfigure((0, 1, 2), weight=1)

#Creating the RFC model globally so program runs faster and more efficient and also to get accuracy without needing to press the button
df = pd.read_csv('mnist_train.csv')
y = df['label']
X = df.drop('label', axis='columns')
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=6, test_size=0.169, stratify=y)
forest = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=20)
forest.fit(X_train, y_train)
acc = getAccuracy()

# Create all the buttons and stuff. Each column will be as wide as it's widest widget. So we make some artifically wide widgets.
lbl_title = tk.Label(text=f'Handwritten Digit Classifier')
lbl_result = tk.Label(text=f'')

# This drawing canvas will be very important for our ML model
rfc_accuracy = tk.Label(text=f"Random Forest Accuracy = {acc}%")
cvs_drawspace = tk.Canvas(width=140, height=140, bg='white', cursor='tcross',
                          highlightthickness=1, highlightbackground='steelblue')

#The Classify button
btn_classify = tk.Button(window, text='Classify Number', command=classify_number)
btn_clear = tk.Button(window, text='Reset Everything', foreground='red', command=clear_drawing)

# The grid layout makes sense but is a bit tedious
lbl_title.grid(row=0, column=1, pady=5)
rfc_accuracy.grid(row=2, column=1, pady=5)
cvs_drawspace.grid(row=3, column=1, pady=5)
btn_classify.grid(row=4, column=1, pady=5)
lbl_result.grid(row=5, column=1, pady=5)
btn_clear.grid(row=6, column=1, pady=5)


cvs_drawspace.bind('<B1-Motion>', draw_handwriting)
cvs_drawspace.bind('<Button-1>', draw_handwriting)

default_background_color = lbl_title.cget('background')

#window.resizable(False, False)
window.resizable(True, True)
window.mainloop()
