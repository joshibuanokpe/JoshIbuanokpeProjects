import os
import csv
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import * 
import tkinter.filedialog as fd
from PIL import ImageTk, Image

#function to convert a csv to a json file
def csv_to_json(csvFilePath): 
    #takes the argument of the file path of the csv file and converts it to a raw string
    csvFilePath = r"{}".format(csvFilePath)
    #the json file will be named the same as the csv file, with 'csv' sliced out and replaced with 'json'
    jsonFilePath = csvFilePath[:csvFilePath.rindex('.')+1] + 'json'
    
    #each row in is appended to empty list, then written to the json file path
    jsonArray = []
    
    with open(csvFilePath, encoding="utf-8") as csv_file:
        csvReader = csv.DictReader(csv_file)
            
        for row in csvReader:
            jsonArray.append(row)
            
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonWriter:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonWriter.write(jsonString)
    
    #making fileType global allows it to be accessed elsewhere, so the read file can be identified in input
    global fileType
    
    #the three file types are identified by dictionary keys that are exclusive to that particular file
    if any('municipality' in key for key in jsonArray):
        fileType = 0 # for airport
    elif any('frequency_mhz' in key for key in jsonArray):
        fileType = 1 # for frequencies 
    elif any('length_ft' in key for key in jsonArray):
        fileType = 2 # for runways file
    else:
        fileType = 3 # for any type of file
        
    #the number for the file type is returned to be used later
    return fileType
 

  
#function to remove type closed from airports file
def remove_closed_airports(filePath): 
    #reads the json file into a dataframe in order to remove this type then overwrites result back to 
    #the same path
    dfFile = pd.read_json(filePath)
    dfFile = dfFile[dfFile['type'] != 'closed']
    
    with open(filePath, 'w', encoding='utf-8') as jsonWriter:
        json.dump(dfFile.to_dict(orient='records'), jsonWriter)
    
        
    
#function to remove closed from other file types        
def remove_closed_other(aiportClosedRemovedFilePath, otherFilePath): 
    #using the airport file as a reference for closed airports, the json files are read in then overwritten
    #when closed airports have been removed
    dfAirports = pd.read_json(aiportClosedRemovedFilePath)
    dfFile = pd.read_json(otherFilePath)
    
    notClosed = dfFile.airport_ref.isin(dfAirports.id)
    dfFile = dfFile[notClosed]
    
    with open(otherFilePath, 'w') as jsonWriter:
        json.dump(dfFile.to_dict(orient='records'), jsonWriter)
 
    
#function to filter by UK airports and add the category key to the airports file by writing to dataframe
def add_category_and_filter(filePath):
    dfFile = pd.read_json(filePath)
    dfFile = dfFile[dfFile['iso_country'] == 'GB']
    dfFile['category'] = np.where(dfFile['type'] == 'small_airport','small_airport',
                                  np.where(dfFile['type'] == 'medium_airport','medium_airport',
                                           np.where(dfFile['type'] == 'large_airport','large_airport', '')))
    dfFile = dfFile[dfFile['category'] != '']
    with open(filePath, 'w', encoding='utf-8') as jsonWriter:
        jsonString = json.dump(dfFile.to_dict(orient='records'), jsonWriter)
        
        
#function to add frequencies information into the airport file
def add_frequencies(airportFilePath, frequenciesFilePath):
    #loaded into dataframes and reset the indexes for merge to the relevant keys     
    dfAirports = pd.read_json(airportFilePath)
    dfFrequencies = pd.read_json(frequenciesFilePath)
    dfFrequencies = dfFrequencies.set_index('airport_ref')
    dfFrequenciesColumnsHidden = dfFrequencies.reindex(columns = ['frequency_mhz'])
    
    #a left merge was used with different merge references, as id is different in both files
    merge = dfAirports.merge(dfFrequenciesColumnsHidden, how='left', 
                             left_index=False, right_index=True, left_on='id', right_on='airport_ref')
    
    with open(airportFilePath, 'w') as jsonWriter:
        json.dump(merge.to_dict(orient='records'), jsonWriter)    

        
