

from tkinter import *

def add(numberOne, numberTwo):
    return round(numberOne + numberTwo, 3)
   

def subtract(numberOne, numberTwo):
    return round(numberOne - numberTwo, 3)
     

def multiply(numberOne, numberTwo):
    return round(numberOne * numberTwo, 3)
    

def divide(numberOne, numberTwo):
    try:
        if (numberOne / numberTwo).is_integer() == True:
            return int(numberOne / numberTwo)
        else:
            return round(numberOne / numberTwo, 3)
    except:
        return False
    

def showNumber(number):
    buttonEquals.config(state=NORMAL)
    if displayVar.get() != '0' and number != '.':
        alreadyVisible = displayVar.get()
        newDisplay = alreadyVisible + str(number)
        displayVar.set(newDisplay)
    elif displayVar.get() == '0' and number == '.':
        alreadyVisible = displayVar.get()
        newDisplay = alreadyVisible + str(number)
        displayVar.set(newDisplay)
    elif displayVar.get() != '0' and number == '.':
        alreadyVisible = displayVar.get()
        newDisplay = alreadyVisible + str(number)
        displayVar.set(newDisplay)
    else:
        displayVar.set(number)



def getNumberOne(operand):
    global addCheck, subtractCheck, multiplyCheck, divideCheck
    addCheck = False
    subtractCheck = False
    multiplyCheck = False
    divideCheck = False
    global number1
    input1 = displayVar.get()
    while input1[-1] == '.':
        input1 = input1[:-1]
        if input1[-1] != '.':
            break
    try:
        number1 = float(input1)
        buttonEquals.config(state=NORMAL)
        displayVar.set('0')
        if operand == '+':
            addCheck = True
            subtractCheck = False
            multiplyCheck = False
            divideCheck = False
        elif operand == '-':
            addCheck = False
            subtractCheck = True
            multiplyCheck = False
            divideCheck = False
        elif operand == 'x':
            addCheck = False
            subtractCheck = False
            multiplyCheck = True
            divideCheck = False
        elif operand == '/':
            addCheck = False
            subtractCheck = False
            multiplyCheck = False
            divideCheck = True
    except:
        displayVar.set('Error1')
    return addCheck, subtractCheck, multiplyCheck, divideCheck
   
def getNumberTwo():
    buttonEquals.config(state=DISABLED)
    global equals
    input2 = displayVar.get()
    while input2[-1] == '.':
        input2 = input2[:-1]
        if input2[-1] != '.':
            break  
    try:
        number2 = float(input2)
        if addCheck == True:
            equals = add(number1, number2)
            if equals.is_integer() == True:
                displayVar.set(str(int(equals)))
            else:
                displayVar.set(str(equals))
            equals = number1
        elif subtractCheck == True:
            equals = subtract(number1, number2)
            if equals.is_integer() == True:
                displayVar.set(str(int(equals)))
            else:
                displayVar.set(str(equals))
            equals = number1
        elif multiplyCheck == True:
            equals = multiply(number1, number2)
            if equals.is_integer() == True:
                displayVar.set(str(int(equals)))
            else:
                displayVar.set(str(equals))
            equals = number1
        elif divideCheck == True:
            equals = divide(number1, number2)
            if equals.is_integer() == True:
                displayVar.set(str(int(equals)))
            else:
                displayVar.set(str(equals))
            equals = number1
    except:
        displayVar.set('Error2')
    
def clear():
    displayVar.set('0')
    buttonEquals.config(state=NORMAL)

master = Tk()
master.title("Josh's Calculator")
master.geometry("400x580")
master.config(bg='black')

displayVar = StringVar()
displayVar.set('0')
display = Label(master, textvariable=displayVar, bg='dark grey', fg='white', font=('Arial',40,'bold'),
                width =6, height=2)
display.grid(columnspan=3, column=1, row=0, pady=10, padx=10)

master.columnconfigure(0, weight=1)
master.columnconfigure(5, weight=1)
master.rowconfigure(0, weight=1)
master.rowconfigure(4, weight=1)

buttonClear = Button(master, text='C', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=2, command= lambda : clear())
buttonClear.grid(column=4, row=0)

button7 = Button(master, text='7', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(7))
button7.grid(column=1, row=1)

button8 = Button(master, text='8', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(8))
button8.grid(column=2, row=1)

button9 = Button(master, text='9', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(9))
button9.grid(column=3, row=1, pady=10)


button4 = Button(master, text='4', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(4))
button4.grid(column=1, row=2)

button5 = Button(master, text='5', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(5))
button5.grid(column=2, row=2)

button6 = Button(master, text='6', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(6))
button6.grid(column=3, row=2, pady=10)


button1 = Button(master, text='1', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(1))
button1.grid(column=1, row=3, padx=10)

button2 = Button(master, text='2', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(2))
button2.grid(column=2, row=3, padx=10)

button3 = Button(master, text='3', bg='grey', fg='black', font=('Arial',30,'bold'),
                 command= lambda : showNumber(3))
button3.grid(column=3, row=3, pady=10, padx=10)

button0 = Button(master, text='0', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : showNumber(0))
button0.grid(column=1, row=4)

buttonDecimal = Button(master, text='.', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, width=2, command= lambda : showNumber('.'))
buttonDecimal.grid(column=2, row=4)

buttonPlus = Button(master, text='+', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, width=2, command= lambda : getNumberOne('+'))
buttonPlus.grid(column=4, row=1)

buttonMinus = Button(master, text='-', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, width=2, command= lambda : getNumberOne('-'))
buttonMinus.grid(column=4, row=2)

buttonTimes = Button(master, text='x', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, width=2, command= lambda : getNumberOne('x'))
buttonTimes.grid(column=4, row=3)

buttonDivide = Button(master, text='/', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, width=2, command= lambda : getNumberOne('/'))
buttonDivide.grid(column=4, row=4, padx=10)

buttonEquals = Button(master, text='=', bg='grey', fg='black', font=('Arial',30,'bold'),
                 height=1, command= lambda : getNumberTwo())
buttonEquals.grid(column=3, row=4)


master.mainloop()
