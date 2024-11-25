import numpy as np
import pandas as pd
import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import math

pd.options.display.max_rows = None
pd.options.display.max_columns = None

def prepareModel():
    #import csv dataset on amazon reviews
    trainDataset = pd.read_csv("TrainData/AllProductReviews.csv")

    #select columns we are concerned with
    trainDataset = trainDataset[["ReviewBody", "ReviewStar"]]

    #set rating of 1 to 5 to match our polarity of -1 to 1 with:
    # 1 star -> -0.8
    # 2 star -> -0.4
    # 3 star -> 0
    # 4 star -> 0.4
    # 5 star -> 0.8
    trainDataset.loc[trainDataset["ReviewStar"] == 1, "ReviewStar"] = -0.8
    trainDataset.loc[trainDataset["ReviewStar"] == 2, "ReviewStar"] = -0.4
    trainDataset.loc[trainDataset["ReviewStar"] == 3, "ReviewStar"] = 0.0
    trainDataset.loc[trainDataset["ReviewStar"] == 4, "ReviewStar"] = 0.4
    trainDataset.loc[trainDataset["ReviewStar"] == 5, "ReviewStar"] = 0.8

    #replace empty strings with nan
    #trainDataset.replace("", np.nan, inplace=True)

    #need to vectorise text as ml models cannot take in strings
    #add new column to dataframe
    trainDataset.insert(loc=1, column="VectorisedReview", value=["" for i in range(trainDataset.shape[0])])

  

    #vectorise the text reviews so the model can understand them
    vectorisedOutput = vectoriser.fit_transform(trainDataset["ReviewBody"])

    #rename ReviewStar to be ReviewPolarity
    trainDataset = trainDataset.rename(columns={"ReviewStar": "ReviewPolarity"})


    #train model on the test data
    rf.fit(vectorisedOutput, trainDataset["ReviewPolarity"])

    print("fitting done")


def computeSentiment(text):
    return rf.predict(vectoriser.transform([text]))