#function to produce mean, mode and median frequencies for airports by category using dataframe
def mean_mode_median_frequency_by_category(filePath, category):        
    dfAirports = pd.read_json(filePath)
    dfAirports['frequency_mhz'] = pd.to_numeric(dfAirports['frequency_mhz'], errors='coerce')
    
    dfAirports = dfAirports.reindex(columns = ['category', 'frequency_mhz']) 
    dfAirportsGrouped = dfAirports.groupby('category')
  
    #all floats rounded to the same number of decimal places as the frequency_mhz information
    meanFrequency = round(dfAirportsGrouped['frequency_mhz'].get_group(category).mean(), 2)
    modeFrequency = round(dfAirportsGrouped['frequency_mhz'].get_group(category).mode().iat[0], 2)
    medianFrequency = round(dfAirportsGrouped['frequency_mhz'].get_group(category).median(), 2)
    
    return meanFrequency, modeFrequency, medianFrequency
  

#function to produce mean, mode and median frequencies for airports in a range using dataframe
def mean_mode_median_frequency_by_range(filePath, lowerBound, upperBound):
    dfAirports = pd.read_json(filePath)
    dfAirports['frequency_mhz'] = pd.to_numeric(dfAirports['frequency_mhz'], errors='coerce')
    
    dfAirports = dfAirports.reindex(columns = ['category', 'frequency_mhz'])
    
    dfFrequencyRange = dfAirports[(dfAirports['frequency_mhz'] > lowerBound) & 
                                  (dfAirports['frequency_mhz'] < upperBound)]
    
    meanFrequency = round(dfFrequencyRange['frequency_mhz'].mean(), 2)
    #try except used for mode for when the input range contains no frequency values
    try:
        modeFrequency = round(dfFrequencyRange['frequency_mhz'].mode().iat[0], 2)
    except:
        modeFrequency = False
    medianFrequency = round(dfFrequencyRange['frequency_mhz'].median(), 2)
    
    return meanFrequency, modeFrequency, medianFrequency


#function to produce boxplot for frequencies based on category
def plot_box_graph_by_category(filePath, category):
    dfAirports = pd.read_json(filePath)
    dfAirports['frequency_mhz'] = pd.to_numeric(dfAirports['frequency_mhz'], errors='coerce')
    

    dfAirports = dfAirports.reindex(columns = ['category', 'frequency_mhz'])
    
    dfAirportsGrouped = dfAirports.groupby('category')
      
    
    dfAirportsGrouped = dfAirportsGrouped['frequency_mhz'].get_group(category)
    
    #interquartile range created so that a zoomed boxplot can be shown
    dfFrequencyQuartileOne = dfAirportsGrouped.quantile(0.25)
    dfFrequencyQuartileThree = dfAirportsGrouped.quantile(0.75)
    
    
    #zoom range of boxplot
    RangeOne = dfFrequencyQuartileOne - 15
    RangeTwo = dfFrequencyQuartileThree + 15
    
    #plot of two boxplots
    plt.figure(figsize=(8,4), linewidth=10, edgecolor='navy')
    
    plt.subplot(2, 1, 1)
    dfAirportsGrouped.plot.box(vert=False, widths = 0.5)
    plt.title(f'Box plot for airport frequencies in the {category} category')
    plt.xlabel('Frequency (MHz)')
    
    plt.yticks([2, 1, 1], [''])
    
    plt.subplot(2, 1, 2)
    dfAirportsGrouped.plot.box(vert=False, widths = 0.5)
    plt.title(f'Box plot for airport frequencies in the {category} category\n(zoomed to exclude'\
              ' outliers)')
    plt.yticks([2, 1, 2], [''])
    plt.xlabel('Frequency (MHz)')
    plt.xlim([RangeOne, RangeTwo])
    plt.subplots_adjust(hspace=1.4)
    
    #generating filepath based on whether it has been entered as a forwardslash or backslash
    try:
        folder = filePath[:filePath.rindex('/')+1]
    except:
        folder = filePath[:filePath.rindex('\\')+1]
        
    pngFilePath = r"{}".format(folder + 'box_plot_' + category +'.png')
    plt.savefig(pngFilePath, edgecolor='navy')
    return pngFilePath


