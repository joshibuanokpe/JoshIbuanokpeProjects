#remember to set best before to datetime
from tkinter import *
from tkinter.ttk import Combobox
class Fruit:
    #countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        self.numberOfPacks = numberOfPacks
        self.numberOfServingsPerPack = numberOfServingsPerPack
        #Fruit.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Fruit.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
    
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings   

class Tins:
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        self.numberOfPacks = numberOfPacks
        self.numberOfServingsPerPack = numberOfServingsPerPack
        #Fruit.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Tins.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
    

    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings  

class Food:
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfItemsPerPack, numberOfServingsPerPack):
        self.numberOfPacks = numberOfPacks
        self.numberOfItemsPerPack = numberOfItemsPerPack
        self.numberOfServingsPerPack = numberOfServingsPerPack
        Food.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Food.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
    
    @classmethod
    def get_itemTotal(cls):
        return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings      
        
        

class Orange(Fruit):
   # countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Orange.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
   # @classmethod
#    def get_itemTotal(cls):
 #       return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings


class Grapes(Fruit):
   # countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Grapes.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
  #  @classmethod
#    def get_itemTotal(cls):
 #       return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class Banana(Fruit):
   # countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Banana.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
    @classmethod
#    def get_itemTotal(cls):
 #       return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

        
class Egg:
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfItemsPerPack, numberOfServingsPerPack):
        self.numberOfPacks = numberOfPacks
        self.numberOfItemsPerPack = numberOfItemsPerPack
        self.numberOfServingsPerPack = numberOfServingsPerPack
        Egg.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Egg.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
    @classmethod
    def get_itemTotal(cls):
        return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class Apple(Fruit):
   # countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
       # Apple.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Apple.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinVeg(Tins):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinVeg.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class Beans(TinVeg):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Beans.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class Sweetcorn(TinVeg):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        Sweetcorn.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinMeatNonHalal(Tins):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinMeatNonHalal.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinMeatHalal(Tins):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinMeatHalal.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings


class TinSoup(Tins):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinSoup.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinBeef(TinMeatHalal):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinBeef.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinChicken(TinMeatHalal):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinChicken.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinHotdogs(TinMeatNonHalal):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinHotdogs.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinHam(TinMeatNonHalal):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinHam.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class TinTomatoSoup(TinSoup):
    countItems = 0
    countServings = 0
    def __init__(self, numberOfPacks, numberOfServingsPerPack):
        super().__init__(numberOfPacks, numberOfServingsPerPack)
        self.numberOfServingsPerPack = self.numberOfServingsPerPack
        #Orange.countItems += (self.numberOfItemsPerPack * self.numberOfPacks)
        TinTomatoSoup.countServings += (self.numberOfServingsPerPack * self.numberOfPacks)
       
#    @classmethod
 #   def get_itemTotal(cls):
  #      return cls.countItems 
    
    @classmethod
    def get_servingsTotal(cls):
        return cls.countServings

class Household:
    
    totalHouseholds = 0
    totalAdults = 0
    totalChildren = 0
    totalInfants = 0
    totalPeople = 0
    
    
    def __init__(self, numberOfAdults, numberOfChildren, numberOfInfants):
        
        self.numberOfAdults = numberOfAdults
        self.numberOfChildren = numberOfChildren
        self.numberOfInfants = numberOfInfants
        
        Household.totalHouseholds += 1
        Household.totalAdults += self.numberOfAdults
        Household.totalChildren += self.numberOfChildren
        Household.totalInfants += self.numberOfInfants
        
    @classmethod
    def totalHouseholdsMethod(cls):
        return cls.totalHouseholds
    
    @classmethod
    def addHousehold(cls):
        cls.totalHouseholds += 1

    @classmethod
    def totalAdultsMethod(cls):
        return cls.totalAdults

    @classmethod
    def totalChildrenMethod(cls):
        return cls.totalChildren
 
    @classmethod
    def totalInfantsMethod(cls):
        return cls.totalInfants
       
    @classmethod
    def totalPeopleMethod(cls):
        cls.totalPeople = cls.totalAdults + cls.totalChildren + cls.totalInfants
        return cls.totalPeople
    
#class Foodpack:
 #   def __init__(self, type, food1, food2)
#Food(no of packs, no of items per pack, no of servings per pack)

def add_fruit(fruitType, numPacks, numServings):
    if fruitType == 1:
        oranges = Orange(numPacks, numServings)
        return oranges
    elif fruitType == 2:
        apples = Apple(numPacks, numServings)
        return apples
    elif fruitType == 3:
        bananas = Banana(numPacks, numServings)
        return bananas
    elif fruitType == 4:
        grapes = Grapes(numPacks, numServings)
        return grapes


