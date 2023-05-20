## I. 테이블 구축 및 관리
```SQL
-- DB 생성
CREATE DATABASE [DB명];
USE [DB명];

-- 테이블 일람
SHOW TABLES;
```
### 1. 테이블 생성
```SQL
CREATE TABLE TBL_USER (
    User_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Password VARCHAR(50) NOT NULL,
    User_name VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE TBL_TUTOR (
    Tutor_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	Password VARCHAR(50) NOT NULL,
	Tutor_name VARCHAR(50) NOT NULL,
	Email VARCHAR(100) NOT NULL,
	Registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE TBL_LECTURE (
	Lecture_id BIGINT AUTO_INCREMENT PRIMARY KEY,
	Lecture_name VARCHAR(100) NOT NULL,
	Tutor_id BIGINT NOT NULL,
	Recommended FLOAT NOT NULL,
	Lecture_url VARCHAR(250) NOT NULL,
	Lecture_length INT NOT NULL,
	Registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
	FOREIGN KEY (Tutor_id) REFERENCES TBL_TUTOR(Tutor_id)
);

CREATE TABLE TBL_RESULT (
    Result_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    User_id BIGINT NOT NULL,
    Lecture_id BIGINT NOT NULL,
    Capture_start TIME NOT NULL,
    Capture_end TIME NOT NULL,
    Start_log TIME NOT NULL,
    End_log TIME NOT NULL,
    Registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (User_id) REFERENCES TBL_USER(User_id),
    FOREIGN KEY (Lecture_id) REFERENCES TBL_LECTURE(Lecture_id)
);

CREATE TABLE TBL_EVENT (
    Event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    Result_id BIGINT NOT NULL,
    Lecture_id bigint not null,
    Start_time DATETIME NOT NULL,
    End_time DATETIME NOT NULL,
    Continued_time INT NOT NULL,
    Registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (Result_id) REFERENCES TBL_RESULT(Result_id),
    FOREIGN KEY (Lecture_id) REFERENCES TBL_LECTURE(Lecture_id)
);
```
### 2. 테이블 수정
> FOREIGN KEY 설정 때문에 반드시 아래 순서로 삭제해야 함

    DROP TABLE tbl_event;
    DROP TABLE tbl_result;
    DROP TABLE tbl_lecture;
    DROP TABLE tbl_tutor;
    DROP TABLE tbl_user;

### 3. 가상 데이터 입력
```SQL
 -- 사용자 테이블 (TBL_USER)
INSERT INTO TBL_USER (User_id, Password, User_name, Email, Registration_date)
VALUES
    (123456789, 'password1', 'User1', 'user1@example.com', NOW()),
    (234567890, 'password2', 'User2', 'user2@example.com', NOW()),
    (345678901, 'password3', 'User3', 'user3@example.com', NOW());

-- 강사명 테이블 (TBL_TUTOR)
INSERT INTO TBL_TUTOR (Tutor_id, Password, Tutor_name, Email, Registration_date)
VALUES
    (987654321, 'password4', 'Tutor1', 'tutor1@example.com', NOW()),
    (876543210, 'password5', 'Tutor2', 'tutor2@example.com', NOW()),
    (765432109, 'password6', 'Tutor3', 'tutor3@example.com', NOW());

-- 강의정보 테이블 (TBL_LECTURE)
INSERT INTO TBL_LECTURE (Lecture_id, Lecture_name, Tutor_id, Recommended, Lecture_url, Lecture_length, Registration_date)
VALUES
    (123456789, 'Lecture1', 987654321, 60.5, 'https://lecture1.com', 3600, NOW()),
    (234567890, 'Lecture2', 876543210, 45.5, 'https://lecture2.com', 2700, NOW()),
    (345678901, 'Lecture3', 765432109, 30.5, 'https://lecture3.com', 1800, NOW());

-- 수강결과 테이블 (TBL_RESULT)
INSERT INTO TBL_RESULT (Result_id, User_id, Lecture_id, Capture_start, Capture_end, Start_log, End_log, Registration_date)
VALUES
    (12345678901, 123456789, 123456789, '09:00:00', '10:00:00', '09:00:00', '10:00:00', NOW()),
    (23456789012, 234567890, 234567890, '11:00:00', '12:00:00', '11:00:00', '12:00:00', NOW()),
    (34567890123, 345678901, 345678901, '13:00:00', '14:00:00', '13:00:00', '14:00:00', NOW());

-- 졸음 이벤트 테이블 (TBL_EVENT)
INSERT INTO TBL_EVENT (Event_id, Result_id, Lecture_id, Start_time, End_time, Continued_time, Registration_date)
VALUES
    (123456789012, 12345678901, 123456789, '2023-05-12 09:30:00', '2023-05-12 09:45:00', 900, NOW()),
    (234567890123, 23456789012, 234567890, '2023-05-12 11:15:00', '2023-05-12 11:30:00', 900, NOW()),
    (345678901234, 34567890123, 345678901, '2023-05-12 13:30:00', '2023-05-12 13:00:00', 900, NOW());
```

## II. 시스템 활용 SQL문
### 1. 사용자별 강의 목록
```SQL
SELECT TBL_USER.User_name, TBL_LECTURE.Lecture_name
FROM TBL_USER
INNER JOIN TBL_RESULT ON TBL_USER.User_id = TBL_RESULT.User_id
INNER JOIN TBL_LECTURE ON TBL_RESULT.Lecture_id = TBL_LECTURE.Lecture_id
WHERE TBL_USER.User_id = [사용자 ID];
```

### 2. 강의명에 해당하는 동영상 정보
```SQL
SELECT * FROM TBL_LECTURE WHERE Lecture_name = ['강의명'];
```
### 3. 특정 강사의 과목별 집중도
```SQL
SELECT Lecture_name, Recommended, SUM(((Lecture_length) - TIMEDIFF(End_time, Start_time)) / (Lecture_length) * 100) AS Awake_time_ratio
FROM TBL_LECTURE L
INNER JOIN TBL_TUTOR T ON L.Tutor_id = T.Tutor_id
INNER JOIN TBL_EVENT E ON L.Lecture_id = E.Lecture_id
WHERE T.Tutor_id = [강사 id];
```
### 4. 사용자가 선택한 과목별 집중도
```SQL
SELECT User_name, Recommended, SUM(((Lecture_length) - TIMEDIFF(End_time, Start_time)) / (Lecture_length) * 100) AS Awake_time_ratio
FROM TBL_USER U
INNER JOIN TBL_RESULT R ON U.User_id = R.User_id
INNER JOIN TBL_EVENT E ON R.Result_id = E.Result_id
INNER JOIN TBL_LECTURE L ON R.Lecture_id = L.Lecture_id
WHERE R.User_id = [유저 id];
```
### 5. 졸음 이벤트 insert
```SQL
INSERT INTO TBL_EVENT (Result_id, Lecture_id, Start_time, End_time, Continued_time, Registration_date)
SELECT R.Result_id, R.Lecture_id, R.Start_log, R.End_log, 
       TIMESTAMPDIFF(SECOND, R.Start_log, R.End_log) AS Continued_time, 
       NOW() AS Registration_date
FROM TBL_RESULT R
WHERE [졸음 이벤트 조건];
```