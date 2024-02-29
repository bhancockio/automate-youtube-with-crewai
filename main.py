from crewai import Crew, Process

from agents import YoutubeAutomationAgents
from tasks import YoutubeAutomationTasks
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4"
)

agents = YoutubeAutomationAgents()
tasks = YoutubeAutomationTasks()


youtube_manager = agents.youtube_manager()
research_manager = agents.research_manager()
youtube_researcher = agents.youtube_researcher()
title_creator = agents.title_creator()
description_creator = agents.description_creator()

video_topic = "Automating Tasks Using CrewAI"
video_details = """
In this comprehensive guide, we delve into the transformative world of CrewAI, 
where automation meets efficiency. Discover how to streamline your workflow 
by automating routine tasks with the power of AI. From setting up agents to 
orchestrating complex processes, we'll cover everything you need to know to 
make CrewAI work for you. Whether you're a seasoned developer or just getting 
started, this video will equip you with the tools and knowledge to supercharge 
your productivity with CrewAI automation.
"""

manage_youtube_video_creation = tasks.manage_youtube_video_creation(
    agent=youtube_manager,
    video_topic=video_topic,
    video_details=video_details
)
research_youtube_video = tasks.research_youtube_video(
    agent=youtube_researcher
)
manage_youtube_video_research = tasks.manage_youtube_video_research(
    agent=research_manager,
    video_topic=video_topic,
    video_details=video_details,
    context=[research_youtube_video]
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


# Create a new Crew instance
crew = Crew(
    agents=[youtube_manager, research_manager, youtube_researcher],
    tasks=[manage_youtube_video_creation,
           manage_youtube_video_research, research_youtube_video],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4
)

# Kick of the crew
results = crew.kickoff()

print("Crew work results:")
print(results)
