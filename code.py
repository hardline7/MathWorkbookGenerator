from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import random
import os
import logging
import sys
from tqdm import tqdm
from itertools import groupby

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('math_workbook_debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

stamp_messages = [
    "🔢 숫자의 달인",
    "➕ 덧셈 천재",
    "➖ 뺄셈 달인",
    "🎯 수학 왕",
    "🌟 수학 영웅",
    "💫 연산의 달인",
    "🎨 수학 예술가",
    "🎮 수학 게이머",
    "📚 수학 박사",
    "🎭 수학 천재"
]

quiz_questions = [
    "🌈 오늘의 수학 미션: 주변에서 동그란 물건 3가지를 찾아보세요!",
    "🐰 토끼가 당근 3개를 가지고 있었어요. 2개를 더 받았다면 몇 개일까요?",
    "🎨 1부터 10까지 숫자 중 가장 예쁘게 쓸 수 있는 숫자는 무엇인가요?",
    "🌟 스스로에게 '참 잘했어요!' 별점을 매겨보세요! ☆☆☆☆☆",
    "🎵 숫자로 박수를 쳐봐요! 선생님이 부르는 숫자만큼 박수를 쳐보세요~",
    "🐸 개구리가 연못에서 2마리씩 짝지어 놀아요. 개구리 8마리는 몇 쌍일까요?",
    "🎪 서커스에 온 관람객이 50명이에요. 10명씩 묶으면 몇 그룹이 될까요?",
    "🍎 사과 바구니에 사과가 7개 있어요. 3개를 먹었다면 몇 개가 남을까요?",
    "🌸 꽃잎이 5장인 꽃이 3송이 있어요. 꽃잎은 모두 몇 장일까요?",
    "🎭 거울을 보며 가장 행복한 표정을 지어보세요! 기분이 좋아지나요?",
    "🚗 자동차가 5대 있는데 2대가 더 왔어요. 몇 대가 되었나요?",
    "🎈 풍선이 있어요. 빨간색 3개, 파란색 4개면 몇 개일까요?",
    "🐱 고양이가 낮잠을 자는데 3시간을 잤어요. 지금 4시라면 몇 시에 잠들었나요?",
    "📏 연필 6자루를 친구 2명에게 나누어 주려면 한 명당 몇 자루씩 받나요?",
    "🦁 동물원에 사자가 4마리 있어요. 2마리가 자고 있다면 깨어있는 사자는 몇 마리인가요?",
    "🎪 줄타기를 하는 곡예사가 10걸음 앞으로 가고 3걸음 뒤로 갔어요. 몇 걸음 갔을까요?",
    "🌳 나무에 새가 5마리 앉아있었는데 3마리가 날아갔어요. 몇 마리가 남았나요?",
    "🍦 아이스크림이 한 개에 2천원이에요. 5천원으로 몇 개를 살 수 있나요?",
    "🎭 연극 관람객이 20명 있었는데 5명이 떠났어요. 몇 명이 남았나요?",
    "🎨 크레파스 8개를 가진 민수와 크레파스 6개를 가진 영희, 누구의 크레파스가 더 많나요?",
    "🎲 주사위를 던져서 나올 수 있는 가장 큰 수는 무엇인가요?",
    "📚 책장에 책이 한 줄에 5권씩 들어가요. 15권을 꽂으려면 몇 줄이 필요한가요?",
    "🌈 무지개의 색은 몇 가지인가요? 하나씩 세어보세요!",
    "🐢 거북이 3마리가 달리기를 했어요. 1등은 몇 등인가요?",
    "🎪 서커스단의 코끼리가 하루에 바나나 6개씩 먹어요. 이틀 동안 먹는 바나나는 몇 개일까요?",
    "🎨 그림을 그리는데 빨간색 크레파스를 3번, 파란색을 2번 썼어요. 총 몇 번 썼나요?",
    "🐝 꿀벌이 꽃을 5송이 찾았어요. 다음 날 3송이를 더 찾았대요. 총 몇 송이를 찾았나요?",
    "🎭 인형극에 토끼가 4마리 나왔어요. 늑대는 토끼보다 2마리 적대요. 늑대는 몇 마리일까요?",
    "🌟 밤하늘에 별이 10개 있었는데 구름에 가려져서 4개가 안 보여요. 보이는 별은 몇 개인가요?",
    "🎪 저글링을 하는데 공 7개 중에서 2개를 떨어뜨렸어요. 몇 개로 저글링을 하고 있나요?",
    "🚂 기차에 객차가 8칸 있었는데 2칸을 떼어냈어요. 몇 칸이 남았나요?",
    "🎨 도화지 10장이 있는데 3장을 그렸어요. 몇 장이 남았나요?",
    "🐟 어항에 물고기가 6마리 있었는데 2마리를 더 넣었어요. 몇 마리가 되었나요?",
    "🎭 마술사가 모자에서 토끼를 3마리 꺼냈어요. 비둘기는 토끼보다 2마리 더 많이 꺼냈대요. 비둘기는 몇 마리인가요?",
    "🌺 화분에 꽃이 4송이 피어있었는데 2송이가 더 폈어요. 몇 송이가 되었나요?",
    "🎪 광대가 풍선을 7개 불었는데 2개가 터졌어요. 몇 개가 남았나요?",
    "🐘 코끼리가 땅콩을 한 번에 3개씩 먹어요. 9개를 먹으려면 몇 번 먹어야 할까요?",
    "🎨 크레파스 5개를 친구 한 명에게 주었더니 2개가 남았어요. 처음에 몇 개가 있었나요?",
    "🌈 색종이가 8장 있었는데 3장으로 학종이를 접었어요. 몇 장이 남았나요?",
    "🎭 인형극에서 병아리가 3마리 나왔어요. 오리는 병아리의 2배가 나왔대요. 오리는 몇 마리일까요?",
    "🎪 줄타기를 하는 곡예사가 줄 위에서 앞으로 4걸음 가다가 뒤로 1걸음 갔어요. 몇 걸음 간 걸까요?",
    "🐳 수족관에 돌고래가 5마리 있었는데 2마리가 쇼하러 갔어요. 몇 마리가 남았나요?",
    "🎨 스티커가 10장 있었는데 친구에게 4장을 주었어요. 몇 장이 남았나요?",
    "🦁 사자가 하루에 고기 2개씩 먹어요. 3일 동안 먹는 고기는 몇 개일까요?",
    "🎭 무대에 풍선이 9개 있었는데 3개가 떴어요. 몇 개가 남았나요?",
    "🌸 꽃밭에 장미가 6송이 있었는데 2송이를 꺾었어요. 몇 송이가 남았나요?",
    "🎪 서커스단의 원숭이가 바나나를 4개 가지고 있었는데 2개를 더 받았어요. 몇 개가 되었나요?",
    "🎨 그림을 그리는데 빨간색을 5번, 노란색을 3번 썼어요. 총 몇 번 크레파스를 사용했나요?",
    "🐠 어항에 금붕어가 7마리 있었는데 3마리를 다른 어항으로 옮겼어요. 몇 마리가 남았나요?",
    "🎭 마술사가 상자에서 비둘기 4마리를 꺼냈어요. 토끼는 비둘기보다 1마리 더 많이 꺼냈대요. 토끼는 몇 마리인가요?",
    "🌺 화분에 씨앗을 6개 심었는데 4개만 싹이 났어요. 싹이 나지 않은 씨앗은 몇 개인가요?",
    "🎪 광대가 공 8개로 저글링을 하다가 3개를 친구에게 주었어요. 몇 개로 저글링을 하게 되었나요?",
    "🦒 기린이 나뭇잎을 한 입에 2장씩 먹어요. 10장을 먹으려면 몇 번 먹어야 할까요?",
    "🎨 물감을 섞어보아요. 빨강 2방울과 파랑 3방울을 섞으면 총 몇 방울인가요?",
    "🌈 풍선이 하늘로 날아갔어요. 처음에 10개가 있었는데 3개가 날아갔어요. 몇 개가 남았나요?",
    "🎭 무대에 작은 공 5개, 큰 공 3개가 있어요. 공은 모두 몇 개인가요?",
    "🦋 나비가 꽃을 3송이 보고 날아갔다가 2송이를 더 보았어요. 총 몇 송이를 보았나요?",
    "🎪 저글링을 할 때 공 6개 중 빨간 공이 2개에요. 나머지 공은 몇 개일까요?",
    "🐼 팬더가 대나무를 4개 가지고 있었는데 3개를 먹었어요. 몇 개가 남았나요?",
    "🎨 크레파스를 9개 가지고 있는데 친구가 2개를 빌려갔어요. 몇 개가 남았나요?",
    "🌺 꽃밭에 튤립이 5송이 피어있었는데 2송이가 시들었어요. 몇 송이가 남았나요?"
]

pdf_path = "초등학교1학년_수학문제집.pdf"
font_path = "NanumGothic.ttf"
emoji_font_path = "NotoEmoji.ttf"

font_name = "NanumGothic"
emoji_font_name = "NotoEmoji"

def is_emoji(c):
    return c in "🔢➕➖🎯🌟💫🎨🎮📚🎭🐰🎵🐸🎪🍎🌸"

def draw_text(c, text, x, y, font_name, font_size, center=True):
    c.saveState()
    try:
        groups = groupby(text, key=is_emoji)
        current_x = x
        if center:
            total_width = 0
            for is_emoji_group, group in groupby(text, key=is_emoji):
                group_text = ''.join(group)
                if is_emoji_group:
                    c.setFont(emoji_font_name, font_size)
                else:
                    c.setFont(font_name, font_size)
                total_width += c.stringWidth(group_text)
            current_x = x - (total_width / 2)
        
        for is_emoji_group, group in groupby(text, key=is_emoji):
            group_text = ''.join(group)
            if is_emoji_group:
                c.setFont(emoji_font_name, font_size)
            else:
                c.setFont(font_name, font_size)
            width = c.stringWidth(group_text)
            c.drawString(current_x, y, group_text)
            current_x += width
    finally:
        c.restoreState()
def setup_fonts():
    try:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        pdfmetrics.registerFont(TTFont(emoji_font_name, emoji_font_path))
        
        if font_name not in pdfmetrics.getRegisteredFontNames():
            raise Exception(f"{font_name} 폰트 등록 실패")
        if emoji_font_name not in pdfmetrics.getRegisteredFontNames():
            raise Exception(f"{emoji_font_name} 폰트 등록 실패")
            
        logger.info("폰트가 성공적으로 로드되었습니다.")
        return True
    except Exception as e:
        logger.error(f"폰트 로드 실패: {e}")
        return False

def wrap_text(c, text, max_width, font_name, font_size):
    """텍스트를 주어진 너비에 맞게 여러 줄로 나누는 함수"""
    words = text.split()
    lines = []
    current_line = []
    
    c.setFont(font_name, font_size)
    
    for word in words:
        # 현재 줄에 단어를 추가했을 때의 너비 계산
        test_line = ' '.join(current_line + [word])
        width = c.stringWidth(test_line)
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # 단어 하나가 너무 길 경우, 강제로 자름
                lines.append(word)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def draw_quiz_box(c, width, y_position, quiz):
    """퀴즈 박스를 그리는 함수"""
    box_margin = 70
    box_width = width - (box_margin * 2)
    text_margin = 30
    font_size = 14
    line_height = 25  # 줄 간격 조정
    
    # 텍스트를 여러 줄로 나누기
    max_text_width = box_width - (text_margin * 2)
    text_lines = wrap_text(c, quiz, max_text_width, font_name, font_size)
    
    # 박스 높이 계산
    min_box_height = 100
    text_height = len(text_lines) * line_height
    box_height = max(min_box_height, text_height + (text_margin * 2))
    box_y = y_position - box_height
    
    # 박스 그리기
    c.setFillColorRGB(0.85, 0.85, 1)
    c.roundRect(box_margin, box_y, box_width, box_height, 10, fill=1)
    
    c.setStrokeColorRGB(0.6, 0.6, 1)
    c.setLineWidth(2)
    c.roundRect(box_margin, box_y, box_width, box_height, 10, fill=0, stroke=1)
    
    # 텍스트 그리기
    c.setFillColorRGB(0, 0, 0)
    text_y = box_y + box_height - text_margin
    
    for line in text_lines:
        draw_text(c, line, width/2, text_y, font_name, font_size)
        text_y -= line_height
    
    return box_y

def draw_coupon(c, x, y, width, height, title, message, is_final=False):
    """쿠폰 그리기 함수"""
    # 쿠폰 배경
    c.setFillColorRGB(1, 0.9, 0.9)  # 연한 핑크
    if is_final:
        c.setFillColorRGB(1, 0.85, 0.85)  # 최종 쿠폰은 조금 더 진한 핑크
    
    # 점선 패턴으로 오릴 수 있는 느낌 주기
    c.setDash([3, 3])
    c.setStrokeColorRGB(0.8, 0.2, 0.6)  # 진한 핑크
    c.setLineWidth(1.5)
    
    # 쿠폰 그리기
    c.roundRect(x, y, width, height, 10, fill=1, stroke=1)
    c.setDash([])  # 점선 패턴 해제
    
    # 쿠폰 내용
    c.setFillColorRGB(0.6, 0.2, 0.4)  # 진한 핑크퍼플
    c.setFont(font_name, 12)
    draw_text(c, title, x + width/2, y + height - 15, font_name, 12)
    draw_text(c, message, x + width/2, y + height/2, font_name, 10)
    
    # 가위 이모지 추가
    draw_text(c, "✂️", x + 10, y + height/2, emoji_font_name, 10)
    draw_text(c, "✂️", x + width - 10, y + height/2, emoji_font_name, 10)

def draw_coupon(c, x, y, width, height, number):
    """쿠폰 그리기 함수"""
    # 쿠폰 배경 (파스텔톤의 분홍색)
    c.setFillColorRGB(1, 0.9, 0.95)
    
    # 점선 패턴으로 오릴 수 있는 느낌 주기
    c.setDash([3, 3])
    c.setStrokeColorRGB(0.8, 0.4, 0.6)
    c.setLineWidth(1)
    
    # 쿠폰 그리기
    c.roundRect(x, y, width, height, 8, fill=1, stroke=1)
    c.setDash([])  # 점선 패턴 해제
    
    # 쿠폰 내용
    c.setFillColorRGB(0.6, 0.2, 0.4)
    messages = {
        10: "🎀 10개 도장 달성! 🎀\n엄마에게 작은 선물을\n요청할 수 있어요!",
        20: "🎁 20개 도장 달성! 🎁\n엄마에게 귀여운 선물을\n요청할 수 있어요!",
        30: "🌟 30개 도장 달성! 🌟\n엄마에게 예쁜 선물을\n요청할 수 있어요!",
        40: "💝 40개 도장 달성! 💝\n엄마에게 특별한 선물을\n요청할 수 있어요!",
        50: "✨ 50개 도장 달성! ✨\n엄마에게 멋진 선물을\n요청할 수 있어요!",
        60: "👑 축하합니다! 60개 완성! 👑\n아빠에게 원하는 선물을\n요청할 수 있어요!"
    }
    
    message = messages[number]
    lines = message.split('\n')
    
    # 여러 줄 텍스트 그리기
    line_height = 15
    start_y = y + height - 20
    for line in lines:
        draw_text(c, line, x + width/2, start_y, font_name, 11)
        start_y -= line_height
    
    # 가위 이모지 추가
    draw_text(c, "✂️", x + 10, y + 5, emoji_font_name, 10)
    draw_text(c, "✂️", x + width - 10, y + 5, emoji_font_name, 10)

def draw_coupon(c, x, y, width, height, number):
    """쿠폰 그리기 함수"""
    # 쿠폰 배경
    c.setFillColorRGB(1, 0.92, 0.95)  # 더 연한 파스텔 핑크
    
    # 점선 패턴
    c.setDash([4, 3])  # 점선 패턴 조정
    c.setStrokeColorRGB(0.85, 0.5, 0.7)  # 테두리 색상 조정
    c.setLineWidth(0.8)  # 선 두께 조정
    
    # 쿠폰 그리기
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)
    c.setDash([])
    
    # 쿠폰 내용
    c.setFillColorRGB(0.7, 0.3, 0.5)  # 텍스트 색상 조정
    
    messages = {
        10: "🎀 10개 도장 달성!\n작은 선물을 요청해보세요",
        20: "🎁 20개 도장 달성!\n귀여운 선물을 요청해보세요",
        30: "🌟 30개 도장 달성!\n예쁜 선물을 요청해보세요",
        40: "💝 40개 도장 달성!\n특별한 선물을 요청해보세요",
        50: "✨ 50개 도장 달성!\n멋진 선물을 요청해보세요",
        60: "👑 축하해요! 60개 완성!\n원하는 선물을 요청하세요"
    }
    
    message = messages[number]
    lines = message.split('\n')
    
    # 텍스트 그리기
    line_height = 13  # 줄간격 조정
    start_y = y + height - 15
    for line in lines:
        draw_text(c, line, x + width/2, start_y, font_name, 10)  # 폰트 크기 조정
        start_y -= line_height
    
    # 가위 이모지 - 왼쪽과 오른쪽에 배치
    c.setFillColorRGB(0.6, 0.3, 0.5)
    draw_text(c, "✂️", x - 8, y + height/2, emoji_font_name, 9)  # 왼쪽
    draw_text(c, "✂️", x + width + 8, y + height/2, emoji_font_name, 9)  # 오른쪽

