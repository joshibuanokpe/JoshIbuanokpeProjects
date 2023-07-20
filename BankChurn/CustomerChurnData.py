import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.max_rows = None
pd.options.display.max_columns = None
# Support functions
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from scipy.stats import uniform

# Fit models
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
#from xgboost import XGBClassifier

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

# Scoring functions
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve


dfTrain = pd.read_csv('/Users/jibuanok/Documents/u/DM/BankChurnersTrain.csv', delimiter=',')
dfTrainSet = pd.read_csv('/Users/jibuanok/Documents/u/DM/BankChurnersTrain.csv', delimiter=',')
dfTrain2 = pd.read_csv('/Users/jibuanok/Documents/u/DM/BankChurnersTrain.csv', delimiter=',')
#dfTrain2.loc[dfTrain2.Attrition_Flag == 'Existing Customer', 'Attrition_Flag'] = 1
#dfTrain2.loc[dfTrain2.Attrition_Flag == 'Attrited Customer', 'Attrition_Flag'] = 0


dfTrain2['Attrition_Flag'] = dfTrain2['Attrition_Flag'].replace(['Existing Customer'], 0)
dfTrain2['Attrition_Flag'] = dfTrain2['Attrition_Flag'].replace(['Attrited Customer'], 1)
dfTrain2['Gender'] = dfTrain2['Gender'].replace(['M'], 1)
dfTrain2['Gender'] = dfTrain2['Gender'].replace(['F'], 0)
dfTrain3 = dfTrain2
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['Less than $40K'], 20)
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['$40K - $60K'], 50)
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['$60K - $80K'], 70)
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['$80K - $120K'], 100)
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['$120K +'], 150)
dfTrain3['Income_Category'] = dfTrain3['Income_Category'] .replace(['Unknown'], 85)

dfTrain4 = dfTrain3.copy()
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['Uneducated'], 1)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['High School'], 2)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['College'], 3)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['Graduate'], 4)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['Post-Graduate'], 5)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['Doctorate'], 6)
dfTrain4['Education_Level'] = dfTrain4['Education_Level'] .replace(['Unknown'], 3.5)

dfTrain6 = dfTrain4.copy()
dfTrain6['Card_Category'] = dfTrain6['Card_Category'] .replace(['Blue'], 1)
dfTrain6['Card_Category'] = dfTrain6['Card_Category'] .replace(['Silver'], 2)
dfTrain6['Card_Category'] = dfTrain6['Card_Category'] .replace(['Gold'], 3)
dfTrain6['Card_Category'] = dfTrain6['Card_Category'] .replace(['Platinum'], 4)




dfTest = pd.read_csv('/Users/jibuanok/Documents/u/DM/BankChurnersTest.csv', delimiter=',')


#Preparing Unknowns as medians in their resepctive sets (part a)
dfTrain5 = dfTrain.copy()
dfTrain5['Income_Category'] = dfTrain5['Income_Category'] .replace(['Unknown'], '$80K - $120K')
dfTrain5['Education_Level'] = dfTrain5['Education_Level'] .replace(['Unknown'], 'Graduate')
dfTrain5['Attrition_Flag'] = dfTrain5['Attrition_Flag'] .replace(['Existing Customer'], 0)
dfTrain5['Attrition_Flag'] = dfTrain5['Attrition_Flag'] .replace(['Attrited Customer'], 1)
dfTest5 = dfTest.copy()
dfTest5['Income_Category'] = dfTest5['Income_Category'] .replace(['Unknown'], '$80K - $120K')
dfTest5['Education_Level'] = dfTest5['Education_Level'] .replace(['Unknown'], 'Graduate')
dfTest5['Attrition_Flag'] = dfTest5['Attrition_Flag'] .replace(['Existing Customer'], 0)
dfTest5['Attrition_Flag'] = dfTest5['Attrition_Flag'] .replace(['Attrited Customer'], 1)


#dfTrain = dfTrain.drop(["CCNum","Trans_date_Time", "Surname"],axis = 1) #drop irrelevant columns
#dfTest = dfTest.drop(["CCNum","Trans_date_Time", "Surname"],axis = 1) #drop irrelevant columns

#print(df.isnull().sum()) #find number of empty values in all columns
"""
print('')
print('Train Balances')
print(100 * dfTrain['Balance'].value_counts(normalize=True).head())
print('')
print('Test Balances')
print(100 * dfTest['Balance'].value_counts(normalize=True).head())
"""

dfTrain5_upsampled =pd.get_dummies(dfTrain5, columns=['Gender', 'Geography', 'Education_Level', 'Income_Category',
                                                      'Card_Category'])

