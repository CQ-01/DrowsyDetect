## 장고 환경 관련
### 장고 프로젝트 구동 불가
```py
python -m venv "환경명"
# 가상환경 생성
"환경명"\Scripts\activate
# cmd 가상환경 활성화
conda activate "환경명"
# anaconda prompt 가상환경 활성화
```
### dlib 설치 불가
- pip install로 진행 안됨
  - 경고문 : `Failed building wheel for dlib`
- cmake 선행 설치 필요 확인, 설치 이후에도 동일 증상
- conda prompt : `conda install -c conda-forge dlib`
  - 여전히 진행 안되었으나 하위 버전으로 설치하여 해결

### DB와 장고프로젝트간 데이터 상이
- migrations 폴더의 initial 파일 삭제 후 재이식하여 해결
- 장고프로젝트는 테이블명 앞에 자동으로 '프로젝트명_'을 붙여 DB를 만듦, 이를 소스코드에 반영하여 해결
- 장고프로젝트는 Foreign Key 컬럼에 자동으로 _id를 붙임, 이를 소스코드에 반영하여 해결