def add_tins(tinType, numPacks, numServings):
    if tinType == 1:
        beans = Beans(numPacks, numServings)
        return beans
    elif tinType == 2:
        sweetcorn = Sweetcorn(numPacks, numServings)
        return sweetcorn
    elif tinType == 3:
        tinbeef = TinBeef(numPacks, numServings)
        return tinbeef
    elif tinType == 4:
        tinchicken = TinChicken(numPacks, numServings)
        return tinchicken
    elif tinType == 5:
        hotdogs = TinHotdogs(numPacks, numServings)
        return hotdogs
    elif tinType == 6:
        tomatosoup = TinTomatoSoup(numPacks, numServings)
        return tomatosoup
    
#add_fruit(1,2,10)
#add_fruit(2,2,10)
#add_fruit(3,4,10)
#add_tins(1,10,2)
#add_tins(4, 10, 2)
#add_tins(5, 20, 2)
#add_tins(3, 15, 2)

master = Tk()
master.title("Foodbank Inventory")
master.geometry("400x500")
master.config(bg='light yellow')

def addbuttonclick():
    subtitleVar.set('Add food')
    addfooddropdown.grid(column=1, row=4, pady=10, padx=10)

def showfoodlist(event):
    if addfooddropdown.get() == 'Fruit':
        fruitlistdropdown.grid(column=1, row=5, pady=10, padx=10)
    
#def additems(event):
 #   if fruitlistdropdown.get() == 'Oranges':

def showfruitentries(event):
    addfruitentryframe.grid(column=1, row=6, pady=5, padx=10)
    packslabel.grid(column=1, row=0, pady=0, padx=10)
    packsentry.grid(column=2, row=0, pady=0, padx=10)
    servingslabel.grid(column=1, row=1, pady=0, padx=10)
    servingsentry.grid(column=2, row=1, pady=0, padx=10)
    addfoodbutton.grid(columnspan=2, column=1, row=3, pady=5, padx=10)
    resetbutton.grid(columnspan=2, column=1, row=4, pady=5, padx=10)
    addfoodresult.grid(columnspan=4, column=0, row=5, pady=5, padx=10)

def showsoupentries(event):#need to figure out how im going to make this method - will probably put everything in frames
    addsoupentryframe.grid(column=1, row=6, pady=5, padx=10)
    packslabel.grid(column=1, row=0, pady=0, padx=10)
    packsentry.grid(column=2, row=0, pady=0, padx=10)
    servingslabel.grid(column=1, row=1, pady=0, padx=10)
    servingsentry.grid(column=2, row=1, pady=0, padx=10)
    addfoodbutton.grid(columnspan=2, column=1, row=3, pady=5, padx=10)
    resetbutton.grid(columnspan=2, column=1, row=4, pady=5, padx=10)
    addfoodresult.grid(columnspan=4, column=0, row=5, pady=5, padx=10)



def addfruittoinv():
    addfoodbutton.config(state=DISABLED)
    packsentry.config(state=DISABLED)
    servingsentry.config(state=DISABLED)
    resetbutton.config(state=NORMAL)
    if fruitlistdropdown.get() == 'Oranges':
        add_fruit(1,int(packsentry.get()),int(servingsentry.get()))
        addfoodresultVar.set(f'{int(packsentry.get())} packs of Oranges added\n'\
                             f'Inventory total Orange servings: {Orange.get_servingsTotal()}\n'\
                             f'Inventory total fruit servings: {Fruit.get_servingsTotal()}')
        
    elif fruitlistdropdown.get() == 'Apples':
        add_fruit(2,int(packsentry.get()),int(servingsentry.get()))
        addfoodresultVar.set(f'{int(packsentry.get())} packs of Apples added\n'\
                             f'Inventory total Apple servings: {Apple.get_servingsTotal()}\n'\
                             f'Inventory total fruit servings: {Fruit.get_servingsTotal()}')
            
    elif fruitlistdropdown.get() == 'Bananas':
        add_fruit(3,int(packsentry.get()),int(servingsentry.get()))
        addfoodresultVar.set(f'{int(packsentry.get())} packs of Bananas added\n'\
                             f'Inventory total Banana servings: {Banana.get_servingsTotal()}\n'\
                             f'Inventory total fruit servings: {Fruit.get_servingsTotal()}')
        
    elif fruitlistdropdown.get() == 'Grapes':
        add_fruit(4,int(packsentry.get()),int(servingsentry.get()))
        addfoodresultVar.set(f'{int(packsentry.get())} packs of Grapes added\n'\
                             f'Inventory total Grape servings: {Grapes.get_servingsTotal()}\n'\
                             f'Inventory total fruit servings: {Fruit.get_servingsTotal()}')
            