def draw_stamp_collection(c, width, height):
    """도장 수집판 페이지 생성"""
    # 제목
    c.setFillColorRGB(0.8, 0.3, 0.5)
    draw_text(c, "✨ 나의 수학 도장 수집판 ✨", width/2, height - 45, font_name, 26)
    
    # 설명
    c.setFillColorRGB(0.7, 0.4, 0.6)
    draw_text(c, "열심히 공부하고 도장을 모아서 선물 쿠폰을 받아보세요!", width/2, height - 75, font_name, 13)

    # 도장판 영역 계산
    stamp_board_width = width * 0.65
    stamp_board_start_x = 40
    stamp_board_start_y = height - 120
    
    # 도장 설정
    stamps_per_row = 5
    stamp_size = 33
    h_spacing = 12
    v_spacing = 12
    block_spacing = 35
    
    # 쿠폰 설정
    coupon_width = width * 0.25
    coupon_height = 60
    coupon_start_x = stamp_board_start_x + stamp_board_width - 70
    
    # 각 블록 그리기
    for block in range(6):
        block_y = stamp_board_start_y - (block * (2 * stamp_size + v_spacing + block_spacing))
        
        # 도장 그리기
        for row in range(2):
            for col in range(stamps_per_row):
                stamp_x = stamp_board_start_x + col * (stamp_size + h_spacing)
                stamp_y = block_y - row * (stamp_size + v_spacing)
                
                # 도장 칸 디자인
                c.setFillColorRGB(0.98, 0.93, 0.98)
                c.setStrokeColorRGB(0.85, 0.7, 0.85)
                c.setLineWidth(0.8)
                
                c.roundRect(stamp_x, stamp_y, stamp_size, stamp_size, 5, fill=1)
                c.roundRect(stamp_x, stamp_y, stamp_size, stamp_size, 5, fill=0)
                
                # 번호
                stamp_num = (block * 10) + (row * 5) + col + 1
                if stamp_num <= 60:
                    c.setFillColorRGB(0.6, 0.4, 0.6)
                    draw_text(c, f"{stamp_num}", stamp_x + stamp_size/2, 
                            stamp_y + stamp_size/2, font_name, 11)
        
        # 쿠폰 그리기 - 세로 위치 20픽셀 아래로 조정
        coupon_y = block_y - stamp_size/2 - 20  # -20 추가
        draw_coupon(c, coupon_start_x, coupon_y, coupon_width, coupon_height, (block + 1) * 10)
    
    # 하단 메시지
    c.setFillColorRGB(0.7, 0.3, 0.5)
    draw_text(c, "도장을 모두 모으면 아빠에게 멋진 선물을 요청할 수 있어요! 💝", 
             width/2, 30, font_name, 13)
    
    
    
    
    