#defining a function here that returns performance metrics based on the cleaned output data
def calculateAccPrecRecF1(outputData):
    
    #to get accuracy - taking all values that are within the range and divide by total predictions 
    #with fail safe behaviour setting accuracy to 0 if divisibility fails
    if (len(outputData) != 0):
        outputAccuracy = round((len(outputData[(outputData["Diff"] <= 0.2)])) / len(outputData) * 100, 3)
    else:
        outputAccuracy = 0.0

    #since the classification here is multinomial rather than binary, to calculate precision,
    #recall and F1-score involves splitting each classification and finding the True Positives,
    #False Positives, True Negatives and False Negatives as selected vs the rest. Then combining
    #the outcome.

    #for Strongly Positive firstly - finding all true positives and false positives
    SP_output_TP_and_FP = outputData[(outputData["Predicted"] >= 0.6)]
    SP_output_TP = len(SP_output_TP_and_FP[(SP_output_TP_and_FP["Actual"] == 0.8)])
    SP_output_FP = len(SP_output_TP_and_FP[(SP_output_TP_and_FP["Actual"] != 0.8)])

    #for Strongly Positive - all true negatives and false negatives
    SP_output_TN_and_FN = outputData[(outputData["Predicted"] <= 0.6)]
    SP_output_TN = len(SP_output_TN_and_FN[(SP_output_TN_and_FN["Actual"] != 0.8)])
    SP_output_FN = len(SP_output_TN_and_FN[(SP_output_TN_and_FN["Actual"] == 0.8)])



    #for Positive - finding all true positives and false positives
    P_output_TP_and_FP = outputData[(outputData["Predicted"] <= 0.6) & (outputData["Predicted"] >= 0.2)]
    P_output_TP = len(P_output_TP_and_FP[(P_output_TP_and_FP["Actual"] == 0.4)])
    P_output_FP = len(P_output_TP_and_FP[(P_output_TP_and_FP["Actual"] != 0.4)])

    #for Positive - all true negatives and false negatives
    P_output_TN_and_FN = outputData[(outputData["Predicted"] >= 0.6) | (outputData["Predicted"] <= 0.2)]
    P_output_TN = len(P_output_TN_and_FN[(P_output_TN_and_FN["Actual"] != 0.4)])
    P_output_FN = len(P_output_TN_and_FN[(P_output_TN_and_FN["Actual"] == 0.4)])


    #for Neutral - finding all true positives and false positives
    Neu_output_TP_and_FP = outputData[(outputData["Predicted"] <= 0.2) & (outputData["Predicted"] >= -0.2)]
    Neu_output_TP = len(Neu_output_TP_and_FP[(Neu_output_TP_and_FP["Actual"] == 0.0)])
    Neu_output_FP = len(Neu_output_TP_and_FP[(Neu_output_TP_and_FP["Actual"] != 0.0)])

    #for Neutral - finding all true negatives and false negatives
    Neu_output_TN_and_FN = outputData[(outputData["Predicted"] >= 0.2) | (outputData["Predicted"] <= -0.2)]
    Neu_output_TN = len(Neu_output_TN_and_FN[(Neu_output_TN_and_FN["Actual"] != 0.0)])
    Neu_output_FN = len(Neu_output_TN_and_FN[(Neu_output_TN_and_FN["Actual"] == 0.0)])


    #for Negative - finding all true positives and false positives
    Neg_output_TP_and_FP = outputData[(outputData["Predicted"] >= -0.6) & (outputData["Predicted"] <= -0.2)]
    Neg_output_TP = len(Neg_output_TP_and_FP[(Neg_output_TP_and_FP["Actual"] == -0.4)])
    Neg_output_FP = len(Neg_output_TP_and_FP[(Neg_output_TP_and_FP["Actual"] != -0.4)])

    #for Negative - finding all true negatives and false negatives
    Neg_output_TN_and_FN = outputData[(outputData["Predicted"] <= -0.6) | (outputData["Predicted"] >= -0.2)]
    Neg_output_TN = len(Neg_output_TN_and_FN[(Neg_output_TN_and_FN["Actual"] != -0.4)])
    Neg_output_FN = len(Neg_output_TN_and_FN[(Neg_output_TN_and_FN["Actual"] == -0.4)])

    #for Strongly Negative - finding all true positives and false positives
    SNeg_output_TP_and_FP = outputData[(outputData["Predicted"] <= -0.6)]
    SNeg_output_TP = len(SNeg_output_TP_and_FP[(SNeg_output_TP_and_FP["Actual"] == -0.8)])
    SNeg_output_FP = len(SNeg_output_TP_and_FP[(SNeg_output_TP_and_FP["Actual"] != -0.8)])

    #for Strongly Negative - finding all true negatives and false negatives
    SNeg_output_TN_and_FN = outputData[(outputData["Predicted"] >= -0.6)]
    SNeg_output_TN = len(SNeg_output_TN_and_FN[(SNeg_output_TN_and_FN["Actual"] != -0.8)])
    SNeg_output_FN = len(SNeg_output_TN_and_FN[(SNeg_output_TN_and_FN["Actual"] == -0.8)])

    ''' this check here was to ensure they summed to the same count
    SP_total = SP_output_TP + SP_output_FP + SP_output_TN + SP_output_FN
    P_total = P_output_TP + P_output_FP + P_output_TN + P_output_FN
    Neu_total = Neu_output_TP + Neu_output_FP + Neu_output_TN + Neu_output_FN
    Neg_total = Neg_output_TP + Neg_output_FP + Neg_output_TN + Neg_output_FN
    SNeg_total = SNeg_output_TP + SNeg_output_FP + SNeg_output_TN + SNeg_output_FN
    outputLength = len(outputData)
    '''

    #in order to calculate Precision, Recall and F1-Score, the weighted averages needed to be
    #calculated. The weighting factor for each will be equal to the proportion of actual
    #instances compared to the total number of instances. with fail safe for divisibility by 0.
    if(len(outputData) != 0):
        SP_weight = len(outputData[(outputData["Actual"] == 0.8)]) / (len(outputData))
        P_weight = len(outputData[(outputData["Actual"] == 0.4)]) / (len(outputData))
        Neu_weight = len(outputData[(outputData["Actual"] == 0.0)]) / (len(outputData))
        Neg_weight = len(outputData[(outputData["Actual"] == -0.4)]) / (len(outputData))
        SNeg_weight = len(outputData[(outputData["Actual"] == -0.8)]) / (len(outputData))
    else:
        SP_weight, P_weight, Neu_weight, Neg_weight, SNeg_weight = 0.0, 0.0, 0.0, 0.0, 0.0
    
    ''' this check here was to ensure that all weights add to 1
    Total_weights = SP_weight + P_weight + Neu_weight + Neg_weight + SNeg_weight
    '''

    #first calculating Precision for each class (with some fail safe behaviour in the case of divisibility by 0
    #thus setting the Precision to 0 in this case)
    if (SP_output_TP + SP_output_FP != 0):
        SP_precision = SP_output_TP / (SP_output_TP + SP_output_FP)
    else:
        SP_precision = 0.0

    if (P_output_TP + P_output_FP != 0):
        P_precision = P_output_TP / (P_output_TP + P_output_FP)
    else:
        P_precision = 0.0

    if (Neu_output_TP + Neu_output_FP != 0):
        Neu_precision = Neu_output_TP / (Neu_output_TP + Neu_output_FP)
    else:
        Neu_precision = 0.0

    if (Neg_output_TP + Neg_output_FP != 0):
        Neg_precision = Neg_output_TP / (Neg_output_TP + Neg_output_FP)
    else:
        Neg_precision = 0.0
    
    if (SNeg_output_TP + SNeg_output_FP != 0):
        SNeg_precision = SNeg_output_TP / (SNeg_output_TP + SNeg_output_FP)
    else:
        SNeg_precision = 0.0

    #and the weighted and unweighted overall precision
    Weighted_precision = round(((SP_precision * SP_weight) +  (P_precision * P_weight) + (Neu_precision * Neu_weight) + (Neg_precision * Neg_weight) + (SNeg_precision * SNeg_weight)) * 100, 3) 
    Unweighted_precision = round((SP_precision + P_precision + Neu_precision + Neg_precision + SNeg_precision) * 100 / 5 ,3)

    #now calculating Recall for each class (with some fail safe behaviour in the case of divisibility by 0
    #thus setting the Recall to 0 in this case)
    if (SP_output_TP + SP_output_FN != 0):
        SP_recall = SP_output_TP / (SP_output_TP + SP_output_FN)
    else:
        SP_recall = 0.0
    
    if (P_output_TP + P_output_FN != 0):
        P_recall = P_output_TP / (P_output_TP + P_output_FN)
    else:
        P_recall = 0.0

    if (Neu_output_TP + Neu_output_FN != 0):
        Neu_recall = Neu_output_TP / (Neu_output_TP + Neu_output_FN)
    else:
        Neu_recall = 0.0
    
    if (Neg_output_TP + Neg_output_FN != 0):
        Neg_recall = Neg_output_TP / (Neg_output_TP + Neg_output_FN)
    else:
        Neg_recall = 0.0

    if (SNeg_output_TP + SNeg_output_FN != 0):
        SNeg_recall = SNeg_output_TP / (SNeg_output_TP + SNeg_output_FN)
    else:
        SNeg_recall = 0.0

    #and the weighted and unweighted overall Recall
    Weighted_recall = round(((SP_recall * SP_weight) +  (P_recall * P_weight) + (Neu_recall * Neu_weight) + (Neg_recall * Neg_weight) + (SNeg_recall * SNeg_weight)) * 100, 3) 
    Unweighted_recall = round((SP_recall + P_recall + Neu_recall + Neg_recall + SNeg_recall) * 100 / 5 ,3)

    #and finally the F1-score for each class (with some fail safe behaviour in the case of divisibility by 0
    #thus setting the F1 to 0 in this case)
    if (SP_precision + SP_recall != 0):
        SP_F1 = 2 * ((SP_precision * SP_recall) / (SP_precision + SP_recall))
    else:
        SP_F1 = 0.0

    if (P_precision + P_recall != 0):
        P_F1 = 2 * ((P_precision * P_recall) / (P_precision + P_recall))
    else:
        P_F1 = 0.0

    if (Neu_precision + Neu_recall != 0):
        Neu_F1 = 2 * ((Neu_precision * Neu_recall) / (Neu_precision + Neu_recall))
    else:
        Neu_F1 = 0.0

    if (Neg_precision + Neg_recall != 0):
        Neg_F1 = 2 * ((Neg_precision * Neg_recall) / (Neg_precision + Neg_recall))
    else:
        Neg_F1 = 0.0

    if (SNeg_precision + SNeg_recall != 0):
        SNeg_F1 = 2 * ((SNeg_precision * SNeg_recall) / (SNeg_precision + SNeg_recall))
    else:
        SNeg_F1 = 0.0


    #and the weighted and unweighted overall F1-score
    Weighted_F1 = round(((SP_F1 * SP_weight) +  (P_F1 * P_weight) + (Neu_F1 * Neu_weight) + (Neg_F1 * Neg_weight) + (SNeg_F1 * SNeg_weight)) * 100, 3) 
    Unweighted_F1 = round((SP_F1 + P_F1 + Neu_F1 + Neg_F1 + SNeg_F1) * 100 / 5 ,3)

    return outputAccuracy, Weighted_precision, Weighted_recall, Weighted_F1, Unweighted_precision, Unweighted_recall, Unweighted_F1

