import pandas as pd
import sjy

member = pd.read_csv('data/member/member_table.csv')
board = pd.read_csv('data/board/lab_board.csv')

board['id'] = board['name'].apply(lambda name: member[member['name'] == name].iloc[0]['user_id'])
board['memo'] = board['memo'].apply(sjy.refine_string)
board['subject'] = board['subject'].apply(sjy.refine_string)

board.to_csv('data/refine/board.csv')