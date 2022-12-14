import pandas as pd

#df_churn_pd = pd.read_csv("customers.csv")
df_churn_pd = pd.read_csv("temp.csv")
df_churn_pd.head()
print("The dataset contains columns of the following data types : \n" +str(df_churn_pd.dtypes))
print("The dataset contains following number of records for each of the columns : \n" +str(df_churn_pd.count()))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
dtree = RandomForestClassifier()
x,y = df_churn_pd.drop(['cust_id','id','cust_segment'],axis=1),df_churn_pd['cust_segment']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 1)
dtree.fit(x_train,y_train)
prediction = dtree.predict(x_test)

print('With RFC accuracy is: ',dtree.score(x_test,y_test)) # accuracy

#####RFC regressor
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(random_state = 42)

from pprint import pprint

# Look at parameters used by our current forest
print('Parameters currently in use:\n')
pprint(rf.get_params())

#####tweaking parameters
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# for chi square
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
# chi square
x=df_churn_pd.iloc[:, df_churn_pd.columns != "cust_segment" ].values
y=df_churn_pd['cust_segment']
#selector = SelectKBest(f_classif, k=60)
selector = SelectKBest(chi2, k=60)
df_ps = selector.fit_transform(x,y )
df_ps.shape[-1]


#RFS with chi2
dtree = RandomForestClassifier()
x,y = df_churn_pd.drop(['cust_id','id','cust_segment'],axis=1),df_churn_pd['cust_segment']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.3,random_state = 1)
dtree.fit(x_train,y_train)
prediction = dtree.predict(x_test)

print('With RFC accuracy is: ',dtree.score(x_test,y_test)) # accuracy

# export the model to pkl file
#from sklearn.externals import joblib
import joblib
joblib.dump(dtree, 'rfc.pkl')


#predict using pkl file
df_query = pd.read_csv("predict.csv")
query = df_query.drop(['cust_id','cust_segment','cust_topologytype','cust_mgmtstn','cust_secstation','cust_dnac','techsupport_sw_type','techsupport_uptime','techsupport_cpu','techsupport_memory','techsupport_hastate','techsupport_version','techsupport_sl','techsupport_systemmtu'],axis=1)
classifier = joblib.load('rfc.pkl')
predict = classifier.predict(query)
print('++++++++')
print(query)
print(predict)
