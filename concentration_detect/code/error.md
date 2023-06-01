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

