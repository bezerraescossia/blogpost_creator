from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BlogpostCreator():
    """BlogpostCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def idea_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['idea_developer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def content_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['content_planner'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def post_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['post_writer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def post_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['post_reviewer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def create_ideas(self) -> Task:
        return Task(
            config=self.tasks_config['create_ideas'], # type: ignore[index]
            output_file='artifacts/1_create_idea.md',
        )

    @task
    def select_idea(self) -> Task:
        return Task(
            config=self.tasks_config['select_idea'], # type: ignore[index]
            output_file='artifacts/2_select_idea.md',
        )
    
    @task
    def plan_content(self) -> Task:
        return Task(
            config=self.tasks_config['plan_content'], # type: ignore[index]
            output_file='artifacts/3_plan_content.md',
        )
    
    @task
    def write_post(self) -> Task:
        return Task(
            config=self.tasks_config['write_post'], # type: ignore[index]
            output_file='artifacts/4_write_post.md',
        )
    
    @task
    def review_post(self) -> Task:
        return Task(
            config=self.tasks_config['review_post'], # type: ignore[index]
            output_file='artifacts/5_review_post.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BlogpostCreator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
