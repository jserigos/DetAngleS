import pandas as pd


def join_punctuation(seq, characters=r'.,:;\?¡¿-!)/""'):
    characters = set(characters)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current

def main():
    OA = pd.read_csv('Documents/Github/TASI/Data/OpinionArticlesRetokenized-GS.csv', encoding='utf-8', header = 0)
    
    OA["Context"] = ""

    for i in range(len(OA)):

        try:
            context = " ".join(join_punctuation(OA.iloc[i-6:i+6, 1]))
        except IndexError:
            context = OA.iloc[i, 1]
        OA.loc[i, 'Context'] = context

    OA.to_csv(r'Desktop/OpinionArticles-GS-Context.csv', index=None, header=True)

if __name__ == '__main__':
    main()

"""
try: 
            context = OA.iloc[index-3:index+3,1]
        except:
            context = OA.iloc[index:index+3,1]
"""