#this function returns how many answers of Strongly Negative, Negative, Neutral
#Positive and Strongly Positive there are in data
def returnProportions(outputData):
    SP_Count = len(outputData[outputData["Actual"] == 0.8])
    P_Count = len(outputData[outputData["Actual"] == 0.4])
    Neu_Count = len(outputData[outputData["Actual"] == 0.0])
    Neg_Count = len(outputData[outputData["Actual"] == -0.4])
    SNeg_Count = len(outputData[outputData["Actual"] == -0.8])

    return SP_Count, P_Count, Neu_Count, Neg_Count, SNeg_Count

#intiialise vectoriser
vectoriser = TfidfVectorizer()

#declare random forest model
rf = RandomForestRegressor(n_estimators=100)

#train the model
prepareModel()

#-------------------------------------
#get current time in milliseconds, so that time at end of code run can be compared - will not count pre-training time to this
start_t = round(time.time()*1000)

#import dataset
surveyDataset = pd.read_csv('SurveyDatasets/Black Mental Health in England & Wales_October 6, 2024_05.28.csv', delimiter=',')

#filter responses that did not finish
surveyDataset = surveyDataset[surveyDataset["Finished"].str.contains("T")]

#drop columns that are not being used
surveyDataset = surveyDataset.drop(['StartDate', 'EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)',
                                    'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName','RecipientFirstName', 
                                    'RecipientEmail', 'ExternalReference', 'LocationLatitude', 'LocationLongitude', 
                                    'DistributionChannel', 'UserLanguage'], axis='columns')



