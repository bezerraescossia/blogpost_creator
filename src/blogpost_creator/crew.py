from dotenv import load_dotenv

_ = load_dotenv()

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from typing import List

import agentops
#agentops.init()

serper = SerperDevTool()
scraper = ScrapeWebsiteTool()
file_write = FileWriterTool(directory='./artifacts/')


@CrewBase
class BlogpostCreator():
    """BlogpostCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['content_researcher'], # type: ignore[index]
            tools=[serper],
            verbose=True
        )

    @agent
    def content_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['content_planner'], # type: ignore[index]
            tools=[scraper],
            verbose=True
        )
    
    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_writer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def content_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_reviewer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def social_media_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_specialist'], # type: ignore[index]
            verbose=True
        )

    @task
    def content_research(self) -> Task:
        return Task(
            config=self.tasks_config['content_research'], # type: ignore[index]
        )
    
    @task
    def content_planning(self) -> Task:
        return Task(
            config=self.tasks_config['content_planning'], # type: ignore[index]
        )
    
    @task
    def blog_post_writing(self) -> Task:
        return Task(
            config=self.tasks_config['blog_post_writing'], # type: ignore[index]
        )
    
    @task
    def content_review(self) -> Task:
        return Task(
            config=self.tasks_config['content_review'], # type: ignore[index]
        )
    
    @task
    def save_content(self) -> Task:
        return Task(
            config=self.tasks_config['save_content'], # type: ignore[index]
            tools=[file_write]
        )
    
    @task
    def social_media_summary(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_summary'], # type: ignore[index]
        )
    
    @task
    def save_social_media_summary(self) -> Task:
        return Task(
            config=self.tasks_config['save_social_media_summary'], # type: ignore[index]
            tools=[file_write]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BlogpostCreator crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

if __name__ == '__main__':

    inputs = {
        'topic': 'Next Generation Sequencing Guide with Applications in Oncology for Medical Doctors',
        'media': 'LinkedIn'
    }

    blogpost_creator = BlogpostCreator().crew()
    results = blogpost_creator.kickoff(inputs=inputs)
    results