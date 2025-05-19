import requests
from sheets_service import get_existing_video_links

YOUTUBE_API_KEY = "AIzaSyCUPbCUqcgTS80p7Jqvby4Qjaoj8WltXLg"

def get_channel_id_from_handle(handle_url):
    handle_name = handle_url.replace("https://www.youtube.com/@", "")
    # fallback 방식으로 검색
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={handle_name}&type=channel&key={YOUTUBE_API_KEY}"
    response = requests.get(search_url)
    data = response.json()
    if "items" in data and data["items"]:
        return data["items"][0]["snippet"]["channelId"]
    raise Exception("채널 ID를 찾을 수 없습니다.")

def fetch_all_video_links(channel_url):
    channel_id = get_channel_id_from_handle(channel_url)
    video_links = []
    next_page_token = None

    existing_links = get_existing_video_links()

    while True:
        api_url = (
            f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}"
            f"&channelId={channel_id}&part=snippet,id&order=date&maxResults=50"
        )
        if next_page_token:
            api_url += f"&pageToken={next_page_token}"

        search_response = requests.get(api_url).json()

        for item in search_response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                # 👉 쇼츠 필터링을 위해 videoDetails 요청
                video_api_url = (
                    f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails"
                    f"&id={video_id}&key={YOUTUBE_API_KEY}"
                )
                video_detail = requests.get(video_api_url).json()
                items = video_detail.get("items", [])

                if not items:
                    continue

                duration_str = items[0]["contentDetails"]["duration"]
                seconds = iso8601_duration_to_seconds(duration_str)

                # 60초 이상 + 중복 아님 → 저장
                if seconds >= 60 and video_url not in existing_links:
                    video_links.append(video_url)

        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    return video_links

def iso8601_duration_to_seconds(duration):
    import isodate
    try:
        return int(isodate.parse_duration(duration).total_seconds())
    except Exception:
        return 0
