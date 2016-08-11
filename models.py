from pymongo import MongoClient

client = MongoClient()
collection = client['ganji']
first_grade = collection['page_url']
second_grade = collection['preview_url']
third_grade = collection['info_details']

if __name__ == '__main__':
    b = len(set([i['url'] for i in third_grade.find()]))
    a = second_grade.find().count()
    print(a, b)
    # a = [i['channel'] for i in second_grade.find()]
    # b = 'http://bj.ganji.com/xianzhilipin/'
    # if b in a:
    #     print(True)
