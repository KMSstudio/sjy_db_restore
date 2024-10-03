import pandas as pd
import sjy

member = pd.read_csv('data/member/member_table.csv')
board = pd.read_csv('data/column/column.csv')

board['id'] = board['name'].apply(lambda name: member[member['name'] == '송재용'].iloc[0]['user_id'])
board['memo'] = board['memo'].apply(sjy.refine_string)
board['subject'] = board['subject'].apply(sjy.refine_string)
board = board.drop(columns=['hit', 'x', 'y'])

board.to_csv('data/refine/column.csv')