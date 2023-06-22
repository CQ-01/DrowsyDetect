import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Lecture, Result, Tutor, Event, UserLecture
from django.db.models import Sum, Count
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import tensorflow as tf
from tensorflow.keras.models import load_model
import dlib
from scipy.spatial import distance
import numpy as np
from datetime import datetime

# Create your views here.
def lecture_list(request):
    return render(request, 'EO_001.html', {})


def get_lecture_name(request):
    
    userId = request.GET.get('user')
    
    lecture_list = []
    results = UserLecture.objects.filter(user=userId, finish=0)
    #results = Lecture.objects.prefetch_related('tutor')#.filter(lecture__lecture_id=123456789)
    #.filter(user=userId)#.get(user=userId)#.values_list("user", "lecture","lecture_name" )
    
    for result in results:
        # print(result)
        
        lecture_id = result.lecture
        lectures = Lecture.objects.select_related('tutor').filter(lectures__lecture_id=lecture_id)
        for lecture in lectures:
            # print(lecture)
            strTime = str(lecture.lecture_length)
            # print(strTime)
            #inStrTime = strTime.split()
            # print(strTime[0:2]+':'+strTime[2:4])
            lecture_list.append({"user": userId,
                         "lecture": lecture.lecture,
                         "lecture_name": lecture.lecture_name,
                         "lecture_length": strTime[0:2]+':'+strTime[2:4], 
                         "tutor": lecture.tutor_id,
                         "tutor_name" :lecture.tutor.tutor_name})
        
            # print("-------------------------------------------------------------------")
            # print(strTime)

    return render(request, 'EO_001.html', {'lectures' : lecture_list})

# 수강 화면 표시 
def lecture_play(request):
    # print(request)
    if request.method == 'GET':
        userId = request.GET.get('user')
        lectureId = request.GET.get('lecture')
    else:
        # POST 방식 
        print(request)
 
    user = User.objects.get(user=userId)
    lecture = Lecture.objects.get(lecture=lectureId)
    result = Result.objects.create(
        user = user, 
        lecture = lecture, 
        capture_start = datetime.now().time(),
        capture_end = datetime.now().time(),
        start_log = datetime.now().time(),
        end_log = datetime.now().time(),
        registration_date = datetime.now()
    )
    # print("*****************")
    # print(result)
    # print("*****************")
    
    return render(request, 'EO_002.html', {'result':result})   

def lecture_sort(request):
    # 사용자 ID를 가져옴 (request를 통해 전달된 데이터)
    user_id = request.GET.get('userId')
    results = ""

    # 결과를 JSON 형식으로 반환
    data = {
        'results': results,
    }
    return JsonResponse(data)

