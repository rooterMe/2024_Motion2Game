# 2024_Motion2Game

2024년 충북과학고 교육기부 프로젝트

> 웹캠으로 사용자의 동작을 인식하고, MediaPipe Pose를 이용해 자세를 분석한 뒤, 특정 동작을 키보드 입력으로 변환하여 원래 키보드로 플레이하는 게임을 몸동작으로 조작할 수 있도록 만든 프로젝트입니다.
>
> with [김태용](https://github.com/DuvIsaac), 박우현
> 
## Overview

이 프로젝트는 웹캠에서 입력된 실시간 영상을 기반으로 사람의 자세를 추정하고, 팔의 각도와 손의 위치를 분석하여 특정 동작을 판별합니다.  
판별된 동작은 미리 정의한 키 입력으로 변환되며, 이를 통해 사용자는 키보드 대신 몸동작으로 게임을 플레이할 수 있습니다.

기본적인 동작 흐름은 다음과 같습니다.

1. 웹캠으로 사용자 영상을 입력받습니다.
2. MediaPipe Pose로 신체 랜드마크를 추출합니다.
3. 어깨, 팔꿈치, 손목, 골반 좌표를 이용해 팔 각도와 자세를 계산합니다.
4. 특정 자세를 미리 정의된 명령으로 분류합니다.
5. 해당 명령을 키보드 입력으로 변환하여 게임에 전달합니다.

## Key Mapping

### 손 (Hand)

Mediapipe의 손 모델은 각 손에 대해 21개의 랜드마크를 제공합니다. 각 랜드마크의 명칭은 다음과 같습니다:

- WRIST (0): 손목
- THUMB_CMC (1): 엄지손가락 뿌리 (손목과 엄지 사이)
- THUMB_MCP (2): 엄지손가락 첫 번째 마디
- THUMB_IP (3): 엄지손가락 두 번째 마디
- THUMB_TIP (4): 엄지손가락 끝
- INDEX_FINGER_MCP (5): 검지손가락 첫 번째 마디
- INDEX_FINGER_PIP (6): 검지손가락 두 번째 마디
- INDEX_FINGER_DIP (7): 검지손가락 세 번째 마디
- INDEX_FINGER_TIP (8): 검지손가락 끝
- MIDDLE_FINGER_MCP (9): 중지손가락 첫 번째 마디
- MIDDLE_FINGER_PIP (10): 중지손가락 두 번째 마디
- MIDDLE_FINGER_DIP (11): 중지손가락 세 번째 마디
- MIDDLE_FINGER_TIP (12): 중지손가락 끝
- RING_FINGER_MCP (13): 약지손가락 첫 번째 마디
- RING_FINGER_PIP (14): 약지손가락 두 번째 마디
- RING_FINGER_DIP (15): 약지손가락 세 번째 마디
- RING_FINGER_TIP (16): 약지손가락 끝
- PINKY_MCP (17): 새끼손가락 첫 번째 마디
- PINKY_PIP (18): 새끼손가락 두 번째 마디
- PINKY_DIP (19): 새끼손가락 세 번째 마디
- PINKY_TIP (20): 새끼손가락 끝

### 얼굴 (Face)
   
Mediapipe의 얼굴 모델은 468개의 랜드마크를 제공합니다. 이 중에서 주요 랜드마크 몇 가지는 다음과 같습니다:

- NOSE_TIP (1): 코 끝
- LEFT_EYE_INNER (33): 왼쪽 눈 안쪽 모서리
- LEFT_EYE (133): 왼쪽 눈 동공 중심
- LEFT_EYE_OUTER (263): 왼쪽 눈 바깥 모서리
- RIGHT_EYE_INNER (362): 오른쪽 눈 안쪽 모서리
- RIGHT_EYE (362): 오른쪽 눈 동공 중심
- RIGHT_EYE_OUTER (263): 오른쪽 눈 바깥 모서리
- MOUTH_LEFT (61): 입의 왼쪽 모서리
- MOUTH_RIGHT (291): 입의 오른쪽 모서리
- LEFT_EAR_TRAGION (234): 왼쪽 귀의 tragion (귀의 작은 돌기)
- RIGHT_EAR_TRAGION (454): 오른쪽 귀의 tragion (귀의 작은 돌기)
- CHIN (199): 턱 끝

전체 468개의 좌표명칭은 방대하며, 각 랜드마크는 번호로 구분됩니다.

### 포즈 (Pose)
   
Mediapipe의 포즈 모델은 33개의 주요 랜드마크를 제공합니다. 각 랜드마크의 명칭은 다음과 같습니다:

- NOSE (0): 코
- LEFT_EYE_INNER (1): 왼쪽 눈 안쪽
- EFT_EYE (2): 왼쪽 눈
- LEFT_EYE_OUTER (3): 왼쪽 눈 바깥쪽
- RIGHT_EYE_INNER (4): 오른쪽 눈 안쪽
- RIGHT_EYE (5): 오른쪽 눈
- RIGHT_EYE_OUTER (6): 오른쪽 눈 바깥쪽
- LEFT_EAR (7): 왼쪽 귀
- RIGHT_EAR (8): 오른쪽 귀
- MOUTH_LEFT (9): 입의 왼쪽
- MOUTH_RIGHT (10): 입의 오른쪽
- LEFT_SHOULDER (11): 왼쪽 어깨
- RIGHT_SHOULDER (12): 오른쪽 어깨
- LEFT_ELBOW (13): 왼쪽 팔꿈치
- RIGHT_ELBOW (14): 오른쪽 팔꿈치
- LEFT_WRIST (15): 왼쪽 손목
- RIGHT_WRIST (16): 오른쪽 손목
- LEFT_PINKY (17): 왼쪽 새끼손가락
- RIGHT_PINKY (18): 오른쪽 새끼손가락
- LEFT_INDEX (19): 왼쪽 검지손가락
- RIGHT_INDEX (20): 오른쪽 검지손가락
- LEFT_THUMB (21): 왼쪽 엄지손가락
- RIGHT_THUMB (22): 오른쪽 엄지손가락
- LEFT_HIP (23): 왼쪽 엉덩이
- RIGHT_HIP (24): 오른쪽 엉덩이
- LEFT_KNEE (25): 왼쪽 무릎
- RIGHT_KNEE (26): 오른쪽 무릎
- LEFT_ANKLE (27): 왼쪽 발목
- RIGHT_ANKLE (28): 오른쪽 발목
- LEFT_HEEL (29): 왼쪽 발 뒤꿈치
- RIGHT_HEEL (30): 오른쪽 발 뒤꿈치
- LEFT_FOOT_INDEX (31): 왼쪽 발의 검지 발가락
- RIGHT_FOOT_INDEX (32): 오른쪽 발의 검지 발가락
