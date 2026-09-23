# math-arena 레슨 스키마 v1.0

경로: content/level{N}/{course}/{chapter}/l{NN}.json, 챕터 목록은 chapter.json

## 레슨 파일
- course / chapter / lesson: id, 번호, 제목 (lesson.minutes = 예상 소요 시간)
- tags.domain: 학문 분과 태그(대수·해석·기하위상·확률통계·이산조합), tags.region, tags.curriculum
- screens: 화면 배열. 순서대로 표시. stage = intro | discover | summary | apply

## 화면 유형
- explain: title, body(문단 배열), figure(선택, 정적 위젯: number_line, area_model)
  - area_model: config.rows / config.cols 에 변 이름 배열, 칸마다 행×열 넓이를 표시
- question: qtype별 필드
  - numeric: answer(문자열), answer_format(integer | fraction | decimal), tolerance
    - fraction은 동치 분수 허용 여부를 플레이어에서 결정(권장: 기약분수만 정답)
  - fill_blank: prompt 안 {{n}} 자리, blanks[n].answers(허용 답 목록), unordered_groups(순서 무관 빈칸 묶음)
    - 허용 답에는 마이너스(- / −)와 거듭제곱(² / ^2) 표기 변형이 미리 들어 있음
    - 플레이어는 비교 전 공백 제거 권장
  - ordering: items(표시 순서), answer_order(정답 id 순서)
  - diagram: widget(number_line), config(min, max, step), answer.value, answer.tolerance
  - written: rubric(visibility=hidden, keyword_groups, min_groups_matched), model_answer
    - 채점: 각 그룹 중 하나라도 포함되면 그룹 일치, 일치 그룹 수가 기준 이상이면 통과
    - rubric은 화면에 노출하지 않음
- 공통: hint(선택), explanation(정답 확인 후 표시)