def check_user_info(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId')
        password = data.get('password')

        # UserInfo 모델에서 사용자 정보와 일치하는지 확인
        try:

            user = User.objects.get(user = user_id, password = password)

            if (user.user_name != None):
                valid = True
            else:
                valid = False 

        except User.DoesNotExist:
            valid = False
          
       
    else:
        print("else---------------------")

    response_data = {'valid': valid}

    return JsonResponse(response_data)



# 모델 적용 부분 시작 

# 
def loss_fn(y_true, y_pred):
  cls_labels = tf.cast(y_true[:,:1], tf.int64)
  loc_labels = y_true[:,1:]
  cls_preds = y_pred[:,:2]
  loc_preds = y_pred[:,2:]
  cls_loss = tf.keras.losses.SparseCategoricalCrossentropy()(cls_labels, cls_preds)
  loc_loss = tf.keras.losses.MeanSquaredError()(loc_labels, loc_preds)
  return cls_loss + 2*loc_loss

model = load_model('ocds\models\MobileNetV3LargeMaxPooling_newest_hope_158- val_loss_ 0.10- loss_ 0.00.h5',custom_objects={'loss_fn': loss_fn})


def calculate_EAR(eye): # 눈 거리 계산
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear_aspect_ratio = (A+B)/(2.0*C)
	return ear_aspect_ratio


hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("ocds\models\shape_predictor_68_face_landmarks.dat")


# def home(request):
#     context = {}

#     return render(request, "home.html", context)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        self.count = 0
        # 30프레임이라고 가정하면 1/30초당 1장을 처리
        self.sleep = 0
        self.awake = 0
        

    def __del__(self):
        self.video.release()

    def get_frame(self, resultId):
        

        image = self.frame
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = hog_face_detector(gray)
        stateNo = 0
        state = ''
        
        for face in faces:

            face_landmarks = dlib_facelandmark(gray, face)
            leftEye = []
            rightEye = []

            for n in range(36,42): # 오른쪽 눈 감지
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x,y))
                next_point = n+1
                if n == 41:
                    next_point = 36
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(image,(x,y),(x2,y2),(0,255,0),1)

            for n in range(42,48): # 왼쪽 눈 감지
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x,y))
                next_point = n+1
                if n == 47:
                    next_point = 42
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(image,(x,y),(x2,y2),(0,255,0),1)

            left_ear = calculate_EAR(leftEye)
            right_ear = calculate_EAR(rightEye)

            EAR = (left_ear+right_ear)/2
            EAR = round(EAR,2)

            if EAR<0.29:
                state = 'close'
                # print(EAR)
            else:
                state = 'open'
                
    # 강지윤 파트
    
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        shape = image.shape
        preprocessed_image = image/255.
        preprocessed_image= cv2.resize(preprocessed_image,(224,224))
        input_img = np.reshape(preprocessed_image, (1,224,224,3))
        attention_prediction = model(input_img)
        #1행 6열의 데이터
        text = ''
        #drowsy, awake
        
        # print(prediction)
        label = np.argmax(attention_prediction[:, :2],axis = 1)
        #깨어있으면 0 리턴 졸리면 1리턴
        box = attention_prediction[:, 2:]
        box = np.squeeze(box)
        
        
        x = box[0]*shape[1]
        y = box[1]*shape[0]
        w = box[2]*shape[1]
        h = box[3]*shape[0]
        
        xmin = int(x - w/2.)
        ymin = int(y - h/2.)
        xmax = int(x+w/2.)
        ymax = int(y+h/2.)


        if label[0] == 0:
            text = 'awake'
        elif label[0] == 1:
            text = 'drowsy'
            
    
        if self.count != self.video.get(cv2.CAP_PROP_FPS):
            #만약 2초당 한번 데이터 베이스에 넣고 싶으시다면 self.video.get(cv2.CAP_PROP_FPS)에 2를 곱하세요
            if text == 'drowsy':
                self.sleep += 0.3
                if state == 'close':
                    self.sleep += 0.7
                elif state == 'open':
                    pass
                else:
                    self.sleep += 0.2
            else :
                if state == 'close':
                    self.sleep += 0.7
                elif state == 'open':
                    self.awake +=1
                else:
                    self.awake += 0.1
            
            self.count+=1
            
            print('sleep : ', self.sleep, 'awake : ', self.awake, 'count : ', self.count)
            #확인 용 코드 매 프레임마다 sleep awake를 확인   
        else:
            # 이쪽 부분에 데이터베이스에 저장하는 코드를 작성하시면 될겁니다. 만약 awake sleep 둘다를 저장하려면
            # 저장 
            # TB - Event table, Result table 
            
            if self.awake > self.sleep:
                stateNo = 0
            else:
                stateNo = 1
                
            saveEvent(resultId, self.sleep, self.awake, stateNo)
            
            self.sleep = 0
            self.awake = 0
            self.count = 0
            
            
                         
        cv2.putText(image, 'State: {}' .format(state), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        ###
        cv2.rectangle(image,(xmin,ymin),(xmax,ymax), color = (0,0,255))
        cv2.putText(image, text, (xmin+2, ymin-10), cv2.FONT_HERSHEY_PLAIN,2,color = (0,0,255))
        ### 
                
                
        
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera, resultId):
    # print("gen------------resultId-----")
    # print(resultId)
    # resultId = str(resultId)
    while True:
        frame = camera.get_frame(resultId)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def detectme(request):
    
    print("################")
    resultId = request.GET.get('result')
    print(resultId)
    # result = Result.objects.get(result=resultId)
    # print(result)
    
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam, resultId), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

# Event 테이블에 저장 
def saveEvent(resultId, sleep, awake,state): #ResultInfo, LectureInfo):

    result = Result.objects.get(result = resultId)
    lectureId = result.lecture.lecture
    print(lectureId)
    lecture = Lecture.objects.get(lecture = lectureId)
    # print(lecture)
    
    event = Event.objects.create(
        result = result, 
        lecture = lecture, 
        # start_time = datetime.now(),  # 동영상 재생 시작 시간 
        # end_time = datetime.now() ,    # 동영상 재생 끝 시간 
        start_time = datetime.now(),  # 동영상 재생 시작 시간 
        end_time = datetime.now() ,    # 동영상 재생 끝 시간 
        sleep = sleep,
        awake = awake,
        stateNo = state,
        registration_date = datetime.now() 
    )
 
    

