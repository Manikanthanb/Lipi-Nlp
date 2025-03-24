import pickle,docx
hash_table = {}

def insert(key, value):
    # print(key+"insert"+value)
    hash_key = hash(key)
    # print(hash_key)
    if hash_key in hash_table:
        hash_table[hash_key].append(value)
    else:
        hash_table[hash_key] = value

def search(key):
    hash_key = hash(key)
    try:
        with open('hash_table.pkl', 'rb') as f:
            hash_table = pickle.load(f)
            return hash_table[hash_key]
    except (FileNotFoundError, KeyError):
        return None
    
doc = docx.Document('actual.docx')

lines = [p.text for p in doc.paragraphs]
# print(lines)
my_dict = {}

for line in lines:
    if ' - ' in line:  
        key, value = line.split(' - ')
        # print(value)
        v1=(value.strip()).split(' ')
        # print(v1[0].strip())
        my_dict[key.strip()] = v1

print(my_dict)
new_doc = docx.Document()
f=open('output3.txt', 'w', encoding='utf-8',errors="ignore")
for key, value in my_dict.items():
    insert(key, value)

with open('hash_table.pkl', 'wb') as f:
    pickle.dump(hash_table, f)
    print(hash_table)


    # print(key+"value "+value)
#     # f.write(key )
    # f.write(value)
    # print(key)
    # print("hdj"+value)
    # new_doc.add_paragraph(key.encode('utf-8').decode('utf-8'))
    # new_doc.add_paragraph( value.encode('utf-8').decode('utf-8'))

# new_doc.save('new.docx')

result = search('ಅಂಕ')
print(result)
result = search('ಅಂಕಣಿ')
print(result)

# if result:
#     with open('output2.txt', 'w', encoding='utf-8',errors="ignore") as f:
#         for value in result:
#             f.write(value + '\n')


