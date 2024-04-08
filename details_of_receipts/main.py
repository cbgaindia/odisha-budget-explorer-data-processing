import os
import math
import pandas as pd
from pandas import DataFrame


pd.options.mode.chained_assignment = None


CURRENT_FOLDER = os.path.realpath(os.path.join(__file__, '..'))


def clean_data(df: DataFrame) -> DataFrame:
    df = df.iloc[4:]

    df.dropna(axis=1)

    df.columns = [
        'Code',
        'Head Of Account In Local Language',
        'Head Of Account',
        'Empty Columns',
        'Accounts',
        'Budget Estimates',
        'Revised Estimates',
        'Budget Estimates',
    ]

    df.reset_index(inplace=True)

    df.drop('index', axis=1, inplace=True)
    df.drop('Head Of Account In Local Language', axis=1, inplace=True)
    df.drop('Empty Columns', axis=1, inplace=True)

    df['Code'] = df['Code'].apply(lambda x: str(x).strip().replace('-', ''))

    return df


def main(year: int):
    df = pd.read_excel(os.path.join(
        CURRENT_FOLDER, 'input.xlsx'
    ))

    df = clean_data(df)

    major_head = ''
    major_head_description = ''
    sub_major_head = '00'
    sub_major_head_description = ''
    minor_head = ''
    minor_head_description = ''
    sub_minor_head = ''
    sub_minor_head_description = ''
    detail_head = ''
    detail_head_description = ''

    empty_row_count = 0

    receipts = []

    for index, row in df.iterrows():
        if math.isnan(float(row[0])):
            empty_row_count = empty_row_count + 1
            continue

        if not isinstance(row[1], float) and 'TOTAL' in row[1]:
            continue

        if index == 0 and len(row[0]) == 4:
            major_head = row[0]
            major_head_description = row[1]
            continue

        if empty_row_count == 2 and len(row[0]) == 4:
            empty_row_count = 0
            major_head = row[0]
            major_head_description = row[1]
            continue

        if len(row[0]) == 3:
            minor_head = row[0]
            minor_head_description = row[1]
            continue

        if empty_row_count != 2 and  len(row[0]) == 4:
            sub_minor_head = row[0]
            sub_minor_head_description = row[1]
            continue

        if len(row[0]) == 5:
            detail_head = row[0]
            detail_head_description = row[1]

            receipts.append([
                "{}-{}-{}-{}-{}".format(
                    major_head, sub_major_head, minor_head, sub_minor_head, detail_head
                ),
                major_head_description,
                sub_major_head_description,
                minor_head_description,
                sub_minor_head_description,
                detail_head_description,
                row[2],
                row[3],
                row[4],
                row[5],
            ])

    ndf = pd.DataFrame(receipts)

    ndf.columns = [
        'HEAD OF ACCOUNT',
        'MAJOR HEAD DESCRIPTION',
        'SUB MAJOR HEAD DESCRIPTION',
        'MINOR HEAD DESCRIPTION',
        'SUB MINOR HEAD DESCRIPTION',
        'DETAIL HEAD DESCRIPTION',
        'ACCOUNTS {}-{}'.format(year - 2, year - 1),
        'BUDGET ESTIMATES {}-{}'.format(year - 1, year),
        'REVISED ESTIMATES {}-{}'.format(year - 1, year),
        'BUDGET ESTIMATES {}-{}'.format(year, year + 1),
    ]

    ndf.reset_index(drop=True, inplace=True)
    
    ndf.to_csv(CURRENT_FOLDER + "/output.csv")


if __name__ == "__main__":
    year = int(
        input("Enter the year of this data (XXXX):")
    )

    main(year)