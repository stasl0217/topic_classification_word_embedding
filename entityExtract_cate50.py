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


# documents: plain text, every element accords to one article
# cate: the category index of every document
[documents, cate] = data_fetcher.DataFetcher().get_classified_training_data()  # balanced

N = len(documents)
print("number of documents" + str(N))
M = 20  # number of categories  # this may need to be CHANGED for IMBALANCED DATASET
print("number of categories" + str(M))

# take only 50 random documents from each category to reduce the query pressure
cate_doc_count = []  # the count of processed articles in every category
for k in range(0, M):
    cate_doc_count.append(0)  # skip the query when count reached 50 later

with open("tags_50.txt", "a") as f:
    with open("id_50.txt", "a") as f_id:
        with open("cate_50.txt", "a") as f_cate:
            for i in range(0, len(documents)):

                doc = documents[i]
                doc_cate = cate[i]
                if (cate_doc_count[doc_cate] < 50):
                    # query the first random 50 articles in every category

                    cate_doc_count[doc_cate] += 1

                    # query text can't be too long, break it and then query
                    size = 5000
                    length = len(doc)
                    for j in range(0, length - 1, size):
                        # may cut some words. could be fixed if bette r methods available
                        small_text = doc[j:min(j + size, length - 1)].lstrip()
                        try:
                            entities = queryTagMe(small_text)
                            print(entities)
                            for e in entities:
                                f.write(e + '\t')
                        except:
                            with open("exceptions.txt", "a") as fe:
                                fe.write(str(i) + '\n')
                                fe.write(str(sys.exc_info()[0]))
                                fe.write(small_text)
                                fe.write('\n\n\n')
                    f.write('\n')
                    f_id.write(str(i) + '\n')
                    f_cate.write(str(doc_cate) + '\n')