# 수강자 집중도 그래프 화면 표시    
def viewGraphUser(request):
    userId = request.GET.get('user')
    lectureId = request.GET.get('lecture')
    
    user = User.objects.get(user=userId)
    lecture = Lecture.objects.get(lecture=lectureId)
    
    # print('userId : ',userId)
    # print('lectureId : ',lectureId)
    result = Result.objects.filter(lecture=lecture, user=user)
    # 수강자의 선택 과목에 대한 조건을 추가 
    print(result.query)
    # data = Event.objects.all()
    
    data = Event.objects.filter(lecture=lecture, result__in=result)  
    
    # 유저수와 강의수 
    # -----------------------------------------
    # numOfUsers = User.objects.aggregate(Count('user'))
    # print(numOfUsers)
    # numOfLectures = Lecture.objects.aggregate(Count('lecture'))
    # print(numOfLectures)
    # ------------------------------------------
    numOfUsers = 1
    numOfLectures = 1
    # END
           
    #sleep, awake 갯수 
    #------------------------------------------\
    numOfSleep = len(Event.objects.filter(stateNo = 1, lecture=lecture, result__in=result))
    numOfAwake = len(Event.objects.filter(stateNo = 0, lecture=lecture, result__in=result))

    print('numOfAwake : ', numOfAwake)
    print('numOfSleep : ', numOfSleep)
    print('lectureName', lecture.lecture_name)
    #user에 해당하는 조건
    arr = [i for i in range(0, len(data))]
    print(arr)
    context = {
        'data' : data,
        'range': arr,
        'lectureName': lecture.lecture_name,
        'userName' : user.user_name,
        'numOfUsers': numOfUsers, #['user__count'],
        'numOfLectures': numOfLectures, # ['lecture__count'],
        'numOfAwake': numOfAwake,
        'numOfSleep': numOfSleep
        }
    # return render(request, 'EO_003.html', context)
    return render(request, 'EO_003.html', context)
    




# 강사의 과목에 해당하는 집중도 그래프 화면 표시    
def viewGraphTutor(request):
    lectureId = request.GET.get('lecture')
    tutorId = request.GET.get('tutor')

    print('lectureId : ', lectureId)
    print('tutorId : ', tutorId)

    tutor = Tutor.objects.get(tutor = tutorId)
    lecture = Lecture.objects.get(lecture=lectureId, tutor=tutor)
              
    # 사용자 수와 강사가 맡은 과목 수 
    #print("-----------------------------------------")
    numOfUsers = UserLecture.objects.filter(lecture_id=lectureId).count()
    #print(numOfUsers)
    numOfLectures = Lecture.objects.filter(tutor_id=tutorId).count()
    #print(numOfLectures)
    #print("------------------------------------------")
    # END
    
    result = Result.objects.filter(lecture=lecture)
    # 수강자의 선택 과목에 대한 조건을 추가 
               
    #sleep, awake 갯수 
    #------------------------------------------\
    numOfSleep = len(Event.objects.filter(stateNo = 1, lecture=lecture, result__in=result))
    numOfAwake = len(Event.objects.filter(stateNo = 0, lecture=lecture, result__in=result))

    print('numOfAwake : ', numOfAwake)
    print('numOfSleep : ', numOfSleep)
           
    # 수강자의 선택 과목에 대한 조건을 추가 
    
    data = Event.objects.filter(lecture=lecture, result__in=result)  
    print(data)
    #user에 해당하는 조건
    arr = [i for i in range(0, len(data))]
    
    context = {
        'data' : data,
        'range': arr,
        'lectureName': lecture.lecture_name,
        'tutorName': tutor.tutor_name,
        'numOfUsers': numOfUsers, #['user__count'],
        'numOfLectures': numOfLectures, # ['lecture__count'],
        'numOfAwake': numOfAwake,
        'numOfSleep': numOfSleep
        }
    # return render(request, 'EO_003.html', context)
    return render(request, 'EO_004.html', context)