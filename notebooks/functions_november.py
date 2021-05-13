import requests
from pathlib import Path
import glob

def dowload_pdf(df):
    filenames = glob.glob("/media/mateus/disk/fee/pdfs/*")
    for index, row in df.iterrows():
        if row['LINK_ARQ'] not in filenames:
            url = row['LINK_ARQ']
            filename = Path(f"/media/mateus/disk/fee/pdfs/{row['NM_ARQ']}")
            response = requests.get(url)
            filename.write_bytes(response.content)

