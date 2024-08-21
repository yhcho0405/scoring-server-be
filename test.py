import requests
import json
from tabulate import tabulate
from termcolor import colored

url = 'http://localhost:8000/api/similarity/score'

sentence_pairs = {
    "의미적_유사도가_높은_세트": [
        {"sentence1": "날씨가 좋습니다", "sentence2": "날이 맑습니다"},
        {"sentence1": "그녀는 피아노를 칩니다", "sentence2": "그녀는 악기를 연주합니다"},
        {"sentence1": "이 꽃은 빨간색입니다", "sentence2": "이 장미는 붉은색입니다"},
        {"sentence1": "나는 학교에 갑니다", "sentence2": "저는 등교합니다"},
        {"sentence1": "그는 의사입니다", "sentence2": "그는 의료인입니다"},
        {"sentence1": "이 가방은 무겁습니다", "sentence2": "이 짐은 묵직합니다"},
        {"sentence1": "버스가 늦게 왔어요", "sentence2": "버스가 지연되었습니다"},
        {"sentence1": "나는 한국어를 공부합니다", "sentence2": "저는 한국어를 배웁니다"},
        {"sentence1": "이 신발은 작습니다", "sentence2": "이 신발은 사이즈가 작네요"},
        {"sentence1": "점심을 먹었습니다", "sentence2": "점심 식사를 했습니다"},
        {"sentence1": "내일 친구를 만납니다", "sentence2": "내일 친구와 약속이 있습니다"},
        {"sentence1": "그는 축구를 잘 합니다", "sentence2": "그는 축구 실력이 뛰어납니다"},
        {"sentence1": "이 방은 춥습니다", "sentence2": "이 방의 온도가 낮습니다"},
        {"sentence1": "저는 커피를 마십니다", "sentence2": "나는 커피를 즐깁니다"},
        {"sentence1": "그 영화는 재미있었어요", "sentence2": "그 영화가 흥미로웠습니다"},
        {"sentence1": "행복", "sentence2": "기쁨"},
        {"sentence1": "슬픔", "sentence2": "우울"},
        {"sentence1": "큰", "sentence2": "거대한"},
        {"sentence1": "빠른", "sentence2": "신속한"},
        {"sentence1": "아름다운", "sentence2": "예쁜"},
        {"sentence1": "어려운", "sentence2": "힘든"},
        {"sentence1": "똑똑한", "sentence2": "영리한"},
        {"sentence1": "부드러운", "sentence2": "연한"},
        {"sentence1": "차가운", "sentence2": "서늘한"},
        {"sentence1": "깨끗한", "sentence2": "청결한"},
        {"sentence1": "새로운", "sentence2": "신선한"},
        {"sentence1": "강한", "sentence2": "튼튼한"},
        {"sentence1": "피곤한", "sentence2": "지친"},
        {"sentence1": "친절한", "sentence2": "상냥한"},
        {"sentence1": "조용한", "sentence2": "고요한"},
        {"sentence1": "차가운 얼음", "sentence2": "시원한 얼음"},
        {"sentence1": "빠른 치타", "sentence2": "신속한 표범"},
        {"sentence1": "착한 소녀", "sentence2": "선한 아이"},
        {"sentence1": "슬픈 이별", "sentence2": "우울한 작별"},
        {"sentence1": "무서운 유령", "sentence2": "두려운 망령"},
        {"sentence1": "달콤한 사탕", "sentence2": "달콤한 과자"},
        {"sentence1": "깨끗한 방", "sentence2": "청결한 실내"},
        {"sentence1": "똑똑한 학생", "sentence2": "영리한 학생"},
        {"sentence1": "조용한 도서관", "sentence2": "고요한 독서실"},
        {"sentence1": "따뜻한 햇살", "sentence2": "포근한 햇빛"},
        {"sentence1": "무거운 짐", "sentence2": "묵직한 짐"},
        {"sentence1": "향기로운 꽃", "sentence2": "향기로운 화초"},
        {"sentence1": "부드러운 털", "sentence2": "보드라운 모피"},
        {"sentence1": "어두운 밤", "sentence2": "캄캄한 저녁"},
        {"sentence1": "건조한 피부", "sentence2": "메마른 살결"},
        {"sentence1": "행복한 순간", "sentence2": "즐거운 시간"},
        {"sentence1": "차가운 얼음", "sentence2": "냉랭한 빙판"},
        {"sentence1": "젖은 우산", "sentence2": "축축한 양산"},
        {"sentence1": "투명한 유리", "sentence2": "맑은 유리"},
        {"sentence1": "단단한 바위", "sentence2": "견고한 암석"},
        {"sentence1": "달콤한 꿀", "sentence2": "달콤한 벌꿀"},
        {"sentence1": "조용한 아침", "sentence2": "고요한 새벽"},
        {"sentence1": "빠른 기차", "sentence2": "신속한 열차"},
        {"sentence1": "뜨거운 태양", "sentence2": "뜨거운 해"},
        {"sentence1": "큰 건물", "sentence2": "거대한 빌딩"},
        {"sentence1": "무거운 바위", "sentence2": "묵직한 돌"},
        {"sentence1": "건강한 신체", "sentence2": "튼튼한 몸"},
        {"sentence1": "부드러운 비단", "sentence2": "부드러운 실크"},
        {"sentence1": "깊은 바다", "sentence2": "심오한 대양"},
        {"sentence1": "똑바른 자세", "sentence2": "바른 자세"}
    ],
    "의미적_유사도가_없는_세트": [
        {"sentence1": "오늘 날씨가 좋습니다", "sentence2": "이 책은 재미있습니다"},
        {"sentence1": "저는 커피를 마십니다", "sentence2": "비행기가 하늘을 납니다"},
        {"sentence1": "그녀는 피아노를 칩니다", "sentence2": "내일 시험이 있습니다"},
        {"sentence1": "이 꽃은 빨간색입니다", "sentence2": "그는 운동을 좋아합니다"},
        {"sentence1": "바다에서 수영을 했어요", "sentence2": "이 컴퓨터는 새 것입니다"},
        {"sentence1": "우리 집은 3층입니다", "sentence2": "그 영화는 슬펐어요"},
        {"sentence1": "나는 학교에 갑니다", "sentence2": "이 음식은 매워요"},
        {"sentence1": "그는 의사입니다", "sentence2": "내 고양이는 털이 하얗습니다"},
        {"sentence1": "이 가방은 무겁습니다", "sentence2": "그녀는 노래를 잘 합니다"},
        {"sentence1": "버스가 늦게 왔어요", "sentence2": "이 그림은 아름답습니다"},
        {"sentence1": "나는 한국어를 공부합니다", "sentence2": "내일은 비가 올 거예요"},
        {"sentence1": "이 신발은 작습니다", "sentence2": "그 나무는 키가 큽니다"},
        {"sentence1": "점심을 먹었습니다", "sentence2": "그 차는 빨간색입니다"},
        {"sentence1": "내일 친구를 만납니다", "sentence2": "이 방은 춥습니다"},
        {"sentence1": "그는 축구를 잘 합니다", "sentence2": "이 꽃은 향기롭습니다"},
        {"sentence1": "사과", "sentence2": "컴퓨터"},
        {"sentence1": "바다", "sentence2": "연필"},
        {"sentence1": "책상", "sentence2": "구름"},
        {"sentence1": "자동차", "sentence2": "꽃"},
        {"sentence1": "신발", "sentence2": "달"},
        {"sentence1": "전화", "sentence2": "나무"},
        {"sentence1": "의자", "sentence2": "비행기"},
        {"sentence1": "모자", "sentence2": "물고기"},
        {"sentence1": "카메라", "sentence2": "소파"},
        {"sentence1": "칫솔", "sentence2": "태양"},
        {"sentence1": "컵", "sentence2": "기타"},
        {"sentence1": "시계", "sentence2": "새"},
        {"sentence1": "냉장고", "sentence2": "연필"},
        {"sentence1": "거울", "sentence2": "책"},
        {"sentence1": "창문", "sentence2": "바나나"},
        {"sentence1": "차가운 청년", "sentence2": "따뜻한 돌"},
        {"sentence1": "빠른 거북이", "sentence2": "무거운 바람"},
        {"sentence1": "착한 칼", "sentence2": "시끄러운 침묵"},
        {"sentence1": "슬픈 태양", "sentence2": "단단한 구름"},
        {"sentence1": "무서운 꽃", "sentence2": "부드러운 번개"},
        {"sentence1": "달콤한 돌", "sentence2": "짠 우유"},
        {"sentence1": "깨끗한 먼지", "sentence2": "더러운 비누"},
        {"sentence1": "똑똑한 의자", "sentence2": "어리석은 책"},
        {"sentence1": "조용한 천둥", "sentence2": "시끄러운 그림자"},
        {"sentence1": "차가운 불꽃", "sentence2": "뜨거운 얼음"},
        {"sentence1": "무거운 깃털", "sentence2": "가벼운 바위"},
        {"sentence1": "향기로운 소음", "sentence2": "악취 나는 향수"},
        {"sentence1": "부드러운 칼날", "sentence2": "날카로운 솜"},
        {"sentence1": "어두운 태양", "sentence2": "밝은 동굴"},
        {"sentence1": "건조한 바다", "sentence2": "습한 사막"},
        {"sentence1": "행복한 장례식", "sentence2": "슬픈 결혼식"},
        {"sentence1": "차가운 불", "sentence2": "뜨거운 눈"},
        {"sentence1": "젖은 모래", "sentence2": "마른 바다"},
        {"sentence1": "투명한 벽돌", "sentence2": "불투명한 유리"},
        {"sentence1": "단단한 물", "sentence2": "부드러운 돌"},
        {"sentence1": "달콤한 소금", "sentence2": "쓴 설탕"},
        {"sentence1": "조용한 폭포", "sentence2": "시끄러운 사막"},
        {"sentence1": "빠른 달팽이", "sentence2": "느린 치타"},
        {"sentence1": "뜨거운 얼음", "sentence2": "차가운 용암"},
        {"sentence1": "큰 원자", "sentence2": "작은 우주"},
        {"sentence1": "무거운 공기", "sentence2": "가벼운 납"},
        {"sentence1": "건강한 독", "sentence2": "유해한 약"},
        {"sentence1": "부드러운 바위", "sentence2": "거친 비단"},
        {"sentence1": "깊은 하늘", "sentence2": "얕은 우주"},
        {"sentence1": "똑바른 미로", "sentence2": "구불구불한 직선"}
    ]
}
def calculate_similarities(pairs):
    results = []
    for pair in pairs:
        response = requests.post(url, json=pair)
        if response.status_code == 200:
            similarity = response.json()['result']
            results.append([pair['sentence1'], pair['sentence2'], similarity])
        else:
            print(f"Error for pair {pair}: {response.text}")
    return results