def add_stamp_reminder(c, width, y_position):
    c.setFillColorRGB(0.3, 0.3, 0.3)
    draw_text(c, "💫 문제를 다 풀었다면 도장 수집판에 도장을 찍어보세요! 💫", width/2, y_position, font_name, 12)

def generate_addition_problems(min_a, max_a, min_b, max_b, count):
    problems = []
    for _ in tqdm(range(count), desc=f"덧셈 문제 생성 중 ({min_a}-{max_a}) + ({min_b}-{max_b})"):
        a = random.randint(min_a, max_a)
        b = random.randint(min_b, max_b)
        problems.append(f"{a} + {b} = ")
    return problems

def generate_subtraction_problems(min_a, max_a, min_b, max_b, count):
    problems = []
    attempts = 0
    max_attempts = count * 2

    with tqdm(total=count, desc=f"뺄셈 문제 생성 중 ({min_a}-{max_a}) - ({min_b}-{max_b})") as pbar:
        while len(problems) < count and attempts < max_attempts:
            if min_b > max_a:
                a = random.randint(min_b, max_b)
                b = random.randint(min_a, max_a)
            else:
                a = random.randint(min_a, max_a)
                b = random.randint(min_b, max_b)
                if b > a:
                    a, b = b, a
            problems.append(f"{a} - {b} = ")
            pbar.update(1)
            attempts += 1
            
    return problems[:count]



