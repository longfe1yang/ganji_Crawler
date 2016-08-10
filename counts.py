import time
import models

while True:
    print(models.second_grade.find().count())
    time.sleep(5)