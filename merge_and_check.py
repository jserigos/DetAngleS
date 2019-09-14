import pandas as pd

def main():
    # read the file after tokenizing
    SpacyTokenizer_csv = pd.read_csv('Data/OpinionArticles-TASI.csv', encoding='utf-8')
    SpacyTokenizer_csv_df = pd.DataFrame(SpacyTokenizer_csv)
    print(len(SpacyTokenizer_csv_df))

    # read Goldstandard file
    GoldStandard_csv = pd.read_csv('Data/OpinionArticlesRetokenized-GS.csv', encoding='utf-8')
    GoldStandard_csv_df = pd.DataFrame(GoldStandard_csv)
    print(len(GoldStandard_csv_df))

    # check the difference between two files
    outer_df = pd.merge(SpacyTokenizer_csv_df, GoldStandard_csv_df, on='Token', how='outer', indicator='Exist')
    diff_df = outer_df.loc[outer_df['Exist'] != 'both']
    print(len(diff_df))
    diff_df.to_csv(r'Data/diff_df.csv', index=None, header=True)

    # df of interested tokens
    target_token = SpacyTokenizer_csv_df[SpacyTokenizer_csv_df.Anglicism.isnull()]
    target_full_df = pd.merge(target_token, GoldStandard_csv_df, on='Token', how='left')
    target_full_df.drop(['Anglicism_x', 'New_Index', 'Language_x'], axis=1, inplace=True)
    target_full_df.rename(columns={'Anglicism_y': 'Anglicism'}, inplace=True)
    target_full_df.rename(columns={'Language_y': 'Language'}, inplace=True)
    target_full_df.drop_duplicates(keep='first', inplace=True)
    print(len(target_full_df))
    print(target_full_df.columns)

    target_full_df.to_csv(r'Data/target_full_df.csv', index=None, header=True)


if __name__ == '__main__':
    main()