dfTest5_upsampled =pd.get_dummies(dfTest5, columns=['Gender', 'Geography', 'Education_Level', 'Income_Category',
                                                      'Card_Category'])



#results for train and test

attritionFlagTrain = np.array(dfTrain5_upsampled['Attrition_Flag'])
exitedTrain = np.array(dfTrain5_upsampled['Exited'])

attritionFlagTest = np.array(dfTest5_upsampled['Attrition_Flag'])
exitedTest = np.array(dfTest5_upsampled['Exited'])

#Profile 1
dfTrainAttProfile1 = dfTrain5_upsampled.loc[:, ['Total_Trans_Amt', 'Total_Trans_Ct', 'Card_Category_Blue',
                            'Card_Category_Gold', 'Card_Category_Platinum', 'Card_Category_Silver', 'Credit_Limit',
                            'Age', 'Gender_F', 'Gender_M']]

dfTestAttProfile1 = dfTest5_upsampled.loc[:, ['Total_Trans_Amt', 'Total_Trans_Ct', 'Card_Category_Blue',
                            'Card_Category_Gold', 'Card_Category_Platinum', 'Card_Category_Silver', 'Credit_Limit',
                            'Age', 'Gender_F', 'Gender_M']]

#Profile 2
dfTrainAttProfile2 = dfTrain5_upsampled.loc[:, ['Balance', 'NumOfProducts', 'IsActiveMember']]
dfTestAttProfile2 = dfTest5_upsampled.loc[:, ['Balance', 'NumOfProducts', 'IsActiveMember']]

#Profile 3
dfTrainAttProfile3 = dfTrain5_upsampled.loc[:, ['Gender_F', 'Gender_M', 'Credit_Limit', 'Income_Category_$120K +',
                                                'Income_Category_$40K - $60K', 'Income_Category_$60K - $80K',
                                                'Income_Category_$80K - $120K', 'Income_Category_Less than $40K', 'Age',
                                                'Card_Category_Blue', 'Card_Category_Gold', 'Card_Category_Platinum',
                                                'Card_Category_Silver', 'HasCrCard']]

dfTestAttProfile3 = dfTest5_upsampled.loc[:, ['Gender_F', 'Gender_M', 'Credit_Limit', 'Income_Category_$120K +',
                                                'Income_Category_$40K - $60K', 'Income_Category_$60K - $80K',
                                                'Income_Category_$80K - $120K', 'Income_Category_Less than $40K', 'Age',
                                                'Card_Category_Blue', 'Card_Category_Gold', 'Card_Category_Platinum',
                                                'Card_Category_Silver', 'HasCrCard']]

#Profile 1 attrition flag model
rf1Attrition = RandomForestClassifier(n_estimators=1000)
rf1Attrition.fit(dfTrainAttProfile1, attritionFlagTrain)
rf1AttritionPredictions = rf1Attrition.predict(dfTestAttProfile1)
rf1AttritionErrors = abs(rf1AttritionPredictions - attritionFlagTest)
rf1AttritionErrors = float(np.mean(rf1AttritionErrors))
rf1AttritionErrors = round(rf1AttritionErrors, 7) * 100
rf1AttritionConfusionMatrix = confusion_matrix(attritionFlagTest, rf1AttritionPredictions)

#Profile 1 exited model
rf1Exited = RandomForestClassifier(n_estimators=1000)
rf1Exited.fit(dfTrainAttProfile1, exitedTrain)
rf1ExitedPredictions = rf1Exited.predict(dfTestAttProfile1)
rf1ExitedErrors = abs(rf1ExitedPredictions - exitedTest)
rf1ExitedErrors = float(np.mean(rf1ExitedErrors))
rf1ExitedErrors = round(rf1ExitedErrors, 7) * 100
rf1ExitedConfusionMatrix = confusion_matrix(exitedTest, rf1ExitedPredictions)

#Profile 2 attrition flag model
rf2Attrition = RandomForestClassifier(n_estimators=1000)
rf2Attrition.fit(dfTrainAttProfile2, attritionFlagTrain)
rf2AttritionPredictions = rf2Attrition.predict(dfTestAttProfile2)
rf2AttritionErrors = abs(rf2AttritionPredictions - attritionFlagTest)
rf2AttritionErrors = float(np.mean(rf2AttritionErrors))
rf2AttritionErrors = round(rf2AttritionErrors, 7) * 100
rf2AttritionConfusionMatrix = confusion_matrix(attritionFlagTest, rf2AttritionPredictions)