# for all part b questions, the worded answers of:
# [Strongly Negative, Negative, Neutral, Positive, Strongly Positive] will be replaced with
# [ -1.0, -0.5, 0, 0.5, 1.0] or [-0.8, -0.4, 0, 0.4, 0.8] TBD

#using a for loop and pandas insert to add empty columns for computed sentiment and string length
counter = 0
for i in range(6,65,5):
    q = str(i - 5 - counter)
    qNumA = "Q" + q + "aNum"
    qNumALength = "Q" + q + "aLength"
    surveyDataset.insert(loc=i, column=qNumA, value=['' for i in range(surveyDataset.shape[0])])
    surveyDataset.insert(loc=i+1, column=qNumALength, value=['' for i in range(surveyDataset.shape[0])])

    qNumB = str(i + 3 - 8 - counter)
    qNumB = "Q" + qNumB + "bNum"
    surveyDataset.insert(loc=i+3, column=qNumB, value=['' for i in range(surveyDataset.shape[0])])
    counter += 4


# adding the numerical values (TODO review these) for each sentiment score
for i in range(1,13):
    q = str(i)
    q = "Q" + q + "b"
    qNumB = q + "Num"
    surveyDataset.loc[surveyDataset[q] == "Strongly Positive", qNumB] = 0.8
    surveyDataset.loc[surveyDataset[q] == "Positive", qNumB] = 0.4
    surveyDataset.loc[surveyDataset[q] == "Neutral", qNumB] = 0.0
    surveyDataset.loc[surveyDataset[q] == "Negative", qNumB] = -0.4
    surveyDataset.loc[surveyDataset[q] == "Strongly Negative", qNumB] = -0.8


