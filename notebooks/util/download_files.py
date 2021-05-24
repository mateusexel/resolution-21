import requests
import glob


def download(df, folder_path):
    # check what files have already been dowloaded
    filenames = [i.replace(folder_path,'') for i in glob.glob(folder_path+'/*')]
    # iterate through every line
    for index, row in df.iterrows():
        # proceed if file has not been dowloaded yet
        if row['NM_ARQ'] not in filenames:
            # get url where file is stored and send request
            url = row['LINK_ARQ']
            response = requests.get(url)
            # save response in folder
            with open(folder_path+row['NM_ARQ'], 'wb') as f:
                f.write(response.content)