def create_math_workbook():
    try:
        if not setup_fonts():
            logger.error("폰트 설정 실패로 PDF 생성을 중단합니다.")
            return False

        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        # 도장 수집판 페이지 생성
        draw_stamp_collection(c, width, height)
        c.showPage()

        current_page = 1  # 페이지 번호

        logger.info("PDF 생성을 시작합니다...")

        # 10번 반복하며 문제 생성
        for repeat in range(10):
            for category_index, (category, problem_generator) in enumerate([
                ("한자리 수 + 한자리 수 덧셈", lambda: generate_addition_problems(1, 9, 1, 9, 10)),
                ("한자리 수 + 두자리 수 덧셈", lambda: generate_addition_problems(1, 9, 10, 20, 10)),
                ("두자리 수 + 두자리 수 덧셈", lambda: generate_addition_problems(10, 20, 10, 20, 10)),
                ("한자리 수 - 한자리 수 뺄셈", lambda: generate_subtraction_problems(1, 9, 1, 9, 10)),
                ("두자리 수 - 한자리 수 뺄셈", lambda: generate_subtraction_problems(10, 99, 1, 9, 10)),
                ("두자리 수 - 두자리 수 뺄셈", lambda: generate_subtraction_problems(10, 99, 10, 99, 10))
            ]):
                problems = problem_generator()  # 매 반복마다 새로운 문제 생성

                logger.info(f"페이지 {current_page} 작성 중...")

                # 제목
                c.setFillColorRGB(0, 0, 0)
                draw_text(c, f"📖 {category}", width/2, height - 80, font_name, 20)

                # 문제 배치
                y_position = height - 150
                for i, problem in enumerate(problems):
                    problem_text = f"{i + 1}. {problem}"
                    draw_text(c, problem_text, 50, y_position, font_name, 16, center=False)
                    y_position -= 50

                # 쉬어가는 퀴즈 추가
                if y_position > 150:
                    y_position -= 30
                    quiz = random.choice(quiz_questions)
                    y_position = draw_quiz_box(c, width, y_position, quiz)

                # 도장 찍기 알림 추가
                add_stamp_reminder(c, width, 40)

                # 페이지 번호
                c.setFillColorRGB(0.3, 0.3, 0.3)
                draw_text(c, f"{current_page}/60", width - 50, 30, font_name, 12)

                c.showPage()
                current_page += 1  # 페이지 번호 증가

            logger.info(f"반복 {repeat + 1}/10 완료")

        c.save()
        logger.info(f"PDF 생성이 완료되었습니다! 파일 위치: {os.path.abspath(pdf_path)}")
        return True

    except Exception as e:
        logger.error(f"PDF 생성 중 오류 발생: {e}", exc_info=True)
        return False




if __name__ == "__main__":
    print("수학 문제집 생성을 시작합니다...")
    if create_math_workbook():
        print("✅ 문제집 생성이 완료되었습니다!")
        print("📖 첫 페이지에 도장 수집판이 있으니 확인해보세요!")
    else:
        print("❌ 문제집 생성 중 오류가 발생했습니다. 로그 파일을 확인해주세요.")
