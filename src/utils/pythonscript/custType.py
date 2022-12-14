import pandas as pd
from sklearn.externals import joblib
import csv

tempfile = "predict.csv"
df_query = pd.read_csv(tempfile)
query = df_query.drop(['cust_id','cust_segment','cust_topologytype','cust_mgmtstn','cust_secstation','cust_dnac','techsupport_sw_type','techsupport_uptime','techsupport_cpu','techsupport_memory','techsupport_hastate','techsupport_version','techsupport_sl','techsupport_systemmtu'],axis=1)
classifier = joblib.load('rfc.pkl')
predict = classifier.predict(query)
print('++++++++')
print(query)
print(predict)
##write to csv 
f = open(tempfile,'r')
reader = csv.reader(f)
mylist = list(reader)
f.close()
mylist[1][1]=predict[0]
my_new_list = open(tempfile,'w')
csv_writer = csv.writer(my_new_list)
csv_writer.writerows(mylist)
my_new_list.close()


