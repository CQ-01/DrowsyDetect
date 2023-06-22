from django import forms
from .models import UserInfo, TutorInfo, LectureInfo, EventInfo, ResultInfo

# class UserInfoForm(forms.ModelForm):
#     # image -> imagefile 변경 
#     class Meta:
#         model = UserInfo
#         fields = (
#                 'user_id',
#                 'password',
#                 'user_name',
#                 'email',
#                 'registration_date'
#         )  
   
# class TutorInfoForm(forms.ModelForm):
#     class Meta:
#         model = TutorInfo
#         fields = (
#                 'tutor_Id',
#                 'password' ,
#                 'tutor_Name',
#                 'email',
#                 'registration_date'
#         )  

# class LectureInfoForm(forms.ModelForm):
#     class Meta:
#         model = LectureInfo
#         fields = (
#                 'lecture_Id',
#                 'lecture_Name' ,
#                 'tutor_Id',
#                 'recommended',
#                 'lectureUrl',
#                 'lectureLength', 
#                 'registration_date'
#         )  

# class ResultInfoForm(forms.ModelForm):
#     class Meta:
#         model = ResultInfo
#         fields = (
#                 'result_Id', 
#                 'user_Id', 
#                 'lectureId', 
#                 'captureStart', 
#                 'captureEnd', 
#                 'startLog', 
#                 'endLog',
#                 'registration_date'
#         )
<<<<<<< Updated upstream

# class EventInfoForm(forms.ModelForm):
#     class Meta:
#         model = EventInfo
#         fields = (
#                 'eventId', 
#                 'resultId', 
#                 'lectureId', 
#                 'StartTime', 
#                 'rndTime', 
#                 'continuedTime',
#                 'registration_date'
#         )

# class LectureListForm(forms.Form):

#     user_id = forms.CharField()
#     tutorId = forms.CharField()
#     tutorName = forms.CharField()
#     lectureId = forms.CharField()
#     lectureName = forms.CharField()
#     lectureUrl = forms.CharField()

<<<<<<< Updated upstream
class EventInfoForm(forms.ModelForm):
    class Meta:
        model = EventInfo
        fields = (
                'eventId', 
                'resultId', 
                'lectureId',
                'awake',
                'sleep',
                'stateNo',
                'continuedTime',
                'registrationDate'
        )
    
=======
>>>>>>> Stashed changes
=======

# class EventInfoForm(forms.ModelForm):
#     class Meta:
#         model = EventInfo
#         fields = (
#                 'eventId', 
#                 'resultId', 
#                 'lectureId', 
#                 'StartTime', 
#                 'rndTime', 
#                 'continuedTime',
#                 'registration_date'
#         )

# class LectureListForm(forms.Form):

#     user_id = forms.CharField()
#     tutorId = forms.CharField()
#     tutorName = forms.CharField()
#     lectureId = forms.CharField()
#     lectureName = forms.CharField()
#     lectureUrl = forms.CharField()

>>>>>>> Stashed changes
