from functools import partial
from crewai import Task
from textwrap import dedent


class YoutubeAutomationTasks():

    def manage_youtube_video_creation(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Oversee the YouTube prepration process including market research, title ideation, 
                and description creation reqired to make a YouTube video. The ultimate goal is for you to generate 
                a report including a research table, potential high click-through-rate titles, 
                and a YouTube video description.
                               
                The video topic is: {video_topic}
                The video details are: {video_details}

            Example Output:
                                   
            # YouTube Competition Research Table:
            - Video 1:
                - Title: "How to Make a YouTube Video"
                - View Count: 100,000
                - Days Since Published: 30
                - Channel Subscriber Count: 1,000
                - Video URL: https://www.youtube.com/watch?v=1234
            - Video 2:
                - Title: "How to Make a YouTube Video"
                - View Count: 100,000
                - Days Since Published: 30
                - Channel Subscriber Count: 1,000
                - Video URL: https://www.youtube.com/watch?v=1234

            [THE REST OF THE YOUTUBE COMPETITION RESEARCH GOES HERE]
                                   
            - Video 15:
                - Title: "How to Make a YouTube Video"
                - View Count: 100,000
                - Days Since Published: 30
                - Channel Subscriber Count: 1,000
                - Video URL: https://www.youtube.com/watch?v=1234                
                                   
            # Potential High CTRO Titles:
            - How to Make a YouTube Video
            - How to Make a YouTube Video in 2021
            - How to Make a YouTube Video for Beginners
            [THE REST OF THE POTENTIAL HIGH CTRO TITLES GO HERE]
                                   
            # YouTube Video Description:
            🤖 Download the CrewAI Source Code Here:
            https://brandonhancock.io/crewai-updated-tutorial-hierarchical 

            Don't forget to Like and Subscribe if you're a fan of free source code 😉

            Ready to lead an AI revolution? Watch and learn how to build your own CrewAI from the ground up using the latest CrewAI features, and get set to deploy an army of AI agents at your command. This video is your ultimate guide to creating a powerful digital workforce, enhancing your projects with intelligent automation and streamlined workflows. Discover the secrets to customizing AI agents, setting them on tasks, and managing a smooth operation with CrewAI. It’s time to amplify your tech capabilities, and after this tutorial, you'll be equipped to engineer an AI crew that transforms any complex challenge into a simple task. Start your journey to AI mastery with CrewAI today!

            📰 Stay updated with my latest projects and insights:
            LinkedIn: https://www.linkedin.com/in/brandon-hancock-ai/
            Twitter: https://twitter.com/bhancock_ai

            Resources:
            - https://github.com/joaomdmoura/crewAI-examples/
            - https://www.crewai.io/
            - https://twitter.com/joaomdmoura/status/1756428892045496608
            - https://serper.dev/
                """),
            agent=agent,
            output_file="output/YouTube_Video_Creation_Report"
        )

    def manage_youtube_video_research(self, agent, context, video_topic, video_details):
        return Task(
            description=dedent(f"""For a given video topic and description, search youtube videos to find 
                15 high-performing YouTube videos on the same topic. Once you have found the videos, 
                delegate out research tasks to other agents to help you finish populate the missing fields in the 
                research CSV. When delegating tasks to other agents, make sure you include the 
                URL of the video that you need them to research.
                            
                This research CSV which will be used by other agents to help them generate titles 
                and other aspects of the new YouTube video that we are planning to create.
                               
                Research CSV Outline:
                - Title of the video
                - View count
                - Days since published
                - Channel subscriber count
                - Video URL
                       
                The video topic is: {video_topic}
                The video details is: {video_details}

                Important Notes: 
                - Make sure the CSV uses ; as the delimiter
                - Make sure the final Research CSV Outline doesn't contain duplicate videos
                - It is SUPER IMPORTANT that you only populate the research CSV with real YouTube videos 
                    and YouTube URLs that actually link to the YouTube Video.
                """),
            agent=agent,
            context=context,
            expected_output=dedent(f"""
                Video Title; View Count; Days Since Published; Channel Subscriber Count; Video URL
                How to Make a YouTube Video; 100,000; 30; 1,000; https://www.youtube.com/watch?v=1234;
                How to Get Your First 1000 Subscribers; 100,000; 30; 1,000; https://www.youtube.com/watch?v=1234;
                       ...              
                """)
        )

    def research_youtube_video(self, agent):
        return Task(
            description=dedent(f"""Based on a given YouTube Video URL research and return the following 
                information in a bulleted list: title of the video, view count, days since published, 
                channel subscriber count, and video url.
                """),
            agent=agent,
            expected_output=dedent(f"""
                - Title: "How to Make a YouTube Video"
                - View Count: 100,000
                - Days Since Published: 30
                - Channel Subscriber Count: 1,000
                - Video URL: https://www.youtube.com/watch?v=1234
                """),
            async_execution=True
        )

    def create_youtube_video_title(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Create 10 potential titles for a given YouTube video topic and description. 
                It is also very important to use researched videos to help you generate the titles.
                The titles should be less than 70 characters and should have a high click-through-rate.
                               
                Video Topic: {video_topic}
                Video Details: {video_details}
                """),
            agent=agent,
            expected_output=dedent(f"""
                - CrewAI Tutorial for Beginners: Learn How To Use Latest CrewAI Features
                - CrewAI Tutorial: Complete Crash Course for Beginners
                - How To Connect Local LLMs to CrewAI [Ollama, Llama2, Mistral]
                - How to Use CrewAI to Automate Your Workflow
                - CrewAI Tutorial: How to Build a Digital Workforce
                ...                
                """),
        )

    def create_youtube_video_description(self, agent, video_topic, video_details):
        return Task(
            description=dedent(f"""Create a description for a given YouTube video topic and description.     
                Video Topic: {video_topic}
                Video Details: {video_details}
                """),
            agent=agent,
            expected_output=dedent(f"""
                🤖 Download the CrewAI Source Code Here:
                https://brandonhancock.io/crewai-updated-tutorial-hierarchical 
                                   
                Don't forget to Like and Subscribe if you're a fan of free source code 😉
                                   
                Want to join a community of AI developers? Join the AI Developer Accelerator Skook Community for FREE:
                https://www.skool.com/ai-developers-9308

                Ready to lead an AI revolution? Watch and learn how to build your own CrewAI from the ground up using the latest CrewAI features, and get set to deploy an army of AI agents at your command. This video is your ultimate guide to creating a powerful digital workforce, enhancing your projects with intelligent automation and streamlined workflows. Discover the secrets to customizing AI agents, setting them on tasks, and managing a smooth operation with CrewAI. It’s time to amplify your tech capabilities, and after this tutorial, you'll be equipped to engineer an AI crew that transforms any complex challenge into a simple task. Start your journey to AI mastery with CrewAI today!

                📰 Stay updated with my latest projects and insights:
                LinkedIn: https://www.linkedin.com/in/brandon-hancock-ai/
                Twitter: https://twitter.com/bhancock_ai

                Resources:
                [LEAVE BLANK]
                                   
                Timestamps: 
                [LEAVE BLANK]
            """),
        )