#Profile 2 exited model
rf2Exited = RandomForestClassifier(n_estimators=1000)
rf2Exited.fit(dfTrainAttProfile2, exitedTrain)
rf2ExitedPredictions = rf2Exited.predict(dfTestAttProfile2)
rf2ExitedErrors = abs(rf2ExitedPredictions - exitedTest)
rf2ExitedErrors = float(np.mean(rf2ExitedErrors))
rf2ExitedErrors = round(rf2ExitedErrors, 7) * 100
rf2ExitedConfusionMatrix = confusion_matrix(exitedTest, rf2ExitedPredictions)

#Profile 3 attrition flag model
rf3Attrition = RandomForestClassifier(n_estimators=1000)
rf3Attrition.fit(dfTrainAttProfile3, attritionFlagTrain)
rf3AttritionPredictions = rf3Attrition.predict(dfTestAttProfile3)
rf3AttritionErrors = abs(rf3AttritionPredictions - attritionFlagTest)
rf3AttritionErrors = float(np.mean(rf3AttritionErrors))
rf3AttritionErrors = round(rf3AttritionErrors, 7) * 100
rf3AttritionConfusionMatrix = confusion_matrix(attritionFlagTest, rf3AttritionPredictions)

#Profile 3 exited model
rf3Exited = RandomForestClassifier(n_estimators=1000)
rf3Exited.fit(dfTrainAttProfile3, exitedTrain)
rf3ExitedPredictions = rf3Exited.predict(dfTestAttProfile3)
rf3ExitedErrors = abs(rf3ExitedPredictions - exitedTest)
rf3ExitedErrors = float(np.mean(rf3ExitedErrors))
rf3ExitedErrors = round(rf3ExitedErrors, 7) * 100
rf3ExitedConfusionMatrix = confusion_matrix(exitedTest, rf3ExitedPredictions)


print('Profile 1 Attrition flag: Mean absolute error: ', rf1AttritionErrors, '%')
print('Profile 1 Attrition flag: Confusion matrix: \n', rf1AttritionConfusionMatrix)
print('Profile 1 Exited: Mean absolute error: ', rf1ExitedErrors, '%')
print('Profile 1 Exited: Confusion matrix: \n', rf1ExitedConfusionMatrix)

print(('--------------------------------------------'))
print('Profile 2 Attrition flag: Mean absolute error: ', rf2AttritionErrors, '%')
print('Profile 2 Attrition flag: Confusion matrix: \n', rf2AttritionConfusionMatrix)
print('Profile 2 Exited: Mean absolute error: ', rf2ExitedErrors, '%')
print('Profile 2 Exited: Confusion matrix: \n', rf2ExitedConfusionMatrix)

print(('--------------------------------------------'))
print('Profile 3 Attrition flag: Mean absolute error: ', rf3AttritionErrors, '%')
print('Profile 3 Attrition flag: Confusion matrix: \n', rf3AttritionConfusionMatrix)
print('Profile 3 Exited: Mean absolute error: ', rf3ExitedErrors, '%')
print('Profile 3 Exited: Confusion matrix: \n', rf3ExitedConfusionMatrix)




dfBalances = dfTrainSet['Balance']
dfBalances = dfBalances.loc[dfBalances != 0.00]
balancesMedian = dfBalances.median()







#Preparing Unknowns as medians in their resepctive sets (part b)
dfTrain9 = dfTrain.copy()
dfTrain9['Income_Category'] = dfTrain9['Income_Category'] .replace(['Unknown'], '$80K - $120K')
dfTrain9['Education_Level'] = dfTrain9['Education_Level'] .replace(['Unknown'], 'Graduate')
dfTrain9['Attrition_Flag'] = dfTrain9['Attrition_Flag'] .replace(['Existing Customer'], 0)
dfTrain9['Attrition_Flag'] = dfTrain9['Attrition_Flag'] .replace(['Attrited Customer'], 1)
dfTest9 = dfTest.copy()
dfTest9['Income_Category'] = dfTest9['Income_Category'] .replace(['Unknown'], '$80K - $120K')
dfTest9['Education_Level'] = dfTest9['Education_Level'] .replace(['Unknown'], 'Graduate')
dfTest9['Attrition_Flag'] = dfTest9['Attrition_Flag'] .replace(['Existing Customer'], 0)
dfTest9['Attrition_Flag'] = dfTest9['Attrition_Flag'] .replace(['Attrited Customer'], 1)


dfTrain9_upsampled =pd.get_dummies(dfTrain9, columns=['Geography', 'Card_Category', 'Gender'])
dfTest9_upsampled =pd.get_dummies(dfTest9, columns=['Geography', 'Card_Category', 'Gender'])


fraudTrain = np.array(dfTrain9_upsampled['is_fraud'])
fraudTest = np.array(dfTest9_upsampled['is_fraud'])


