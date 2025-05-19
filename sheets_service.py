import gspread
from google.oauth2.service_account import Credentials

# 인증 설정
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# 시트 열기
SPREADSHEET_NAME = "메일링 자동화"  # 정확한 문서 이름 입력
sheet = client.open(SPREADSHEET_NAME)

channel_sheet = sheet.worksheet("채널목록")
result_sheet = sheet.worksheet("자막결과")

# 자막결과 시트에 한 줄 추가하는 함수
def append_transcription_row(channel_name, channel_link, video_link, transcript):
    result_sheet.append_row([channel_name, channel_link, video_link, transcript])
    print("✅ 자막결과 시트에 저장 완료")
    
# 채널 목록에서 'X'인 항목들 불러오기
def get_pending_channels():
    data = channel_sheet.get_all_values()[1:]  # 헤더 제외
    pending = []
    for i, row in enumerate(data, start=2):  # 시트는 1-indexed
        if len(row) >= 3 and row[2].strip().upper() == "X":
            pending.append({
                "row_number": i,
                "channel_name": row[0],
                "channel_link": row[1]
            })
    return pending

# '수집여부'를 O로 업데이트
def mark_channel_done(row_number):
    channel_sheet.update_cell(row_number, 3, "O")
    print(f"✅ 수집여부 업데이트 완료 (Row {row_number})")

# 이미 저장된 영상 링크 목록 가져오기 (중복 방지용)
def get_existing_video_links():
    data = result_sheet.get_all_values()[1:]  # 헤더 제외
    return set(row[2] for row in data if len(row) >= 3)

