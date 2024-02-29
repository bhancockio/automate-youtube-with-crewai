import os
import requests
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
from langchain.tools import tool


class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int


class VideoDetails(BaseModel):
    title: str
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    channel_subscriber_count: int


class YoutubeTools:
    @tool("Search YouTube Videos")
    def search_youtube_videos(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        """
        Searches YouTube videos based on a keyword and returns a list of video search results.
        """
        api_key = os.getenv("YOUTUBE_API_KEY")
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "maxResults": max_results,
            "type": "video",
            "key": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        results = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel_id = item["snippet"]["channelId"]
            channel_title = item["snippet"]["channelTitle"]
            publish_date = datetime.fromisoformat(
                item["snippet"]["publishedAt"].replace('Z', '+00:00')).astimezone(timezone.utc)
            # Calculate the days since published
            days_since_published = (datetime.now(
                timezone.utc) - publish_date).days
            results.append(VideoSearchResult(
                video_id=video_id,
                title=title,
                channel_id=channel_id,
                channel_title=channel_title,
                days_since_published=days_since_published
            ))

        return results

    @tool("Get Video Details")
    def get_video_details(self, video_id: str) -> VideoDetails:
        """
        Retrieves details for a specific YouTube video.
        """
        api_key = os.getenv("YOUTUBE_API_KEY")
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        item = response.json().get("items", [])[0]

        title = item["snippet"]["title"]
        view_count = int(item["statistics"]["viewCount"])
        like_count = int(item["statistics"].get("likeCount", 0))
        dislike_count = int(item["statistics"].get("dislikeCount", 0))
        comment_count = int(item["statistics"].get("commentCount", 0))

        channel_id = item["snippet"]["channelId"]
        channel_url = "https://www.googleapis.com/youtube/v3/channels"
        channel_params = {
            "part": "statistics",
            "id": channel_id,
            "key": api_key
        }
        channel_response = requests.get(channel_url, params=channel_params)
        channel_response.raise_for_status()
        channel_item = channel_response.json().get("items", [])[0]
        channel_subscriber_count = int(
            channel_item["statistics"]["subscriberCount"])

        return VideoDetails(
            title=title,
            view_count=view_count,
            like_count=like_count,
            dislike_count=dislike_count,
            comment_count=comment_count,
            channel_subscriber_count=channel_subscriber_count
        )
