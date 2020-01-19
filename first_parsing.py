import json
import pandas as pd
import numpy as np
from collections import defaultdict
import pickle

#toutes gloses utilisees et nb de fois utilisees
def used_glosses(morpheme, data):
    used_gloss = defaultdict(list)
    for _, row in data.iterrows():
        if row[morpheme] is not np.nan:
            for glose_list in list(row[morpheme]):
                print(glose_list)
                used_gloss[glose_list].append(row["lang"])
    return(used_gloss)

with open('excerpt-pangloss.json', 'r') as json_file:
    jsondata = json.load(json_file)[0]

data = pd.DataFrame(jsondata)

nb_phrases= data.shape[0]
df_general = data.count()

#nb lang
nb_lang = data["lang"].nunique()
list_name_lang = data["lang"].unique()

used_gloss_morphem= used_glosses("glose_morphem", data)
used_gloss_word= used_glosses("glose_word", data)
pickle.dump((used_gloss_word, used_gloss_morphem), open("gloss.pkl", "wb"))
