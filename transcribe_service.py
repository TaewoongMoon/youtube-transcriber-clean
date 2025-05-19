import openai
import os
import subprocess

# 최신 방식 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# YouTube 오디오 다운로드
def download_audio_from_youtube(url):
    output_pattern = "audio.%(ext)s"
    result = subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", output_pattern,
        url
    ], capture_output=True, text=True)

    print("📦 yt-dlp 출력:\n", result.stdout)
    if result.stderr:
        print("❗ 오류 로그:\n", result.stderr)

    for file in os.listdir():
        if file.endswith(".mp3"):
            print("✅ 다운로드된 파일:", file)
            return file

    raise FileNotFoundError("❌ mp3 파일이 생성되지 않았습니다.")

# 최신 방식 Whisper API 호출
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"[에러] 전사 실패: {e}")
        return None

# 전체 실행 파이프라인
def transcribe_youtube_video(youtube_url):
    try:
        audio_file = download_audio_from_youtube(youtube_url)
        result = transcribe_audio(audio_file)
        os.remove(audio_file)
        return result
    except Exception as e:
        print(f"[실패] 전체 처리 에러: {e}")
        return None

# 테스트
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=s75Ryr-qSJU&t=4s"
    text = transcribe_youtube_video(test_url)

    if text:
        print("\n📄 전사 결과:\n", text)
    else:
        print("\n❌ 자막 추출에 실패했습니다.")
