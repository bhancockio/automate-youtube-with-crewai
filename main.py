from crewai import Crew, Process

from agents import YoutubeAutomationAgents
from tasks import YoutubeAutomationTasks
from langchain_openai import ChatOpenAI
from tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from tools.youtube_video_search_tool import YoutubeVideoSearchTool

from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4"
)

agents = YoutubeAutomationAgents()
tasks = YoutubeAutomationTasks()

youtube_video_search_tool = YoutubeVideoSearchTool()
youtube_video_details_tool = YoutubeVideoDetailsTool()

youtube_manager = agents.youtube_manager()
research_manager = agents.research_manager(
    youtube_video_search_tool, youtube_video_details_tool)
title_creator = agents.title_creator()
description_creator = agents.description_creator()
email_creator = agents.email_creator()

# TODO: UPDATE THE VIDEO DETAILS - The purpose of this video is to talk about how I've automated my YouTube video creation process using CrewAI, cover new CrewAI features, and how to build custom CrewAI tools

video_topic = "Automating Tasks Using CrewAI"
video_details = """
In this video, we're diving into the innovative ways I'm using CrewAI to 
automate my YouTube channel. From conducting thorough research to 
streamline video preparation, CrewAI is revolutionizing how I create content. 
But that's not all - I'm also exploring how to harness the power of CrewAI 
to generate personalized emails for my subscribers. Join me on this journey 
as I unlock the potential of AI to enhance my YouTube channel and connect 
with my audience like never before.
"""

manage_youtube_video_creation = tasks.manage_youtube_video_creation(
    agent=youtube_manager,
    video_topic=video_topic,
    video_details=video_details
)
manage_youtube_video_research = tasks.manage_youtube_video_research(
    agent=research_manager,
    video_topic=video_topic,
    video_details=video_details,
)
create_youtube_video_title = tasks.create_youtube_video_title(
    agent=title_creator,
    video_topic=video_topic,
    video_details=video_details
)
create_youtube_video_description = tasks.create_youtube_video_description(
    agent=description_creator,
    video_topic=video_topic,
    video_details=video_details
)
create_email_announcement_for_new_video = tasks.create_email_announcement_for_new_video(
    agent=email_creator,
    video_topic=video_topic,
    video_details=video_details
)


# Create a new Crew instance
crew = Crew(
    agents=[youtube_manager,
            research_manager,
            email_creator,
            ],
    tasks=[manage_youtube_video_creation,
           manage_youtube_video_research,
           create_email_announcement_for_new_video],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4
)

# Kick of the crew
results = crew.kickoff()

print("Crew work results:")
print(results)
