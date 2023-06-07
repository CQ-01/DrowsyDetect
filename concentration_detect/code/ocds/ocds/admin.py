from django.contrib import admin
from .models import User, Tutor, Lecture, Result, Event, UserLecture


# Register your models here.
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Lecture) 
admin.site.register(Result) 
admin.site.register(Event) 
admin.site.register(UserLecture) 
##//, LectureInfo, ResultInfo, EventInfo)