def print_results(results, set_name):
    print(f"\n{set_name} 결과:")
    headers = ["순위", "Sentence 1", "Sentence 2", "Similarity"]
    ranked_results = [[i+1] + result for i, result in enumerate(sorted(results, key=lambda x: x[2], reverse=True))]
    print(tabulate(ranked_results, headers=headers, tablefmt="grid", floatfmt=".4f"))

    similarities = [r[2] for r in results]
    avg_similarity = sum(similarities) / len(similarities)
    max_similarity = max(similarities)
    min_similarity = min(similarities)

    print(f"\n{set_name} 통계:")
    print(f"평균 유사도: {avg_similarity:.4f}")
    print(f"최대 유사도: {max_similarity:.4f}")
    print(f"최소 유사도: {min_similarity:.4f}")

    return avg_similarity

high_similarity_results = calculate_similarities(sentence_pairs["의미적_유사도가_높은_세트"])
low_similarity_results = calculate_similarities(sentence_pairs["의미적_유사도가_없는_세트"])

high_avg = print_results(high_similarity_results, "의미적 유사도가 높은 세트")
low_avg = print_results(low_similarity_results, "의미적 유사도가 낮은 세트")

all_results = low_similarity_results + high_similarity_results
ranked_results = sorted(all_results, key=lambda x: x[2], reverse=True)

print("\n전체 순위:")
headers = ["Rank", "Sentence 1", "Sentence 2", "Similarity", "Set"]
ranked_data = []
for i, result in enumerate(ranked_results):
    set_name = "낮은 세트" if result in low_similarity_results else "높은 세트"
    color = "red" if set_name == "낮은 세트" else "green"
    ranked_data.append([
        i+1, 
        result[0], 
        result[1], 
        result[2],
        colored(set_name, color)
    ])

print(tabulate(ranked_data, headers=headers, tablefmt="grid", floatfmt=".4f"))

print(f"\n세트 간 평균 유사도 차이: {high_avg - low_avg:.4f}")