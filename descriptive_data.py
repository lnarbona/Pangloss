import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from operator import itemgetter
from collections import defaultdict
import seaborn as sns

def from_data_to_list(pickledata, num):
    data = pickledata[num]
    del(data[None])

    whole_list = []
    for key in data:
        list=[key, len(data[key])]
        whole_list.append(list)

    sorted_whole_list = sorted(whole_list, key=itemgetter(1), reverse = True)

    return(sorted_whole_list)

#Make graphs of gloses occurrences
def make_graphs(pickledata, num,type):
    sorted_whole_list = from_data_to_list(pickledata,num)
    sns.set()

    #First 10
    first10 = sorted_whole_list[:10]
    labels, ys = zip(*first10)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('First 10 {}'.format(type))
    plt.savefig('first_10_{}.png'.format(type))

    #Middle 10
    num = int(len(sorted_whole_list)/2)
    middle10 = sorted_whole_list[num-5:num+5]
    labels, ys = zip(*middle10)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('Middle 10 {}'.format(type))
    plt.savefig('middle_10_{}.png'.format(type))

    #Last 10
    last10 = sorted_whole_list[-10:]
    labels, ys = zip(*last10)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('Last 10 {}'.format(type))
    plt.savefig('last_10_{}.png'.format(type))

    #First 100
    first100 = sorted_whole_list[:100]
    labels, ys = zip(*first100)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('First 100 {}'.format(type))
    plt.savefig('first_100_{}.png'.format(type))

    #Middle 100
    num = int(len(sorted_whole_list)/2)
    middle100 = sorted_whole_list[num-50:num+50]
    labels, ys = zip(*middle100)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('Middle 100 {}'.format(type))
    plt.savefig('middle_100_{}.png'.format(type))

    #Last 100
    last10 = sorted_whole_list[-100:]
    labels, ys = zip(*last10)
    plt.figure(figsize=(20, 15))
    xs = np.arange(len(labels))
    width = 1
    plt.bar(xs, ys, width, align='center')
    plt.xticks(xs, labels, rotation=90, FontProperties=ChineseFont)
    plt.suptitle('Last 100 {}'.format(type))
    plt.savefig('last_100_{}.png'.format(type))

#Which gloses are in more than one language
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

#Which languages are shared by the gloses in the data.
def languages_in_gloses(data):
    languages = []
    for key, value in data.items():
        for i in value:
            if i not in languages:
                languages.append(i)
    return(languages)

ChineseFont = FontProperties("Microsoft YaHei")
pickledata = pickle.load(open('gloss.pkl', 'rb'))

#Graph for words:
make_graphs(pickledata,0,"words")

#Graph for morphemes:
make_graphs(pickledata,1,"morphemes")

#Gloss data for words
multiple_lang_gloss,length = multiple_language_gloss(pickledata,0)
print(length)
languages = languages_in_gloses(multiple_lang_gloss)
print(languages)

#Gloss data for morphems
multiple_lang_gloss,length = multiple_language_gloss(pickledata,1)
print(length)
languages = languages_in_gloses(multiple_lang_gloss)
print(languages)