#iterating through the questions and generating the sentiment for each answered response
#computing the length of each string for part a answers
for i in range(1,13):
    q = str(i)
    q = "Q" + q + "a"
    qNumA = q + "Num"
    qLength = q + "Length"
    for index, row in surveyDataset.iterrows():
        textAnswer = row[q]
        if (textAnswer != textAnswer) :
            #ignore if nan
            pass
        else:
            surveyDataset.loc[index, qNumA] = computeSentiment(textAnswer)
            surveyDataset.loc[index,qLength] = len(textAnswer)



#make a new dataframe for computing results
outputData = surveyDataset.iloc[:,[6,7,9]].rename(columns={"Q1aNum": "Predicted", "Q1aLength": "Str Length", "Q1bNum": "Actual"})


#iterating over each column, renaming it and appending it to the end of surveyDataset_outputData
counter2 = 0
for i in range(10,65,5):
    q = str(i-8 - 4*counter2)
    qa = "Q" + q + "aNum"
    qb = "Q" + q + "bNum"
    qLength = "Q" + q + "aLength"
    datasetToAppend = surveyDataset.iloc[:,[i+1,i+2, i+4]]
    datasetToAppend = datasetToAppend.rename(columns={qa: "Predicted", qLength: "Str Length", qb: "Actual"} )
    outputData = pd.concat([outputData, datasetToAppend], ignore_index=True)
    counter2 += 1

#removing all NaN or empty data
outputData.replace('', np.nan, inplace=True)
outputData.dropna(inplace=True)
outputData.reset_index(drop=True, inplace=True)


#adding new column that will compute difference between actual and predicted squared
outputData["Diff"] = np.nan

for index, row in outputData.iterrows():
    output = abs(row["Actual"] - row["Predicted"])
    outputData.loc[index, "Diff"] = output


#calling the function to compute accuracy, and weighted/unweighted precision, recall and F1 for entire dataset
totalAccuracy, totalWeighted_precision, totalWeighted_recall, totalWeighted_F1, totalUnweighted_precision, totalUnweighted_recall, totalUnweighted_F1 = calculateAccPrecRecF1(outputData)

#calling function to return the Strongly Positive, Positive, Neutral, Negative, Strongly Negative counts
totalSP_count, totalP_count, totalNeu_count, totalNeg_count, totalSNeg_count = returnProportions(outputData)



#TODO this range may change
#performance of algorithms may be influenced by length of string
#current minimum and maximum string length is 4 characters and 760 characters respectively
#will split the dataset into different dataframes for intervals of 100 characters (TODO or 50???)

#for string length range 0 < x < 100 characters
outputData_0_100 = outputData[outputData["Str Length"] < 100 ]
Accuracy_0_100, Weighted_precision_0_100, Weighted_recall_0_100, Weighted_F1_0_100, Unweighted_precision_0_100, Unweighted_recall_0_100, Unweighted_F1_0_100 = calculateAccPrecRecF1(outputData_0_100)
SPCount_0_100, PCount_0_100, NeuCount_0_100, NegCount_0_100, SNegCount_0_100 = returnProportions(outputData_0_100)

