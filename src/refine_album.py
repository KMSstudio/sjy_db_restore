import os
import shutil
import pandas as pd
import sjy

src_folder = 'data/album/images'
des_folder = 'data/refine/image'
os.makedirs(des_folder, exist_ok=True)

# Copy src to des
def copy_all_files(src, dest):
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest, file)
            shutil.copy2(src_file_path, dest_file_path)

# Copy images to data/refine/image
copy_all_files(src_folder, des_folder)

member = pd.read_csv('data/member/member_table.csv')
album = pd.read_csv('data/album/album.csv')

album['id'] = album['name'].apply(lambda name: member[member['name'] == name].iloc[0]['user_id'])
album['memo'] = album['memo'].apply(sjy.refine_string)
album['subject'] = album['subject'].apply(sjy.refine_string)

album = album.drop(columns='file_name1')
album = album.rename(columns={'s_file_name1': 'file'})

refine_album = album.groupby('subject').agg({
    'name': 'first',
    'id': 'first',
    'memo': lambda x: '&split&'.join(x),
    'file': lambda x: ';'.join(x),
    'date': 'first'
}).reset_index()

refine_album.to_csv('data/refine/album.csv')