#function to produce scatter graph for frequencies for all categories
def plot_scatter_graph_all_categories(filePath):
    dfAirports = pd.read_json(filePath)
    dfAirports['frequency_mhz'] = pd.to_numeric(dfAirports['frequency_mhz'], errors='coerce')
    dfAirports = dfAirports.reindex(columns = ['category', 'frequency_mhz'])
        
    dfAirportsSorted = dfAirports.sort_values(
        by=['category'], ascending = False).reset_index().reindex(
            columns = ['category', 'frequency_mhz'])
        
    
    x_axis = dfAirportsSorted['category']
    y_axis = dfAirportsSorted['frequency_mhz']
    
    #colour range and colour bar and y axis grid shown to show banding correlations
    plt.figure(figsize=(6,4), linewidth=10, edgecolor='navy')
    plt.scatter(x=x_axis, y=y_axis, c=y_axis, cmap='gist_rainbow')
    plt.colorbar().set_label('Frequency (MHz)')
    plt.ylabel('Frequency (MHz)')
    plt.grid(axis='y')
    plt.title('Airport frequencies by category')
    #generating filepath based on whether it has been entered as a forwardslash or backslash
    try:
        folder = filePath[:filePath.rindex('/')+1]
    except:
        folder = filePath[:filePath.rindex('\\')+1]
    
    pngFilePath = folder + 'all_categories.png'
    plt.savefig(pngFilePath, edgecolor='navy')
    return pngFilePath


    
   
#master window and all frames created
master = Tk()
master.title("Advanced Programming: Summative Assessment")
master.geometry("600x600")

frame1=Frame(master, bg='snow',height=30)
frame1.pack_propagate(0)
frame1.pack(expand=True,fill=BOTH)

frame2=Frame(master, bg='snow', height=500)
frame2.pack_propagate(0)


frame22=Frame(frame2,bg='snow', height=500)

frame23=Frame(frame2,bg='snow', height=500)

frame3=Frame(master, bg='snow', height=500)
frame3.pack_propagate(0)


frame4=Frame(frame3, bg='snow', height=500)

frame5=Frame(master, bg='snow', height=500)
frame5.pack_propagate(0)

frame50=Frame(frame5,bg='snow',height=500, width=550)

frame6=Frame(master, bg='snow', height=500)
frame6.pack_propagate(0)


frame7=Frame(master, bg='snow', height=500)
frame7.pack_propagate(0)


frame8=Frame(frame7, bg='snow', height=500)

frame9=Frame(frame7, bg='snow', height=500)

frame10=Frame(frame7, bg='snow', height=500)

frame11=Frame(master, bg='snow', height=500)
frame11.pack_propagate(0)

frame12=Frame(frame11, bg='snow', height=500)
frame12.pack_propagate(0)

stringVarTitle = StringVar()
stringVarTitle.set('Load three CSV files to begin')
home_title = Label(frame1, textvariable=stringVarTitle , font=('None', 12, 'bold'), bg='snow', fg='navy')
home_title.pack()   
    
start_button1 = Button(frame1, text='Load files', height=2, width=10)
start_button1.pack()
start_button1.config(command=lambda start_button1=start_button1: 
                     [launch(), start_button1.config(state=DISABLED)])

