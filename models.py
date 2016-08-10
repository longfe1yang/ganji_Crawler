from pymongo import MongoClient

client = MongoClient()
collection = client['ganji']
first_grade = collection['page_url']
second_grade = collection['preview_url']
third_grade = collection['info_details']

# b = len(set([i['url'] for i in second_grade.find()]))
# a = second_grade.find().count()
# print(a, b)
