import pandas as pd


def extract_dataset(df_path: str):
    df = pd.read_csv(df_path)
    return df


def remove_rows(df):
    df.dropna(subset=[df.columns[9, 13, 19, 21]], inplace=True)
    return df


def replace_empty(df):
    df[df.columns[11]] = df[df.columns[11]].fillna(df[df.columns[10]])
    return df


def extract_values_by_indexes(df, column_indexes):
    values_list = []
    for _, row in df.iterrows():
        row_values = [row.iloc[column_index] for column_index in column_indexes]
        values_list.append(row_values)
    return values_list


def extract_data(df_path):
    df = pd.read_csv(df_path)
    df.dropna(subset=[df.columns[9, 13, 19, 21]], inplace=True)
    df[df.columns[11]] = df[df.columns[11]].fillna(df[df.columns[10]])                                               
    values_list = []
    for _, row in df.iterrows():
        row_values = [row.iloc[column_index] for column_index in [7, 9, 11, 13, 19, 21]]
        values_list.append(row_values)
    return values_list
