import os
import json
import requests
import data_fetcher
import sys


def findFiles(rootDir):
    filePaths = []  # id-filePath
    fileClusters = []  # id-cluster id(from 0)
    k = 0;  # cluster count / current id
    for dirs in os.listdir(rootDir):
        dirpath = os.path.join(rootDir, dirs)
        if os.path.isdir(dirpath):  # just in case
            # file under the same dir belong to one cluster
            for file in os.listdir(dirpath):
                filepath = os.path.join(dirpath, file)
                filePaths.append(filepath)
                fileClusters.append(k)
        k = k + 1
    return [filePaths, fileClusters]


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


def decodeJsonForEntities(json_data):
    data = json.loads(json_data, object_hook=JSONObject)
    annotations = data.annotations  # entities in json
    es = []  # entity list
    for entity in annotations:
        entity_name = entity.title
        es.append(entity_name)
    return es


def queryTagMe(text):
    token = "a1166a48-6fbe-4afd-a0b7-1f3f949b2511-843339462"
    url = "https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=" + token + "&text=" + text
    r = requests.get(url)
    print(r.status_code)
    json_data = r.text
    # print(json_data)
    entities = decodeJsonForEntities(json_data)
    return entities


documents = data_fetcher.DataFetcher().get_data()  # balanced

print(len(documents))

# # skewed
# bc = ['alt.atheism','rec.sport.baseball','talk.politics.guns']
# ic = ['sci.space']
# d = .7
# ### initialize DataFetcher and get the documents
# df2 = data_fetcher.DataFetcher(bc,ic,d)
with open("tags_full.txt","a") as f:
    for i in range(0,len(documents)):
        text=documents[i]
        # query text can't be too long
        size = 5000
        length = len(text)
        for i in range(0, length - 1, size):
            # may cut some words. could be fixed if bette r methods available
            small_text = text[i:min(i + size, length - 1)].lstrip()
            try:
                entities = queryTagMe(small_text)
                print(entities)
                for e in entities:
                    f.write(e+'\t')
            except:
                with open("exceptions.txt","a") as fe:
                    fe.write(small_text)
                    fe.write(str(sys.exc_info()[0]))

        f.write('\n')
