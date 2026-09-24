# math-arena 레슨 스키마 v1.0

경로: content/level{N}/{course}/ch{NN}/l{NN}.json
- 코스 목록: content/level{N}/{course}/course.json
- 챕터 목록: content/level{N}/{course}/ch{NN}/chapter.json
- 챕터 복습 세트: content/level{N}/{course}/ch{NN}/review.json

## 레슨 파일
- course / chapter / lesson: id, 번호, 제목 (lesson.minutes = 예상 소요 시간)
- tags.domain: 학문 분과 태그(대수·해석·기하위상·확률통계·이산조합), tags.region, tags.curriculum
- screens: 화면 배열. 순서대로 표시. stage = intro | discover | summary | apply
- 분량 기준: 레슨당 화면 20~24개, 문항 15~17개

## 복습 세트 파일(review.json)
- review: id, title, minutes
- questions: 문항 10개(레슨 문항과 같은 형식), stage = review, source_lesson = 출제 레슨 id
- 챕터의 모든 레슨에서 출제. 간격 복습과 진단 문항 풀로 재사용

## 화면 유형
- explain: title, body(문단 배열), figure(선택, 정적 위젯: number_line, area_model, right_triangle, graph)
  - area_model: config.rows / config.cols 에 변 이름 배열, 칸마다 행×열 넓이를 표시
  - right_triangle: config.legs·hypotenuse(변 이름), squares(각 변 위 정사각형 표시), angle·labels(삼각비 기준각과 변 이름)
- question: qtype별 필드
  - numeric: answer(문자열), answer_format(integer | fraction | decimal), tolerance
    - fraction은 동치 분수 허용 여부를 플레이어에서 결정(권장: 기약분수만 정답)
  - fill_blank: prompt 안 {{n}} 자리, blanks[n].answers(허용 답 목록), unordered_groups(순서 무관 빈칸 묶음)
    - 허용 답에는 마이너스(- / −)와 거듭제곱(² / ^2) 표기 변형이 미리 들어 있음
    - 플레이어는 비교 전 공백 제거 권장
  - ordering: items(표시 순서), answer_order(정답 id 순서)
  - diagram: widget별 설정
    - number_line: config(min, max, step), answer.value, answer.tolerance
    - coordinate_plane: config(xmin, xmax, ymin, ymax, xstep, ystep), answer.x, answer.y, answer.tolerance
  - written: rubric(visibility=hidden, keyword_groups, min_groups_matched), model_answer
    - 채점: 각 그룹 중 하나라도 포함되면 그룹 일치, 일치 그룹 수가 기준 이상이면 통과
    - rubric은 화면에 노출하지 않음
- 공통: hint(선택), explanation(정답 확인 후 표시), figure(선택, 문제 아래에 표시할 정적 그림)

## graph 위젯
- config: xmin, xmax, ymin, ymax, xstep, ystep, curves, points(선택, [x, y, 라벨]), xpi(선택, true이면 x축 눈금을 π/2, π처럼 표시)
- curves 종류(kind)
  - poly: coef = 오름차순 계수 [c0, c1, c2, …]
  - circle: cx, cy, r
  - rational: y = k/(x − p) + q
  - sqrt: y = a√(b(x − p)) + q
  - abs: y = a|x − p| + q
  - exp: y = a·b^(x − p) + q
  - log: y = a·log_b(x − p) + q
  - trig: y = a·fn(b(x − p)) + q, fn = sin | cos | tan
  - vline: x / hline: y (점선, 점근선·경계 표시용)
  - 공통 선택 키: from, to(그릴 x 범위), color
- coordinate_plane 문항도 config.curves를 넣으면 곡선 위에 점을 찍게 할 수 있음
