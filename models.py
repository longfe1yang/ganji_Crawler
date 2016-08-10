from pymongo import MongoClient

client = MongoClient()
collection = client['ganji']
first_grade = collection['page_url']
second_grade = collection['preview_url']
third_grade = collection['info_details']

if __name__ == '__main__':
    b = len(set([i['page_url'] for i in first_grade.find()]))
    a = first_grade.find().count()
    print(a, b)