#for string length range 100 <= x < 200 characters
outputData_100_200 = outputData[outputData["Str Length"] >= 100 ]
outputData_100_200 = outputData_100_200[outputData_100_200["Str Length"] < 200]
Accuracy_100_200, Weighted_precision_100_200, Weighted_recall_100_200, Weighted_F1_100_200, Unweighted_precision_100_200, Unweighted_recall_100_200, Unweighted_F1_100_200 = calculateAccPrecRecF1(outputData_100_200)
SPCount_100_200, PCount_100_200, NeuCount_100_200, NegCount_100_200, SNegCount_100_200 = returnProportions(outputData_100_200)

#for string length range 200 <= x < 300 characters
outputData_200_300 = outputData[outputData["Str Length"] >= 200 ]
outputData_200_300 = outputData_200_300[outputData_200_300["Str Length"] < 300]
Accuracy_200_300, Weighted_precision_200_300, Weighted_recall_200_300, Weighted_F1_200_300, Unweighted_precision_200_300, Unweighted_recall_200_300, Unweighted_F1_200_300 = calculateAccPrecRecF1(outputData_200_300)
SPCount_200_300, PCount_200_300, NeuCount_200_300, NegCount_200_300, SNegCount_200_300 = returnProportions(outputData_200_300)

#for string length range 300 <= x < 400 characters
outputData_300_400 = outputData[outputData["Str Length"] >= 300 ]
outputData_300_400 = outputData_300_400[outputData_300_400["Str Length"] < 400]
Accuracy_300_400, Weighted_precision_300_400, Weighted_recall_300_400, Weighted_F1_300_400, Unweighted_precision_300_400, Unweighted_recall_300_400, Unweighted_F1_300_400 = calculateAccPrecRecF1(outputData_300_400)
SPCount_300_400, PCount_300_400, NeuCount_300_400, NegCount_300_400, SNegCount_300_400 = returnProportions(outputData_300_400)

#for string length range 400 <= x < 500 characters
outputData_400_500 = outputData[outputData["Str Length"] >= 400 ]
outputData_400_500 = outputData_400_500[outputData_400_500["Str Length"] < 500]
Accuracy_400_500, Weighted_precision_400_500, Weighted_recall_400_500, Weighted_F1_400_500, Unweighted_precision_400_500, Unweighted_recall_400_500, Unweighted_F1_400_500 = calculateAccPrecRecF1(outputData_400_500)
SPCount_400_500, PCount_400_500, NeuCount_400_500, NegCount_400_500, SNegCount_400_500 = returnProportions(outputData_400_500)

#for string length range 500 <= x < 600 characters
outputData_500_600 = outputData[outputData["Str Length"] >= 500 ]
outputData_500_600 = outputData_500_600[outputData_500_600["Str Length"] < 600]
Accuracy_500_600, Weighted_precision_500_600, Weighted_recall_500_600, Weighted_F1_500_600, Unweighted_precision_500_600, Unweighted_recall_500_600, Unweighted_F1_500_600 = calculateAccPrecRecF1(outputData_500_600)
SPCount_500_600, PCount_500_600, NeuCount_500_600, NegCount_500_600, SNegCount_500_600 = returnProportions(outputData_500_600)

#for string length range 600 <= x < 700 characters
outputData_600_700 = outputData[outputData["Str Length"] >= 600 ]
outputData_600_700 = outputData_600_700[outputData_600_700["Str Length"] < 700]
Accuracy_600_700, Weighted_precision_600_700, Weighted_recall_600_700, Weighted_F1_600_700, Unweighted_precision_600_700, Unweighted_recall_600_700, Unweighted_F1_600_700 = calculateAccPrecRecF1(outputData_600_700)
SPCount_600_700, PCount_600_700, NeuCount_600_700, NegCount_600_700, SNegCount_600_700 = returnProportions(outputData_600_700)

