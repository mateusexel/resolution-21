import pandas as pd
import glob
import functions_november
import subprocess

df = pd.read_json('./ydata/portal_merge_eco.json')
df = df.sample(frac=1)
functions_november.dowload_pdf(df)

# subprocess.Popen(['bash',"doc_to_docx_rm_doc"],cwd="/home/mateus/data-science/spiced/fee_extraction/pdfs/")

# filenames = glob.glob("./pdfs/*")
# functions_november.pdf_to_txt(filenames)
# print(glob.glob("./txtfiles/*"))
