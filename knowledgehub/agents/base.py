from enum import Enum
from typing import Optional, Union

from theflow import Node, Param

from kotaemon.base import BaseComponent
from kotaemon.llms import PromptTemplate
from kotaemon.llms.chats.base import ChatLLM
from kotaemon.llms.completions.base import LLM

from .tools import BaseTool

BaseLLM = Union[ChatLLM, LLM]


class AgentType(Enum):
    """
    Enumerated type for agent types.
    """

    openai = "openai"
    openai_multi = "openai_multi"
    openai_tool = "openai_tool"
    self_ask = "self_ask"
    react = "react"
    rewoo = "rewoo"
    vanilla = "vanilla"

    @staticmethod
    def get_agent_class(_type: "AgentType"):
        """
        Get agent class from agent type.
        :param _type: agent type
        :return: agent class
        """
        if _type == AgentType.rewoo:
            from .rewoo.agent import RewooAgent

            return RewooAgent
        else:
            raise ValueError(f"Unknown agent type: {_type}")


class BaseAgent(BaseComponent):
    """Define base agent interface"""

    name: str = Param(help="Name of the agent.")
    agent_type: AgentType = Param(help="Agent type, must be one of AgentType")
    description: str = Param(
        help="Description used to tell the model how/when/why to use the agent. "
        "You can provide few-shot examples as a part of the description. This will be "
        "input to the prompt of LLM."
    )
    llm: Union[BaseLLM, dict[str, BaseLLM]] = Node(
        help="Specify LLM to be used in the model, cam be a dict to supply different "
        "LLMs to multiple purposes in the agent"
    )
    prompt_template: Optional[Union[PromptTemplate, dict[str, PromptTemplate]]] = Param(
        help="A prompt template or a dict to supply different prompt to the agent"
    )
    plugins: list[BaseTool] = Param(
        default_callback=lambda _: [],
        help="List of plugins / tools to be used in the agent",
    )

    def add_tools(self, tools: list[BaseTool]) -> None:
        """Helper method to add tools and update agent state if needed"""
        self.plugins.extend(tools)
