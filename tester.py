from tools.youtube_tools import YoutubeTools
from dotenv import load_dotenv
load_dotenv()

youtube_tools = YoutubeTools()  # Create an instance of YoutubeTools

results = youtube_tools.search_youtube_videos("CrewAI", 10)

for result in results:
    print("-----------------------")
    print(result)
    video_details = youtube_tools.get_video_details(
        result.video_id)  # Call the method on the instance
    print("Video Details:")
    print(video_details)
