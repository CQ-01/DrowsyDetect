from django.db import models
from django.utils import timezone

## 자동으로 증가하는 primary key setting
# class CustomAutoField(models.AutoField):
    
#     def db_type(self, connection):
#             return 'mediumint(8) UNSIGNED AUTO_INCREMENT'
#     def rel_db_type(self, connection):
#         return 'mediumint(8) UNSIGNED'


## 사용자 테이블 
class User(models.Model):
    user = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=50, default=0000)
    user_name = models.CharField(max_length=50, default='김학생')
    email = models.CharField(max_length=100, default='default@example.com')
    registration_date = models.DateTimeField(default = timezone.now)
    
## 강사 테이블 
class Tutor(models.Model):
    tutor = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=50, default=0000)
    tutor_name = models.CharField(max_length=50, default='박선생')
    email = models.CharField(max_length=100, default='default@example.com')
    registration_date = models.DateTimeField(default = timezone.now)


class Lecture(models.Model):
	lecture = models.BigAutoField(primary_key=True)
	lecture_name = models.CharField(max_length=100, default="강사명")
	tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
	recommended = models.FloatField(default = 0)
	lecture_url = models.CharField(max_length=250, default='https://example.com/default-url')
	lecture_length = models.IntegerField(default=0)
	registration_date = models.DateTimeField(default = timezone.now) 

class Result(models.Model):
    result = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    capture_start = models.TimeField(default=timezone.now)
    capture_end = models.TimeField(default=timezone.now)
    start_log = models.TimeField(default=timezone.now)
    end_log = models.TimeField(default=timezone.now)
    registration_date = models.DateTimeField(default = timezone.now) 

class Event(models.Model):
    event = models.BigAutoField(primary_key = True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    sleep = models.FloatField(default=0.0)
    awake = models.FloatField(default=0.0)
    stateNo = models.IntegerField(default=0)
    continued_time = models.IntegerField(default=0)
    registration_date = models.DateTimeField(default = timezone.now) 

class UserLecture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="lectures")
    finish = models.CharField(max_length=10, default="0")
    registration_date = models.DateTimeField(default = timezone.now) 


