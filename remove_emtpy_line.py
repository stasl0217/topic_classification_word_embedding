in_tags = 'tags_full_test.txt'
in_id = 'id_full_test.txt'
in_cate = 'cate_full_test.txt'

out_tags = 'tags_test.txt'
out_id = 'id_test.txt'
out_cate = 'cate_test.txt'

docs = []
empty_id = []
count = 0
for line in open(in_tags):
    line = line.rstrip('\n')  # don't split by '\t'
    if line == "":
        print("emtpy string")
        print(count)
        empty_id.append(count)
    else:
        docs.append(line)
    count += 1

ids = []
for id in open(in_id):
    ids.append(id)

cates = []
for c in open(in_cate):
    cates.append(c)

with open(out_tags, 'w') as fout:
    for doc in docs:
        fout.write(doc)
        fout.write('\n')

with open(out_id, 'w') as fout_id:
    for i in range(0, len(ids)):
        if i not in empty_id:
            fout_id.write(ids[i])

with open(out_cate, 'w') as fout_cate:
    for k in range(0, len(cates)):
        if k not in empty_id:
            fout_cate.write(cates[k])