#for string length range 700 <= x < 800 characters
outputData_700_800 = outputData[outputData["Str Length"] >= 700 ]
outputData_700_800 = outputData_700_800[outputData_700_800["Str Length"] < 800]
Accuracy_700_800, Weighted_precision_700_800, Weighted_recall_700_800, Weighted_F1_700_800, Unweighted_precision_700_800, Unweighted_recall_700_800, Unweighted_F1_700_800 = calculateAccPrecRecF1(outputData_700_800)
SPCount_700_800, PCount_700_800, NeuCount_700_800, NegCount_700_800, SNegCount_700_800 = returnProportions(outputData_700_800)


#get time in milliseconds after processing
end_t = round(time.time()*1000)
#generate the time difference
time_diff = end_t - start_t

#creating a list of lists that will tell us how many positivity scores of each string length there are
stringLengthLists = [
    ["1 - 99 Characters", SPCount_0_100, PCount_0_100, NeuCount_0_100, NegCount_0_100, SNegCount_0_100, len(outputData_0_100)],
    ["100 - 199 Characters", SPCount_100_200, PCount_100_200, NeuCount_100_200, NegCount_100_200, SNegCount_100_200, len(outputData_100_200)],
    ["200 - 299 Characters", SPCount_200_300, PCount_200_300, NeuCount_200_300, NegCount_200_300, SNegCount_200_300, len(outputData_200_300)],
    ["300 - 399 Characters", SPCount_300_400, PCount_300_400, NeuCount_300_400, NegCount_300_400, SNegCount_300_400, len(outputData_300_400)],
    ["400 - 499 Characters", SPCount_400_500, PCount_400_500, NeuCount_400_500, NegCount_400_500, SNegCount_400_500, len(outputData_400_500)],
    ["500 - 599 Characters", SPCount_500_600, PCount_500_600, NeuCount_500_600, NegCount_500_600, SNegCount_500_600, len(outputData_500_600)],
    ["600 - 699 Characters", SPCount_600_700, PCount_600_700, NeuCount_600_700, NegCount_600_700, SNegCount_600_700, len(outputData_600_700)],
    ["700 + Characters", SPCount_700_800, PCount_700_800, NeuCount_700_800, NegCount_700_800, SNegCount_700_800, len(outputData_700_800)],
    ["Total  Dataset", totalSP_count, totalP_count, totalNeu_count, totalNeg_count, totalSNeg_count, len(outputData)],
]

stringLengths = pd.DataFrame(stringLengthLists, columns=["Answer Length", "Strongly Positive Count", "Positive Count", "Neutral Count", "Negative Count", "Strongly Negative Count", "Overall Count"])
stringLengths = stringLengths.reset_index(drop=True)


stringLengths = pd.DataFrame(stringLengthLists, columns=["Answer Length", "Strongly Positive Count", "Positive Count", "Neutral Count", "Negative Count", "Strongly Negative Count", "Overall Count"])
stringLengths = stringLengths.reset_index(drop=True)

#this will be used for calculating mean and standard deviation
stringLengthList = outputData["Str Length"].to_list()
stringLengthMean = round(sum(stringLengthList)/len(stringLengthList),0)

#initilisae standard deviation to 0
stringLengthStandardDeviation = 0

#loop through all values and add (x - mu)^2 to it
for i in range (0, len(stringLengthList)):
    stringLengthStandardDeviation = stringLengthStandardDeviation + (stringLengthList[i] - stringLengthMean)**2

#to complete standard deviation, divide by N and then square root
stringLengthStandardDeviation = round(math.sqrt(stringLengthStandardDeviation/len(stringLengthList)),0)

