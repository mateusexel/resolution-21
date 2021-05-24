import pandas as pd
import glob


def merging_cvm(folder):
    list_files = glob.glob(folder + '/*')
    df = pd.DataFrame()
    for file in list_files:
        df = df.append(pd.read_csv(file, sep=';', encoding='latin-1'))

    return df


def clean_cvm(df):
    df = df[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_COMPTC', 'TP_DOC', 'NM_ARQ', 'LINK_ARQ']]
    df = df[df['TP_DOC'] == 'REGUL FDO']
    df['CNPJ_FUNDO'] = df['CNPJ_FUNDO'].str.replace('[^0-9]', '')
    df.dropna(subset=['NM_ARQ'], inplace=True)
    df = df.reset_index(drop=True)

    return df


def read_eco_data(filepath):
    df = pd.read_excel(filepath, header=3, index_col=0)
    df.columns = df.columns = [i.replace('\n', ' ') for i in df.columns]
    df = df[['Name', 'Employer ID number', 'Administrator', 'Series Start Date', 'Res 3792/4661 (acc regul)',
             'Date of regulation']]
    df = df.rename(columns={'Res 3792/4661 (acc regul)': 'Res 3792/4661'})
    df['Employer ID number'] = df['Employer ID number'].astype(str)

    return df


def rebalance_eco(df):
    cont0, count1, cont_undefinde = df['Res 3792/4661'].value_counts()
    df_class0 = df[df['Res 3792/4661'] == '-']
    df_class1 = df[df['Res 3792/4661'] == 'Yes']
    df_class0_under = df_class0.sample(count1, random_state=42)
    df = pd.concat([df_class0_under, df_class1], axis=0)

    return df


def merge_fix_target(df_cvm, df_eco):
    df = pd.merge(df_cvm, df_eco, how='inner', left_on=['CNPJ_FUNDO'], right_on=['Employer ID number'])
    d = {'Yes': 1, '-': 0}
    df['Res 3792/4661'] = [d[i] for i in df['Res 3792/4661']]
    df = df.sample(frac=1)

    return df
