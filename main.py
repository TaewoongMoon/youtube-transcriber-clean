from transcribe_service import transcribe_youtube_video
from sheets_service import append_transcription_row
from transcribe_service import transcribe_youtube_video
from sheets_service import (
    append_transcription_row,
    get_pending_channels,
    mark_channel_done
)

# YouTube API 영상 링크 수집 함수
from youtube_service import fetch_all_video_links  # 이미 작성한 영상 수집 코드


# ✅ 자막 생성 → 시트 기록 함수
def process_and_save_to_sheet(channel_name, channel_link, video_url):
    transcript = transcribe_youtube_video(video_url)

    if transcript:
        append_transcription_row(channel_name, channel_link, video_url, transcript)
    else:
        print(f"[실패] {video_url} 자막 추출 실패")

def run_batch_transcription():
    pending_channels = get_pending_channels()

    if not pending_channels:
        print("처리할 채널이 없습니다.")
        return

    for item in pending_channels:
        print(f"\n 채널 처리 중: {item['channel_name']}")

        try:
            video_links = fetch_all_video_links(item["channel_link"])

            for video_url in video_links:
                transcript = transcribe_youtube_video(video_url)
                if transcript:
                    append_transcription_row(
                        item["channel_name"],
                        item["channel_link"],
                        video_url,
                        transcript
                    )

            mark_channel_done(item["row_number"])

        except Exception as e:
            print(f"채널 처리 실패: {e}")

# 실행
if __name__ == "__main__":
    run_batch_transcription()