def resetfruitadd():
    addfoodbutton.config(state=NORMAL)
    resetbutton.config(state=DISABLED)
    packsentry.config(state=NORMAL)
    servingsentry.config(state=NORMAL)
    packsentry.delete(0,END)
    servingsentry.delete(0,END)
    addfoodresultVar.set(f'\n\nInventory total fruit servings: {Fruit.get_servingsTotal()}')
    
    
    
    

    
title = Label(master, text='Foodbank Inventory', bg='light yellow', fg='green', font=('Arial',20,'bold'),
                width=20, height=2)
title.grid( column=1, row=0, pady=5, padx=10)

subtitleVar = StringVar()
subtitleVar.set('')

AddButton = Button(master, text='Add food', fg='light yellow', bg='green', font=('Arial',10), height=1,
                   width=15, command= lambda : addbuttonclick())
AddButton.grid(column=1, row=1, pady=5, padx=10)

CheckButton = Button(master, text='Check inventory', fg='light yellow', bg='green', font=('Arial',10), height=1,
                   width=15)
                   #, command= lambda : showNumber(8))
CheckButton.grid(column=1, row=2, pady=5, padx=10)

subtitle = Label(master, textvariable=subtitleVar, bg='light yellow', fg='green', font=('Arial', 14, 'bold'),
                 width=20, height=2)
subtitle.grid(column=1, row=3, pady=5, padx=10)




addfoodtypes = ["Fruit", "Tinned soup", "Tinned vegetables", "Tinned meat (Halal)",
                "Tinned meat (non-Halal)", "Other"]
addfoodtypesVar = StringVar()
addfoodtypesVar.set('Select food category')

#---------------------fruit--------------------------------

fruitlist = ['Oranges', 'Apples', 'Grapes', 'Bananas']
fruitlistVar = StringVar()
fruitlistVar.set('Select fruit')

fruitlistdropdown = Combobox(master,state='readonly',textvariable=fruitlistVar,  values=fruitlist)
fruitlistdropdown.bind("<<ComboboxSelected>>", showfruitentries)

addfruitentryframe = Frame(master, bg='light yellow')

packslabel = Label(addfruitentryframe, text='No. Packs', fg='black', bg='light yellow', width=20,
                      anchor='w')
packsentry = Entry(addfruitentryframe,width=3)
servingslabel = Label(addfruitentryframe, text='No. Servings per pack', fg='black', bg='light yellow', width=20,
                      anchor='w')
servingsentry = Entry(addfruitentryframe,width=3)
addfoodbutton = Button(addfruitentryframe, text='Add to inventory', fg='light yellow',
                       bg='green', height=1, width=15, command=addfruittoinv)

resetbutton = Button(addfruitentryframe, text='Add another item', fg='light yellow',
                       bg='green', height=1, width=15, command=resetfruitadd, state=DISABLED)

addfoodresultVar = StringVar()
addfoodresultVar.set('')

addfoodresult = Label(addfruitentryframe, textvariable=addfoodresultVar, fg='green', bg='light yellow',
                      width=40, font=('Arial', 10, 'bold'), height=3, justify=LEFT)

addfooddropdown = Combobox(master,state='readonly',textvariable=addfoodtypesVar,  values=addfoodtypes)
addfooddropdown.bind("<<ComboboxSelected>>", showfoodlist)

#----------------------------Tinned soup-----------------

souplist = ['Tomato soup']
souplistVar = StringVar()
souplistVar.set('Select soup')

souplistdropdown = Combobox(master,state='readonly',textvariable=souplistVar,  values=souplist)
souplistdropdown.bind("<<ComboboxSelected>>", showsoupentries)

addsoupentryframe = Frame(master, bg='light yellow')

packslabel = Label(addsoupframe, text='No. Packs', fg='black', bg='light yellow', width=20,
                      anchor='w')
packsentry = Entry(addsoupentryframe,width=3)
servingslabel = Label(addsoupentryframe, text='No. Servings per pack', fg='black', bg='light yellow', width=20,
                      anchor='w')
servingsentry = Entry(addsoupentryframe,width=3)
addfoodbutton = Button(addsoupentryframe, text='Add to inventory', fg='light yellow',
                       bg='green', height=1, width=15, command=addsouptoinv)

resetbutton = Button(addsoupentryframe, text='Add another item', fg='light yellow',
                       bg='green', height=1, width=15, command=resetsoupadd, state=DISABLED)






master.mainloop()





