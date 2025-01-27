from headhunter import get_jobs as hh_get_jobs
import pandas as pd
hh_jobs = hh_get_jobs()
df = pd.DataFrame(hh_jobs)
df2 = pd.read_csv('../PythonProject9/test2.csv')
df.fillna("Уровень дохода не указан")
df["salary"] = df["salary"].replace('[]',"Уровень дохода не указан")
#print(df["title"].head())
df.to_csv('test2.csv')
#print(hh_jobs)
print(df.head())