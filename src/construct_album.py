import pandas as pd
import sjy as sjy

from selenium import webdriver
import time

board = pd.read_csv('data/refine/album.csv')

driver = webdriver.Chrome() 

idx_src = 52
idx_cur = idx_src
for idx, row in board.iloc[idx_src:].iterrows():
    sjy.login(driver, row['id'], row['id'])
    sjy.album_write(driver, row['subject'], image_lst=row['file'].split(';'), comment_lst=row['memo'].split('&split&'), date=row['date'])
    sjy.logout(driver)
    idx_cur += 1
    print(f'processing iloc[{idx_cur}]..')
print()
print('construct all board')