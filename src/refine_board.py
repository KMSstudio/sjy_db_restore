import pandas as pd

refine_dict = { '&nbsp;': ' ', 
    '\\\'': '\'', '\\\"': '\"',
    '&gt;': ' ', '&it;': ' ', '&amp': ' ', '&lt;': '',
    '병신': '##', '존나': '##', '지랄': '##', '좆': '#', '좇': '#', '씹': '#',
}
def refine_string(string):
    for key, value in refine_dict.items():
        string = string.replace(key, f";{value}")
    return string

member = pd.read_csv('data/member/member_table.csv')
board = pd.read_csv('data/board/lab_board.csv')

board['id'] = board['name'].apply(lambda name: member[member['name'] == name].iloc[0]['user_id'])
board['memo'] = board['memo'].apply(refine_string)
board['subject'] = board['subject'].apply(refine_string)

board.to_csv('data/refine/board.csv')