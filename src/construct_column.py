import pandas as pd
import sjy as sjy

from selenium import webdriver
import time

column = pd.read_csv('data/refine/column.csv')

driver = webdriver.Chrome() 

idx_src = 124
idx_cur = idx_src
for idx, row in column.iloc[idx_src:].iterrows():
    sjy.login(driver, '#####', '#####')
    sjy.column_write(driver, title=row['subject'], content=row['memo'], url=row['sitelink1'], date=row['date'])
    sjy.logout(driver)
    time.sleep(5)
    idx_cur += 1
    print(f'processing iloc[{idx_cur}]..')
print()
print('construct all column')