#creating a list of lists that will be converted to dataframe that will be tabulated for readable output
finalResultsList = [
    ["0 - 99 Characters", len(outputData_0_100), f"{Accuracy_0_100} %", f"{Weighted_precision_0_100} %", f"{Weighted_recall_0_100} %", f"{Weighted_F1_0_100} %", f"{Unweighted_precision_0_100} %", f"{Unweighted_recall_0_100} %", f"{Unweighted_F1_0_100} %"],
    ["100 - 199 Characters", len(outputData_100_200), f"{Accuracy_100_200} %", f"{Weighted_precision_100_200} %", f"{Weighted_recall_100_200} %", f"{Weighted_F1_100_200} %", f"{Unweighted_precision_100_200} %", f"{Unweighted_recall_100_200} %", f"{Unweighted_F1_100_200} %"],
    ["200 - 299 Characters", len(outputData_200_300), f"{Accuracy_200_300} %", f"{Weighted_precision_200_300} %", f"{Weighted_recall_200_300} %", f"{Weighted_F1_200_300} %", f"{Unweighted_precision_200_300} %", f"{Unweighted_recall_200_300} %", f"{Unweighted_F1_200_300} %"],
    ["300 - 399 Characters", len(outputData_300_400), f"{Accuracy_300_400} %", f"{Weighted_precision_300_400} %", f"{Weighted_recall_300_400} %", f"{Weighted_F1_300_400} %", f"{Unweighted_precision_300_400} %", f"{Unweighted_recall_300_400} %", f"{Unweighted_F1_300_400} %"],
    ["400 - 499 Characters", len(outputData_400_500), f"{Accuracy_400_500} %", f"{Weighted_precision_400_500} %", f"{Weighted_recall_400_500} %", f"{Weighted_F1_400_500} %", f"{Unweighted_precision_400_500} %", f"{Unweighted_recall_400_500} %", f"{Unweighted_F1_400_500} %"],
    ["500 - 599 Characters", len(outputData_500_600), f"{Accuracy_500_600} %", f"{Weighted_precision_500_600} %", f"{Weighted_recall_500_600} %", f"{Weighted_F1_500_600} %", f"{Unweighted_precision_500_600} %", f"{Unweighted_recall_500_600} %", f"{Unweighted_F1_500_600} %"],
    ["600 - 699 Characters", len(outputData_600_700), f"{Accuracy_600_700} %", f"{Weighted_precision_600_700} %", f"{Weighted_recall_600_700} %", f"{Weighted_F1_600_700} %", f"{Unweighted_precision_600_700} %", f"{Unweighted_recall_600_700} %", f"{Unweighted_F1_600_700} %"],
    ["700 + Characters", len(outputData_700_800), f"{Accuracy_700_800} %", f"{Weighted_precision_700_800} %", f"{Weighted_recall_700_800} %", f"{Weighted_F1_700_800} %", f"{Unweighted_precision_700_800} %", f"{Unweighted_recall_700_800} %", f"{Unweighted_F1_700_800} %"],
    ["Total Dataset", len(outputData), f"{totalAccuracy} %", f"{totalWeighted_precision} %", f"{totalWeighted_recall} %", f"{totalWeighted_F1} %", f"{totalUnweighted_precision} %", f"{totalUnweighted_recall} %", f"{totalUnweighted_F1} %"],
]

#converting the list of lists into a dataframe and dropping the index column
finalResults = pd.DataFrame(finalResultsList, columns=["Answer Length", "Count", "Accuracy", "Weighted Precision", "Weighted Recall", "Weighted F1-Score", "Unwweighted Precision", "Unweighted Recall", "Unweighted F1-Score"])
finalResults = finalResults.reset_index(drop=True)

print()
print()
print("Average string length: ", stringLengthMean)
print("Standard deviation of string lengths: ", stringLengthStandardDeviation)
print("Two standard deviations range is: ", stringLengthMean - 2*stringLengthStandardDeviation, " < x < ", stringLengthMean + 2*stringLengthStandardDeviation, " characters")
print()
print(stringLengths)
print()
print("--------------------------------------------------------------------------")
print()
print(finalResults)

print("Total time to generate results is ", time_diff, "ms")