#method to launch program
def launch():
      
    #-------------------------------------------------
    #methods to open browse filepath boxes in for the entry fields
    def browse_file0():
        filePath = fd.askopenfilename()
        entry0.delete(0, END)
        entry0.insert(END, filePath)
        
    def browse_file1():
        filePath = fd.askopenfilename()
        entry1.delete(0, END)
        entry1.insert(END, filePath)
    
    def browse_file2():
        filePath = fd.askopenfilename()
        entry2.delete(0, END)
        entry2.insert(END, filePath)
    #-------------------------------------------------
    
    
    #function to re-enable filepath fields when incorrect files have been input
    def retry_load():
        entry0.config(state=NORMAL)
        entry0.delete(0, END)
        entry1.config(state=NORMAL)
        entry1.delete(0, END)
        entry2.config(state=NORMAL)
        entry2.delete(0, END)
        button0.config(state=NORMAL)
        button1.config(state=NORMAL)
        button2.config(state=NORMAL)
        button3.config(state=NORMAL)
        stringVar3.set("")
        stringVar4.set("\n\n\n")
     
    #function with embedded functions assignment and moving between pages 
    def process_files():
        #convert to json based on the entries
        def convert_to_json_and_initial_processing():
            #try except used for the case that the three files have not been input
            try:
                #get and convert entries to raw strings
                csvFilePath0 = r"{}".format(entry0.get())
                csvFilePath1 = r"{}".format(entry1.get())
                csvFilePath2 = r"{}".format(entry2.get())
                
                #assigning the filetypes returned from csv_to_json to variables of three entries
                fileType0 = csv_to_json(csvFilePath0)
                fileType1 = csv_to_json(csvFilePath1)
                fileType2 = csv_to_json(csvFilePath2)
                
                # using the fileTypes to mitigate against the files being input in an order not expected
                if fileType0 == fileType1 or fileType0 == fileType2 or fileType1 == fileType2:
                    stringVar4.set('The JSON file/s has been created and loaded into the same directory'\
                                   ' folder\nThe filepaths selected are not distinct, therefore no '\
                                       'further action has been taken\nRetry using the button below')
            
                elif fileType0 == 0 and fileType1 == 1 and fileType2 == 2:
                    jsonFilePath0 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath1 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath2 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                elif fileType0 == 0 and fileType1 == 2 and fileType2 == 1:
                    jsonFilePath0 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath2 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath1 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                elif fileType0 == 1 and fileType1 == 0 and fileType2 == 2:
                    jsonFilePath1 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath0 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath2 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                elif fileType0 == 1 and fileType1 == 2 and fileType2 == 0:
                    jsonFilePath1 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath2 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath0 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                elif fileType0 == 2 and fileType1 == 1 and fileType2 == 0:
                    jsonFilePath2 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath1 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath0 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                elif fileType0 == 2 and fileType1 == 0 and fileType2 == 1:
                    jsonFilePath2 = csvFilePath0[:csvFilePath0.rindex('.')+1] + 'json'
                    jsonFilePath0 = csvFilePath1[:csvFilePath1.rindex('.')+1] + 'json'
                    jsonFilePath1 = csvFilePath2[:csvFilePath2.rindex('.')+1] + 'json'
            
                else:
                    stringVar4.set('The three JSON files have been created and loaded into the same'\
                                   ' directory folder\nData in one of the files entered has data in '\
                                       'an unexpected format\nTry again')
                
                #making the json filepaths global and assigning to more recognisable names
                global jsonAirport 
                global jsonFrequency 
                global jsonRunways 
                jsonAirport = jsonFilePath0
                jsonFrequency = jsonFilePath1
                jsonRunways = jsonFilePath2
                
                #functions removing closed airports and adding additional information
                #if all three input files are not present, an error occurs here, hence except block begins
                remove_closed_airports(jsonAirport)
                remove_closed_other(jsonAirport,jsonFrequency)
                remove_closed_other(jsonAirport,jsonRunways)
                add_category_and_filter(jsonAirport)
                add_frequencies(jsonAirport, jsonFrequency)
            
                #------------------------------------------------------------------
                #creation of page for boxplots based on category of airport
                #all categories included hence increasing the functionality of the GUI
                label0 = Label(frame7, text='Select category of airport for a graphical representation'\
                               ' of its frequencies', bg='snow', fg='navy')
                label0.pack()
                button0 = Button(frame7, text="small_airport", width=20)
                button0.pack()
                button0.config(command=lambda button0=button0: 
                               [display_graph_small(), button0.config(state=NORMAL)])
                button1 = Button(frame7, text="medium_airport", width=20)
                button1.pack()
                button1.config(command=lambda button1=button1: 
                               [display_graph_medium(), button1.config(state=NORMAL)])
                button2 = Button(frame7, text="large_airport", width=20)
                button2.pack()
                button2.config(command=lambda button2=button2:
                               [display_graph_large(), button2.config(state=NORMAL)])
                blankLabel2 = Label(frame7, text='', bg='snow', fg='navy')
                blankLabel2.pack()
                
                button_return = Button(frame7, text='Back to previous')
                button_return.pack()
                button_return.config(command=lambda button_return=button_return: 
                                     [back_to_mean_mode(), button_return.config(state=NORMAL)])
                button_proceed1 = Button(frame7, text='Proceed to frequency correlation visualisation')
                button_proceed1.pack()
                button_proceed1.config(command=lambda button_proceed1=button_proceed1: 
                                       [show_all_category_graph(), button_proceed1.config(state=NORMAL)])
                Label25 = Label(frame7, text='Though the brief initially requested a visualisation'\
                                    ' for "small_airport" airports, visualisations for all three'\
                                        '\ncategories have been provided for comparisons and deeper'\
                                            ' analysis.', bg='snow', fg='navy')
                Label25.pack()
                
                #-----------------------------------------------------
                #generating the three boxplots based on category
                plot_box_graph_by_category(jsonAirport, 'small_airport')
                figureFilePath = plot_box_graph_by_category(jsonAirport, 'small_airport')
                figure = ImageTk.PhotoImage(Image.open(figureFilePath))
                label0 = Label(frame8, image = figure, bg='snow', fg='navy')
                label0.photo = figure 
                label0.pack()
             
        
                plot_box_graph_by_category(jsonAirport, 'medium_airport')
                figureFilePath = plot_box_graph_by_category(jsonAirport, 'medium_airport')
                figure = ImageTk.PhotoImage(Image.open(figureFilePath))
                label0 = Label(frame9, image = figure, bg='snow', fg='navy')
                label0.photo = figure 
                label0.pack()
          
                plot_box_graph_by_category(jsonAirport, 'large_airport')
                figureFilePath = plot_box_graph_by_category(jsonAirport, 'large_airport')
                figure = ImageTk.PhotoImage(Image.open(figureFilePath))
                label0 = Label(frame10, image = figure, bg='snow', fg='navy')
                label0.photo = figure 
                label0.pack()
                #-----------------------------------------------------
                #-----------------------------------------------------
                
                
                
                
                #-----------------------------------------------------
                #creation of page to show frequencies correlation graph
                button0 = Button(frame11, text="Back to previous", width=20, 
                                 command=back_to_single_graph)
                button0.pack()
                button1 = Button(frame11, text="Exit", width=20, command=exit_gui)
                button1.pack()
                blanklabel0 = Label(frame11, text='', bg='snow', fg='navy')
                blanklabel0.pack()
        
                frame12.pack(expand=True, fill=BOTH)
        
                #-----------------------------------------------------
                #generating scatter graph
                plot_scatter_graph_all_categories(jsonAirport)
                figureFilePath = plot_scatter_graph_all_categories(jsonAirport)
                figure = ImageTk.PhotoImage(Image.open(figureFilePath))
                label0 = Label(frame12, image = figure, bg='snow', fg='navy')
                label0.photo = figure 
                label0.pack()
                #-----------------------------------------------------
                
                #addition of a brief description of correlations
                label1 = Label(frame12, text='\nBrief overview of the output', font=("None",9,"bold"),
                               bg='snow', fg='navy')
                label1.pack()
                label2 = Label(frame12, text='A scatter graph was used to show frequencies for '\
                               'each category. Horizontal gridliens were plotted\nto show 100Mhz '\
                                   'bands. A colourmap was added to show correlations visually between'\
                                       ' bandings, and allow\nfor easier identification of relevant'\
                                           ' trends. The figure shows that all airport categories '\
                                               'have airports\nthat use frequencies in the lower'\
                                                   ' ends of the 0-100MHz and 100-200MHz bands. '\
                                                       'However, the medium_airports\ncategory has '\
                                                           'the majority of its airports with '\
                                                               'frequencies in the 200-400MHz band, '\
                                                                   'and has two airports\nabove that'\
                                                                       ' (at ~580MHz and ~680MHz). '\
                                                                           'The small_airport category'\
                                                                               ' also has two airports '\
                                                                                   'within the\n200-400MHz'\
                                                                                       ' band.', bg='snow'
                                                                                       , fg='navy')
                label2.pack()
                #-----------------------------------------------------
                
                
                #if generation of all these outputs is successful, the user is allowed to proceed
                stringVar4.set('Files prepared for analysis\nProceed to next page\n')
                button_proceed.config(state=NORMAL)
            
            
            #except block gives the user an instruction to try again due to incorrect files
            except:
                stringVar4.set('The three JSON files have been created and loaded into the same'\
                                   ' directory folder\nThey do not contain the datasets expected'\
                                       '\n\nTry again')
                button_proceed.config(state=DISABLED)
                button_restart.config(state=NORMAL)
      
         
        #checking input filepaths exist in the directory
        filePath0 = entry0.get()
        filePath1 = entry1.get()
        filePath2 = entry2.get()
        p0 = os.path.exists(filePath0)
        p1 = os.path.exists(filePath1)
        p2 = os.path.exists(filePath2)
        
        try:
            #if all filepaths exist and all end with csv, they are the correct format for conversion
            if p0 == True and (filePath0[filePath0.rindex('.')+1:] == 'csv'):
                if p1 == True and (filePath1[filePath1.rindex('.')+1:] == 'csv'):
                    if p2 == True and (filePath2[filePath2.rindex('.')+1:] == 'csv'):
                        button3.config(state=DISABLED)
                        blanklabel0 = Label(frame22, text='', bg='snow', fg='navy')
                        blankLabel0.pack()
                        #stops the user from changing their entry after they have input filepaths
                        entry0.config(state=DISABLED)
                        entry1.config(state=DISABLED)
                        entry2.config(state=DISABLED)
                        button0.config(state=DISABLED)
                        button1.config(state=DISABLED)
                        button2.config(state=DISABLED)
                        #confirms to user that their files are the correct format, and informs them of
                        #potential extended processing time
                        stringVar3.set('Files confirmed as CSVs')
                        stringVar4.set("This may take a few seconds once initialised...\n\n")
                        #call to initialise the conversion to json
                        convert_to_json_and_initial_processing()
                          
            else:
                #if files do not exist or are not CSVs, this feedback will be given
                stringVar3.set('The files are not in CSV format\n\n\nTry again')
                button_proceed.config(state=DISABLED)
                button3.config(state=DISABLED)#here
                button_restart.config(state=NORMAL)                   
        except:
            #except block allows user to retry their inputs
            stringVar3.set('The files are not correct, please check them again')
            button_proceed.config(state=DISABLED)
            button_restart.config(state=NORMAL)
            
    #---------------------------------------------------------
    #creation of page for loading files
    frame2.pack(expand=True, fill=BOTH)
    label0 = Label(frame2, text='Enter the filepath of the airports.csv file', bg='snow', fg='navy')
    label0.pack()
    entry0 = Entry(frame2, width=60)
    entry0.pack()
    button0 = Button(frame2,text="Browse", command=browse_file0)
    button0.pack()
    blankLabel0 = Label(frame2, text='', bg='snow', fg='navy')
    blankLabel0.pack()
    label3 = Label(frame2, text='Enter the filepath of the airport-frequencies.csv file',
                   bg='snow', fg='navy')
    label3.pack()
    entry1 = Entry(frame2, width=60)
    entry1.pack()
    button1 = Button(frame2, text="Browse", command=browse_file1)
    button1.pack()
    blankLabel1 = Label(frame2, text='', bg='snow', fg='navy')
    blankLabel1.pack()
    label5 = Label(frame2, text='Enter the filepath of the runways.csv', bg='snow', fg='navy')
    label5.pack()
    entry2 = Entry(frame2, width=60)
    entry2.pack()
    button2 = Button(frame2,text="Browse", command=browse_file2)
    button2.pack()
    blankLabel2 = Label(frame2, text='', bg='snow', fg='navy')
    blankLabel2.pack()
    frame22.pack(expand=True, fill=BOTH)
    frame23.pack(expand=True, fill=BOTH)
    button3 = Button(frame22, text='Prepare files', command=process_files, height=2)
    button3.pack()
    stringVar3 = StringVar()
    stringVar3.set("This may take a few seconds once initialised...")  
    label7 = Label(frame22, textvariable=stringVar3, bg='snow', fg='navy')
    label7.pack()
    stringVar4 = StringVar()
    stringVar4.set("\n\n")
    label23 = Label(frame22, textvariable=stringVar4, bg='snow', fg='navy')
    label23.pack()
    button_proceed = Button(frame23, text='Proceed to analysis', height=2, state=DISABLED)
    button_proceed.pack()
    button_proceed.config(command=lambda button_proceed=button_proceed: 
                          [generate_and_show_mean_mode_frequency(), button_proceed.config(state=DISABLED)])
    button_restart = Button(frame23, text='Retry', height=2, state=DISABLED)
    button_restart.pack()
    button_restart.config(command=lambda button_restart=button_restart: 
                          [retry_load(), button_restart.config(state=DISABLED)])
    
    #---------------------------------------------------------
 
    
 
    #---------------------------------------------------------
    #functions for exiting GUI and navigating between pages
    def exit_gui():
        master.destroy()
   
    def back_to_single_graph():
        frame5.pack_forget()
        frame11.pack_forget()
        frame12.pack_forget()
        frame9.pack_forget()
        frame10.pack_forget()
        frame7.pack(expand=True, fill=BOTH)
        frame8.pack(expand=True, fill=BOTH)
        stringVarTitle.set('Graphical representations of frequency by category')
    
    def show_all_category_graph():
        frame7.pack_forget()
        frame11.pack(expand=True, fill=BOTH)
        frame12.pack(expand=True, fill=BOTH)
        stringVarTitle.set('Graphical representation of frequency correlations\nbetween categories')
        
    def back_to_mean_mode():
        frame8.pack_forget()
        frame9.pack_forget()
        frame10.pack_forget()
        stringVarTitle.set('Mean, mode and median frequencies')
        frame7.pack_forget()
        frame5.pack(expand=True, fill=BOTH)
        frame50.place(height=600, width=600,x=0,y=180)
    #---------------------------------------------------------
    
    
    
    #---------------------------------------------------------
    #functions for displaying the graphs
    def display_graph_small():
        frame8.pack_forget()
        frame9.pack_forget()
        frame10.pack_forget()
        
        frame8.pack(expand=True,fill=BOTH)
        stringVarTitle.set('Category: "small_airport"')
        
    def display_graph_medium():
        frame8.pack_forget()
        frame9.pack_forget()
        frame10.pack_forget()
        
        frame9.pack(expand=True,fill=BOTH)
        stringVarTitle.set('Category: "medium_airport"')
    
    def display_graph_large():
        frame8.pack_forget()
        frame9.pack_forget()
        frame10.pack_forget()
        
        frame10.pack(expand=True,fill=BOTH)
        stringVarTitle.set('Category: "large_airport"')
    #---------------------------------------------------------
    
    
    #function with nested functions for generation mean, mode and median frequencies
    #also contains the building of the page
    def generate_and_show_mean_mode_frequency():
        
        values0 = mean_mode_median_frequency_by_category(jsonAirport, 'small_airport')
        values1 = mean_mode_median_frequency_by_category(jsonAirport, 'medium_airport')
        values2 = mean_mode_median_frequency_by_category(jsonAirport, 'large_airport')
        
        #-----------------------------------------------------
        #building of mean, mode, median frequencies by category section of page
        frame2.pack_forget()
        start_button1.pack_forget()
        frame5.pack(expand=True, fill=BOTH)
        stringVarTitle.set('Mean, mode and median frequencies')
        label200 = Label(frame5, text='\nThough the brief initially requested the mean, mode'\
                         ' and median frequencies for "large_airport" airports and\nfrequencies'\
                             ' greater than 100Mhz, figures for all three categories and range '\
                                 'inputs have been provided for\ncomparisons and deeper analysis.\n', 
                                 bg='snow', fg='navy')
        label200.pack()
        label0 = Label(frame5, text='Mean, mode and median frequencies by category', bg='snow', fg='navy')
        label0.pack()

        label1 = Label(frame5, text=f'For type: small_airport:\n Mean = {values0[0]}MHz'\
                       f'\n Mode = {values0[1]}MHz\n Median = {values0[2]}MHz', bg='snow', fg='navy')
        label1.place(x=90,y=100)
        
        label1 = Label(frame5, text=f'For type: medium_airport:\n Mean = {values1[0]}MHz'\
                       f'\n Mode = {values1[1]}MHz\n Median = {values1[2]}MHz', bg='snow', fg='navy')
        label1.place(x=230,y=100)
        
        label2 = Label(frame5, text=f' For type: large_airport: \n Mean = {values2[0]}MHz'\
                       f'\n Mode = {values2[1]}MHz\n Median = {values2[2]}MHz', 
                       bg='snow', fg='navy', borderwidth=2, relief='ridge')
       
        label2.place(x=390,y=100)
        #-----------------------------------------------------
        


        #-----------------------------------------------------------------------
        #function for computing ranges for mean, mode, median frequencies
        #user is able to input values for added functionality, but it defaults to 100Mhz
        def mean_mode_frequency_range():
            #try excepts for bounds with sentinels of 0 and 100,000 if the user leaves field empty
            try:   
                lowerBound = float(entry001.get())
            except:
                if entry001.get() == '':
                    lowerBound = 0.0
                else:
                    pass
            try:
                upperBound = float(entry011.get())
            except:
                if entry011.get() == '':
                    upperBound = 100000.0
                else:
                    pass
            
            #try except to catch if input is not a number
            try:
                values = mean_mode_median_frequency_by_range(jsonAirport, lowerBound, upperBound)  
                #if mode produces no values, range input does not contain any values
                if values[1] == False:
                    stringVar0.set('Bounds out of frequency range\n\n\n')
                elif lowerBound == 0.0 and upperBound != 100000.0:
                    stringVar0.set(f'For airports with frequencies less than {upperBound}MHz:\n'\
                                   f' Mean = {values[0]}MHz\n Mode = {values[1]}MHz\n Median ='\
                                       f' {values[2]}MHz')
                elif upperBound == 100000.0 and lowerBound != 0.0:
                    stringVar0.set(f'For airports with frequencies greater than {lowerBound}MHz:'\
                                   f'\n Mean = {values[0]}MHz\n Mode = {values[1]}MHz\n Median = '\
                                       f'{values[2]}MHz')
                elif lowerBound == 0 and upperBound == 100000.0:
                    stringVar0.set(f'For all airports:\n Mean = {values[0]}MHz\n Mode = {values[1]}'\
                                   f'MHz\n Median = {values[2]}MHz')
                else:
                    stringVar0.set(f'For airports with frequencies in range {lowerBound}MHz < x <'\
                                   f' {upperBound}MHz:\n Mean = {values[0]}MHz\n Mode = {values[1]}'\
                                       f'MHz\n Median = {values[2]}MHz')
            except:
                stringVar0.set('Input value/s is not a number\n\n\n')
        #------------------------------------------------------------
        
        
        
        
        #-------------------------------------------------------------
        #building of mean, mode, median frequencies by range section of page
        frame50.place(height=600, width=600,x=0,y=180)
        label01 = Label(frame50, text='Mean, mode and median frequencies for frequency range', 
                        bg='snow', fg='navy')
        label01.pack()
        label102 = Label(frame50, text='Set lower bound (in MHz)', bg='snow', fg='navy')
        label102.pack()
        entry001 = Entry(frame50, width=30)
        entry001.insert(0, '100')
        entry001.pack()
        label011 = Label(frame50, text='Set upper bound (in MHz)', bg='snow', fg='navy')
        label011.pack()
        entry011 = Entry(frame50, width=30)
        entry011.pack()
        blankLabel011 = Label(frame50, text='', bg='snow', fg='navy')
        blankLabel011.pack()
        button001 = Button(frame50, text="Compute", width=20)
        button001.pack()
        button001.config(command=lambda button001=button001: [mean_mode_frequency_range(), 
                                                              button001.config(state=NORMAL)])
        values = mean_mode_median_frequency_by_range(jsonAirport, 100,10000)
        stringVar0 = StringVar()
        stringVar0.set(f'For airports with frequencies greater than 100Mhz:'\
                                   f'\n Mean = {values[0]}MHz\n Mode = {values[1]}MHz\n Median = '\
                                       f'{values[2]}MHz') 
        label021 = Label(frame50, textvariable=stringVar0, bg='snow', fg='navy')
        label021.pack()
        button_proceed = Button(frame50, text='Proceed to visualisations')
        button_proceed.pack()
        button_proceed.config(command=lambda button_proceed=button_proceed: 
                              [back_to_single_graph(), button_proceed.config(state=NORMAL)])
        #-------------------------------------------------------------
        


master.resizable(False, False)
master.mainloop()
