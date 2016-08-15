import time
import models

while True:
    print(models.second_grade.find().count(), models.third_grade.find().count())
    time.sleep(4)