#Geography profile
dfTrainGeography = dfTrain9_upsampled.loc[:, ['Geography_France', 'Geography_Germany', 'Geography_Spain',]]
dfTestGeography = dfTest9_upsampled.loc[:, ['Geography_France', 'Geography_Germany', 'Geography_Spain']]

#Card category profile
dfTrainCardCategory = dfTrain9_upsampled.loc[:, ['Card_Category_Blue', 'Card_Category_Gold', 'Card_Category_Platinum',
                                                'Card_Category_Silver']]
dfTestCardCategory = dfTest9_upsampled.loc[:, ['Card_Category_Blue', 'Card_Category_Gold', 'Card_Category_Platinum',
                                                'Card_Category_Silver']]

#Gender profile
dfTrainGender = dfTrain9_upsampled.loc[:, ['Gender_F', 'Gender_M']]
dfTestGender = dfTest9_upsampled.loc[:, ['Gender_F', 'Gender_M']]

#Tenure profile
dfTrainTenure = dfTrain9_upsampled.loc[:,['Tenure']]
dfTestTenure = dfTest9_upsampled.loc[:,['Tenure']]



#Geography fraud model
rfGeography = RandomForestClassifier(n_estimators=1000)
rfGeography.fit(dfTrainGeography, fraudTrain)
rfGeographyPredictions = rfGeography.predict(dfTestGeography)
rfGeographyErrors = abs(rfGeographyPredictions - fraudTest)
rfGeographyErrors = float(np.mean(rfGeographyErrors))
rfGeographyErrors = round(rfGeographyErrors, 7) * 100
rfGeographyConfusionMatrix = confusion_matrix(fraudTest, rfGeographyPredictions)

#Card category fraud model
rfCardCategory = RandomForestClassifier(n_estimators=1000)
rfCardCategory.fit(dfTrainCardCategory, fraudTrain)
rfCardCategoryPredictions = rfCardCategory.predict(dfTestCardCategory)
rfCardCategoryErrors = abs(rfCardCategoryPredictions - fraudTest)
rfCardCategoryErrors = float(np.mean(rfCardCategoryErrors))
rfCardCategoryErrors = round(rfCardCategoryErrors, 7) * 100
rfCardCategoryConfusionMatrix = confusion_matrix(fraudTest, rfCardCategoryPredictions)

#Gender fraud model
rfGender = RandomForestClassifier(n_estimators=1000)
rfGender.fit(dfTrainGender, fraudTrain)
rfGenderPredictions = rfGender.predict(dfTestGender)
rfGenderErrors = abs(rfGenderPredictions - fraudTest)
rfGenderErrors = float(np.mean(rfGenderErrors))
rfGenderErrors = round(rfGenderErrors, 7) * 100
rfGenderConfusionMatrix = confusion_matrix(fraudTest, rfGenderPredictions)



#Tenure fraud model
rfTenure = RandomForestClassifier(n_estimators=1000)
rfTenure.fit(dfTrainTenure, fraudTrain)
rfTenurePredictions = rfTenure.predict(dfTestTenure)
rfTenureErrors = abs(rfGenderPredictions - fraudTest)
rfTenureErrors = float(np.mean(rfTenureErrors))
rfTenureErrors = round(rfTenureErrors, 7) * 100
rfTenureConfusionMatrix = confusion_matrix(fraudTest, rfTenurePredictions)


print('\n\n')
print('Geography fraud: Mean absolute error: ', rfGeographyErrors, '%')
print('Geography fraud: Confusion matrix: \n', rfGeographyConfusionMatrix)
print(('--------------------------------------------'))
print('Card Category fraud: Mean absolute error: ', rfCardCategoryErrors, '%')
print('Card Category fraud: Confusion matrix: \n', rfCardCategoryConfusionMatrix)
print(('--------------------------------------------'))
print('Gender fraud: Mean absolute error: ', rfGenderErrors, '%')
print('Gender fraud: Confusion matrix: \n', rfGenderConfusionMatrix)
print(('--------------------------------------------'))
print('Tenure fraud: Mean absolute error: ', rfTenureErrors, '%')
print('Tenure fraud: Confusion matrix: \n', rfTenureConfusionMatrix)




#print(dfBalances.head())
#print(dfBalances.median())

#print(dfTrain4.dtypes)
#print(dfTrainAttProfile3.shape)
#print(dfTestAttProfile3.shape)

"""
cmap = "RdYlGn"
plt.figure(figsize=(20, 20))
ax = sns.heatmap(
    dfTrain6.corr(),
    vmin=-1, vmax=1, center=0,
    cmap=cmap,
    square=True,linewidths=.5
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)
plt.show()

"""