import pandas as pd
import sjy as sjy

from selenium import webdriver
import time

board = pd.read_csv('data/refine/board.csv')

driver = webdriver.Chrome() 

idx_src = 998
idx_cur = idx_src
for idx, row in board.iloc[idx_src:].iterrows():
    sjy.login(driver, row['id'], row['id'])
    sjy.lab_board_write(driver, row['subject'], row['memo'], row['date'])
    sjy.logout(driver)
    idx_cur += 1
    print(f'processing iloc[{idx_cur}]..')
print()
print('construct all board')