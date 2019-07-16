import pandas as pd
import numpy as np

def main():
    # read the file after tokenized
    NACC_csv = pd.read_csv('spacy-annotated_df.csv', encoding='utf-8')
    NACC_csv_df = pd.DataFrame(NACC_csv)
    print(len(NACC_csv_df))

    # read Goldstandard file
    GoldStandard_tsv = pd.read_csv('NACC-GoldStandard.tsv', delimiter='\t', encoding='utf-8')
    GoldStandard_tsv_df = pd.DataFrame(GoldStandard_tsv)
    print(len(GoldStandard_tsv_df))

    # check the difference between two files
    outer_df = pd.merge(NACC_csv_df, GoldStandard_tsv, on='Token', how='outer', indicator='Exist')
    diff_df = outer_df.loc[outer_df['Exist'] != 'both']
    print(len(diff_df))
    diff_df.to_csv(r'diff_df.csv', index=None, header=True)

    # df of interested tokens
    target_token = NACC_csv_df[NACC_csv_df.Anglicism.isnull()]
    target_full_df = pd.merge(target_token, GoldStandard_tsv_df, on='Token', how='left')
    target_full_df.drop(['Language_x', 'Anglicism_x'], axis=1, inplace=True)
    target_full_df.rename(columns={'Language_y': 'Language', 'Anglicism_y': 'Anglicism'},inplace=True)
    target_full_df.drop_duplicates(keep='first', inplace=True)
    print(len(target_full_df))
    print(target_full_df.columns)

    target_full_df.to_csv(r'target_full_df.csv', index=None, header=True)


if __name__ == '__main__':
    main()