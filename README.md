# Desciptive analysis from The Pangloss Collection data 

The aim of this project was to do a descriptive analysis of the linguistic data acquired in the [Pangloss Collection](https://pangloss.cnrs.fr/index_en.htm "PANGLOSS website"), to be able to create a tool that would group all glosses by type.

The Pangloss Collection is a database of media in under-documented languages. One type of data Pangloss has are transcripted texts, with their gloses (per word, per morphem, or both) and with a translation in another language (English, French...). The "problem" with this kind of data, though, is that because different researches do the work, it is difficult to have unified gloses and translation. The ultimate goal of this project is to create a tool that would allow to unify all those gloses in order for linguists to compare different languages. This bunch of code is the beginning of this project: descriptive analysis of the dataset to see how it looks like, before getting to the creation of the tool itself.

/!\ The file always names as ```pangloss.json``` is, in this code, ```excerpt-pangloss.json```, given that the first one was really heavy to be posted in this repository.

#### Table of Contents

* [Grabbing the Data](#data)
* [First Parsing](#parse)
* [Glosses descriptive analysis](#gloss)
* [Executing the code](#code)
* [Conclusion](#conclusion)
* [What I learned from this course](#learned)

## <a name="data"></a>Grabbing the data
The data of The Pangloss Collection has been extracted from diverse XML files and recorded in a JSON (```pangloss.json```) in the form of a list of dictionnaries as the following:
```python
{"lang": "tvk", "src": "Napol goni transleta tei .", "en": "I work as a translator", "bi": "mi wok olsem wan translator", "tokenized_src_morphem": ["na", "pol", "goni", "transleta", "tei"], "glose_morphem": ["1s.nfut", "work", "3s.be_like.ind", "translator", "one"]}
```
Where: 
* **"lang"** represents the code of the sampled langue
* **"src"**, the transcripted sentence
* **"en"**/**"bi"**/**"fr"**..., the languages in which the source has been translaetd in
* **"tokenized_src_morphem"**, the token morphems present in the source
* **"glose_morphem"**, the glose for each one of this morphems
* **"tokenized_src_word"**, the token words present in the source *(Not present in this example)*
* **"glose_word"**, the glose for each one of this words *(Not present in this example)*

This file has been the one used for the ensuing analysis, importing it with the following code:
```python
import json
import pandas as pd

with open('pangloss.json', 'r') as json_file:
    jsondata = json.load(json_file)[0]

data = pd.DataFrame(jsondata)
```

## <a name="parse"></a>First Parsing
For the first steps of the parsing, I wanted to have a general view of the DataFrame, know how many phrases we had in total, and finally which languages and how many we were dealing with. To do so, I used the following code (and got the following output):
```python
>>> # general view of the DataFrame
>>> df_general = data.count()
bi                          305
che                           8
cmn                        1290
cn                          522
de                         2927
ell                         736
en                        31606
eng                        1650
fr                        36662
glose_morphem             27567
glose_word                20129
it                         2110
lang                     120328
ne                         1003
nep                        1261
src                      109780
tokenized_src_morphem     29342
tokenized_src_word        35562
vie                         519
vn                           42
zh                        33886
dtype: int64

>>> # nb of phrases in total
>>> nb_phrases= data.shape[0]
120328

>>> # nb lang
>>> nb_lang = data["lang"].nunique()
88

>>> # list of languages
>>> list_name_lang = data["lang"].unique() 
['tvk' 'nep' 'nge' 'lhu' 'aji' 'taj' 'ayn' 'way' 'dhv' 'lzz' 'tur' 'swb'
 'zdj' 'bfq' 'nem' 'iai' 'uve' 'rmn' 'mkd' 'bul' 'ixc' 'nee' 'nua' 'udl'
 'lag' 'ycn' 'ady' 'kkt' 'tdh' 'klr' 'ckb' 'pmi' 'che' 'svm' 'hrv' 'hsb'
 'ers' 'cmn' 'sxg' 'twh' 'tpo' 'akr' 'mlv' 'msn' 'lkn' 'wwo' 'mrm' 'olr'
 'krf' 'tgs' 'mtt' 'hiw' 'lht' 'tkw' 'lrz' 'tql' 'urr' 'vra' 'tkp' 'tnx'
 'vnk' 'jya' 'nbc' 'vay' 'lif' 'bhj' 'lus' 'njo' 'new' 'uby' 'nru' 'nxq'
 'vie' 'tyj' 'ane' 'axx' 'wls' 'fud' 'cir' 'kdk' 'bwa' 'cam' 'pri' 'piz'
 'kke' 'pbn' 'kdx']
```
Then, I proceeded to look more into the gloses themselves, grabbing the following informations for each language:
* Its gloses-per-word
* Its gloses-per-morphem
* The number of times each glose has been used in each language

To do so, I created the following function:
```python
import numpy as np
from collections import defaultdict

def used_glosses(gloses, data):
    used_gloss = defaultdict(list)
    for _, row in data.iterrows():
        if row[gloses] is not np.nan:
            for glose_list in list(row[morpheme]):
                print(glose_list)
                used_gloss[glose_list].append(row["lang"])
    return(used_gloss)
```
Then, I applied this function to **"glose_word"** and to **"glose_morphem"** and saved the data in another file (```gloss.pkl```), so it would be easier to treat afterwards:
```python
import pickle

used_gloss_morphem= used_glosses("glose_morphem", data)
used_gloss_word= used_glosses("glose_word", data)
pickle.dump((used_gloss_word, used_gloss_morphem), open("gloss.pkl", "wb"))
```
## <a name="gloss"></a>Glosses descriptive analysis
Once I had the new file, created a new function that would convert my ```.pkl``` to a sorted list of all the pairs (*glose-number of times it appears*) present in the dataset.
```python
def from_data_to_list(pickledata, num):
    data = pickledata[num]
    del(data[None])
    whole_list = []
    for key in data:
        list=[key, len(data[key])]
        whole_list.append(list)
    sorted_whole_list = sorted(whole_list, key=itemgetter(1), reverse = True)
    return(sorted_whole_list)
```
To have an overall look of the data in glosses we had and their distribution, I created a function to make and save graphs of:
* The first 10 gloses
* The middle 10 gloses
* The last 10 gloses
* The first 100 gloses
* The middle 100 gloses
* The last 100 gloses

An example of the code for one of the created graphics is the following (I added ```FontProperties``` because some of the data were in Chinese and ```matplotlib``` wouldn't show them):

```python
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns

def make_graphs(pickledata, num,type):
    sorted_whole_list = from_data_to_list(pickledata,num)
    ChineseFont = FontProperties("Microsoft YaHei")
    sns.set()
    
    #Middle 10
    num = int(len(sorted_whole_list)/2)
    middle10 = sorted_whole_list[num-5:num+5]
    labels, ys = zip(*middle10)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('First 10 {}'.format(type))
    plt.savefig('middle_10_{}.png'.format(type))
```
I ran this function for all *the gloses for words* and *the gloses for morphems* in my dataset:
```python
pickledata = pickle.load(open('gloss.pkl', 'rb'))

#Graph for words:
make_graphs(pickledata,0,"words")

#Graph for morphemes:
make_graphs(pickledata,1,"morphemes")
```
This gave me the following graphs (You can see them directly in GitHub, I have problems displaying them in GitHub Pages):

![First 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/first_10_morphemes.png "First 10 morphem gloses")

![Middle 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/middle_10_morphemes.png "Middle 10 morphem gloses")

![Last 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/last_10_morphemes.png "Last 10 morphem gloses")

![First 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/first_100_morphemes.png "First 100 morphem gloses")

![Middle 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/middle_100_morphemes.png "Middle 100 morphem gloses")

![Last 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/last_100_morphemes.png "Last 100 morphem gloses")

![First 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/first_10_words.png "First 10 word gloses")

![Middle 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/middle_10_words.png "Middle 10 word gloses")

![Last 10 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/last_10_words.png "Last 10 word gloses")

![First 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/first_100_words.png "First 100 word gloses")

![Middle 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/middle_100_words.png "Middle 100 word gloses")

![Last 100 gloses](https://github.com/lnarbona/Pangloss/blob/master/Graphs/last_100_words.png "Last 100 word gloses")

We can see that the graphs follow a Zipf law distribution, as we could have expected.

Finally, I decided also to look at which glosses appeared in more than one language (the ones that should be interesting for us in this project)
```python
def multiple_language_gloss(pickledata, num):
    data=pickledata[num]
    del(data[None])
    multiple_lang_gloss = defaultdict(list)
    for key, value in data.items():
        list_lang = []
        for lang in value:
            if lang not in list_lang:
                list_lang.append(lang)
        if len(list_lang) > 1:
            multiple_lang_gloss[key] = list_lang
    return(multiple_lang_gloss, len(multiple_lang_gloss))
```
and also which languages are shared by the gloses in the data: 

```python
def languages_in_gloses(data):
    languages = []
    for key, value in data.items():
        for i in value:
            if i not in languages:
                languages.append(i)
    return(languages)
```
The results I got from applying the precedent codes are the following ones:
```python
>>> #Gloss data for words
>>> multiple_lang_gloss_words,length_words = multiple_language_gloss(pickledata,0)
>>> print(length_words)
2351
>>> languages = languages_in_gloses(multiple_lang_gloss_words)
>>> print(languages)
['tvk', 'lhu', 'nbc', 'iai', 'uve', 'kdk', 'ane', 'nxq', 'aji', 'nem', 'swb', 'jya', 'cam', 'kkt', 'nru', 'axx', 'bwa', 'twh', 'tyj', 'ycn', 'dhv', 'piz', 'pri', 'che', 'uby', 'ady', 'mkd', 'hrv', 'bul', 'svm', 'hsb', 'ers', 'cmn', 'sxg', 'pmi', 'tpo']

#Gloss data for morphems
>>> multiple_lang_gloss_morph,length_morph = multiple_language_gloss(pickledata,1)
>>> print(length_moprh)
3004
>>> languages = languages_in_gloses(multiple_lang_gloss_morph)
>>> print(languages)
['tvk', 'rmn', 'mkd', 'ixc', 'kkt', 'tdh', 'klr', 'ckb', 'svm', 'hrv', 'lif', 'bhj', 'kke', 'lhu', 'pmi', 'hsb', 'akr', 'vay', 'lus', 'njo', 'uby', 'nge', 'bul', 'swb', 'lag', 'kdx', 'udl', 'bfq', 'way', 'nxq', 'nee', 'dhv', 'taj', 'lzz', 'ayn', 'nru', 'ers', 'cmn', 'sxg']
```

## <a name="code"></a>Executing the code
When executing the code, you can do it separatly now because both ```pangloss.json``` and ```gloss.pkl``` are in the GitHub. Anyways, if you were to do it as if ```gloss.pkl``` wasn't already created, you should execute ```fist_data.py``` first and then ```descriptive_data.py```.

## <a name="conclusion"></a>Conclusion
This is the beggining of a bigger project, where I just got to know the database. Further steps I should take to finish the project would be:
* Separate Chinese and non-Chinese gloses (to create first a code with latin alphabet).
* See the distance of edition (Levenshtein distance) of the different strings (gloses).
* Group gloses by minimal edition distance to see if they are the same but ordered/written differently.
* I should also take into account that the glosses (even if all of them are written in the latin alphabet after the filter), are still written in different languages (mostly English and French). So, for example, *1SG-work* and *travailler-1SG* can have the same meaning, but a mere LD will not show that --> think on implementing some kind of translation.

## <a name="learned"></a>What I learned in this course
I've already coded before, as one of the courses in my Bachelor I had informatics and then in biology projects (basic data-treating). In this project I'd been able to get to know a new dataset using descriptive analysis and I learned how to use panda (to see which part of the data I'd to parse, to llok directly at the data before coding) and how tocreate this kind of histograms. 
I think that the articulations between this course and the DataCamp one were not clear enough for us. I don't know what was expected from me in this course and I think in some ways both courses overlapped.
