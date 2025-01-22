from typing import List, Optional, Dict, Any
from enum import IntEnum
from cozepy.model import CozeModel, NumberPaged, AsyncNumberPaged, NumberPagedResponse
from cozepy.auth import Auth
from cozepy.request import HTTPRequest, Requester
from cozepy.util import remove_url_trailing_slash


class SimpleBot(CozeModel):
    """The unique identifier of the agent."""

    bot_id: Optional[str]
    """The name of the agent."""
    bot_name: Optional[str]
    """Description of the intelligent agent."""
    description: Optional[str]
    """Avatar of the intelligent agent."""
    icon_url: Optional[str]
    """The most recent release time of the agent, formatted as a 10-digit Unixtime timestamp. The list of agents returned by this API is sorted in descending order by this field."""
    publish_time: Optional[str]


class _PrivateListBotsData(CozeModel, NumberPagedResponse[SimpleBot]):
    """List of agents published to the Agent as API channel in the specified space."""

    space_bots: List[SimpleBot]
    """Total number of agents in the agent list."""
    total: int

    def get_total(self) -> Optional[int]:
        return self.total

    def get_has_more(self) -> Optional[bool]:
        return None

    def get_items(self) -> List[SimpleBot]:
        return self.space_bots


class ResponseDetail(CozeModel):
    """The log ID for this request. If you encounter an error scenario and continue to receive errors after repeated attempts, you can contact the Coze team for assistance using this log ID and error code. For more information, see [Help and technical support](https://www.coze.com/docs/guides/help_and_support)."""

    logid: str


class BotModelInfoConfig(CozeModel):
    """最大回复长度"""

    max_tokens: Optional[int]
    """模型id"""
    model_id: str
    """存在惩罚"""
    presence_penalty: Optional[float]
    """生成随机性"""
    temperature: Optional[float]
    """top p"""
    top_p: Optional[float]
    """频率惩罚"""
    frequency_penalty: Optional[float]
    """输出格式 text、markdown、json"""
    response_format: Optional[str]
    """生成时，采样候选集的大小"""
    top_k: Optional[int]
    """携带上下文轮数"""
    context_round: Optional[int]


class VoiceData(CozeModel):
    """Unique ID"""

    id: Optional[str]
    """Timbre language code"""
    language_code: Optional[str]
    """Timbre language name"""
    language_name: Optional[str]
    """Timbre name"""
    name: Optional[str]
    """Preview tone content."""
    preview_audio: Optional[str]
    """Preview the text content"""
    preview_text: Optional[str]
    """Timbre style_id"""
    style_id: Optional[str]


class BotOnboardingInfo(CozeModel):
    """Agent's opening remarks. Length: 0~300 characters. Default: no opening remarks.
    If the opening remarks include the user name variable `{{user_name}}`, the business side needs to handle it in the API scenario, such as replacing this variable with the user's name on the business side when displaying the opening remarks."""

    prologue: str
    """Preset questions for agent's opening remarks. Each question should be 0~50 characters in length, with an unlimited number of questions. No default preset questions."""
    suggested_questions: List[str]


class ShortcutCommandComponent(CozeModel):
    """默认值 没配置时不返回"""

    default_value: Optional[str]
    """参数描述"""
    description: Optional[str]
    """是否隐藏不展示 线上bot tool类型的快捷指令不返回hide=true的component"""
    is_hide: Optional[bool]
    """panel参数参数名字"""
    name: Optional[str]
    """type为select时的可选项列表 or type为file时，支持哪些类型 image、doc、table、audio、video、zip、code、txt、ppt"""
    options: Optional[List[str]]
    """请求工具时，参数的key 对应tool的参数名称，没有则为不返回"""
    tool_parameter: Optional[str]
    """输入类型 text、select、file"""
    type: Optional[str]


class SuggestedQuestionsShowMode(IntEnum):
    RANDOM = 0  #
    ALL = 1  #


class OnboardingMode(IntEnum):
    NO_NEED = 1  #
    USE_MANUAL = 2  #
    USE_LLM = 3  #


class BotOnboardingInfoV2(CozeModel):
    suggested_questions_show_mode: Optional[SuggestedQuestionsShowMode]
    """LLM generation, user-customized Prompt"""
    customized_onboarding_prompt: Optional[str]
    onboarding_mode: Optional[OnboardingMode]
    """Opening remarks for agent configuration.
    If the opening remarks set a user name variable `{{user_name}}`, the business side needs to handle it by itself in the API scenario, such as replacing this variable with the user name on the business side when displaying the opening remarks."""
    prologue: Optional[str]
    """Recommended list of agent configuration questions. This field is not returned when user question suggestions are not enabled."""
    suggested_questions: Optional[List[str]]


class KnowledgeInfo(CozeModel):
    """Knowledge Base Name."""

    name: Optional[str]
    """Knowledge Base ID."""
    id: Optional[str]


class BotMode(IntEnum):
    SINGLE_AGENT = 0  #
    MULTI_AGENT = 1  #
    SINGLE_AGENT_WORKFLOW = 2  #


"""The search strategy for the knowledge base. Values include:
    0: (Default) Semantic search. Understand the relationships between words and sentences like a human does.
    1: Hybrid search. Combine the advantages of full-text retrieval and semantic search, and sort the results comprehensively to recall relevant content fragments.
    20: Full-text search. Full-text retrieval based on keywords."""


class SearchStrategy(IntEnum):
    SEMANTIC_SEARCH = 0  #
    HYBRID_SEARCH = 1  #
    FULL_TEXT_SEARCH = 20  #


class BotPluginAPIInfo(CozeModel):
    """Unique identifier of the tool."""

    api_id: str
    """Description of the tool."""
    description: str
    """The name of the tool."""
    name: str


class BotPluginInfo(CozeModel):
    """Information about the tool list of the plugin."""

    api_info_list: List[BotPluginAPIInfo]
    """Plugin Description."""
    description: str
    """Plugin avatar."""
    icon_url: str
    """Plugin Name."""
    name: str
    """Plugin unique identifier."""
    plugin_id: str


class ShortcutCommandToolInfo(CozeModel):
    name: Optional[str]
    """tool类型 workflow plugin"""
    type: Optional[str]


class ShortcutCommandInfo(CozeModel):
    """快捷指令按钮名称"""

    name: Optional[str]
    tool: Optional[ShortcutCommandToolInfo]
    """multi的指令时，该指令由哪个节点执行 没配置不返回"""
    agent_id: Optional[str]
    """快捷指令"""
    command: Optional[str]
    """组件列表（参数列表）"""
    components: Optional[List[ShortcutCommandComponent]]
    """快捷指令描述"""
    description: Optional[str]
    """快捷指令icon"""
    icon_url: Optional[str]
    """快捷指令id"""
    id: Optional[str]
    """指令query模版"""
    query_template: Optional[str]


class WorkflowInfo(CozeModel):
    """workflow描述"""

    description: Optional[str]
    """workflow图片url"""
    icon_url: Optional[str]
    """workflow_id"""
    id: Optional[str]
    """workflow名称"""
    name: Optional[str]


class BotPromptInfo(CozeModel):
    """The persona and response logic of the intelligent agent. Length is 0~20,000 characters. Default is empty."""

    prompt: str


class BotModelInfo(CozeModel):
    """最大回复长度"""

    max_tokens: int
    """Model Name."""
    model_name: str
    """生成时，采样候选集的大小 没配置不返回"""
    top_k: int
    """top p 没配置不返回"""
    top_p: float
    """携带上下文轮数"""
    context_round: int
    """频率惩罚 没配置不返回"""
    frequency_penalty: float
    """输出格式 text、markdown、json"""
    response_format: str
    """生成随机性 没配置不返回"""
    temperature: float
    """Unique identifier of the model."""
    model_id: str
    """存在惩罚 没配置不返回"""
    presence_penalty: float


class CommonKnowledge(CozeModel):
    """Knowledge base information."""

    knowledge_infos: Optional[List[KnowledgeInfo]]


class Bot(CozeModel):
    """Avatar URL of the intelligent agent."""

    icon_url: Optional[str]
    onboarding_info: Optional[BotOnboardingInfoV2]
    """Agent configuration plugins."""
    plugin_info_list: Optional[List[BotPluginInfo]]
    prompt_info: Optional[BotPromptInfo]
    """快捷指令信息列表"""
    shortcut_commands: Optional[List[ShortcutCommandInfo]]
    """Update time, formatted as a 10-digit Unix timestamp in seconds (s)."""
    update_time: Optional[int]
    """workflow信息列表"""
    workflow_info_list: Optional[List[WorkflowInfo]]
    """Description of the agent."""
    description: Optional[str]
    model_info: Optional[BotModelInfo]
    knowledge: Optional[CommonKnowledge]
    """Create time, formatted as a 10-digit Unix timestamp, in seconds (s)."""
    create_time: Optional[int]
    """Agent Name."""
    name: Optional[str]
    """The version number of the latest release of the agent."""
    version: Optional[str]
    """Selected voice information"""
    voice_data_list: Optional[List[VoiceData]]
    """The unique identifier of the agent."""
    bot_id: Optional[str]
    bot_mode: Optional[BotMode]


class WorkflowIdInfo(CozeModel):
    id: str


class Knowledge(CozeModel):
    """Whether to automatically call the knowledge base. The values include:
    - **true: (default) automatically call**. The knowledge base is called in each round of conversation, using the recalled content to assist in generating replies.
    - **false: call as needed**. The knowledge base is called based on actual needs, using the recalled content to assist in generating replies. In this case, it is necessary to clearly specify in the persona and reply logic area on the left under what circumstances to call which knowledge base to reply."""

    auto_call: Optional[bool]
    """The knowledge base ID bound to the agent.
    In the Button platform, open the specified knowledge base page, and the number after the knowledge parameter in the page URL is the knowledge base ID. For example, https://bots.bytedance.net/space/736142423532160****/knowledge/738509371792341****, the knowledge base ID is 738509371792341****."""
    dataset_ids: Optional[List[str]]
    """The search strategy for the knowledge base. Values include:
    0: (Default) Semantic search. Understand the relationships between words and sentences like a human does.
    1: Hybrid search. Combine the advantages of full-text retrieval and semantic search, and sort the results comprehensively to recall relevant content fragments.
    20: Full-text search. Full-text retrieval based on keywords."""
    search_strategy: Optional[SearchStrategy]


class CreateDraftBotData(CozeModel):
    """The ID of the created agent."""

    bot_id: str


class WorkflowIdList(CozeModel):
    ids: Optional[List[WorkflowIdInfo]]


class PublishDraftBotData(CozeModel):
    """The ID of the agent."""

    bot_id: Optional[str]
    """The version of the agent."""
    version: Optional[str]


class UpdateBotResp(CozeModel):
    pass


"""
API Client for bots endpoints
"""


class Client(object):
    def __init__(self, base_url: str, auth: Auth, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._auth = auth
        self._requester = requester

    """
    Publish the specified agent to API, Web SDK, or custom channels.
    :param bot_id: 
    :param connector_ids: 
    :return: 
    """

    def publish(
        self,
        *,
        bot_id: str,
        connector_ids: List[str],
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/publish"
        return self._requester.request(
            "POST",
            url,
            False,
            cast=Bot,
            body={
                "bot_id": bot_id,
                "connector_ids": connector_ids,
            },
        )

    """
    To get the configuration of a specified agent, the agent must be published to the Agent as API channel.
This API only supports viewing agents that have already been published as API services. For agents that have never been published as API, you can view the list and configuration on the [Coze platform](https://www.coze.com/).
    :param bot_id: To view the agent ID, go to the agent's development page. The number following the `bot` parameter in the development page URL is the agent ID. For example, in `https://www.coze.cn/space/341****/bot/73428668*****`, the bot ID is `73428668*****`.


Ensure that the space to which the agent belongs has generated an access token.
    :return: 
    """

    def retrieve(
        self,
        *,
        bot_id: str,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/get_online_info"
        params = {
            "bot_id": bot_id,
        }
        return self._requester.request(
            "GET",
            url,
            False,
            cast=Bot,
            params=params,
        )

    """
    View the list of agents published to the Agent as API channel in the specified space.
    :param space_id: The Space ID of the space where the agent is located. The Space ID is the unique identifier of the space. To enter the specified space, the number following the `space` parameter in the space page URL is the Space ID. For example, `https://www.coze.cn/space/736163827687053****/bot`, the Space ID is `736163827687053****`.
    :param page_num: Page size. The default is 20, meaning 20 data entries are returned per page.
    :param page_size: Page number for pagination. Defaults to 1, which means data is returned starting from the first page.
    :return: 
    """

    def list(
        self,
        *,
        space_id: str,
        page_num: int,
        page_size: int,
    ) -> NumberPaged[SimpleBot]:
        url = f"{self._base_url}/v1/space/published_bots_list"

        def request_maker(i_page_num: int, i_page_size: int) -> HTTPRequest:
            return self._requester.make_request(
                "GET",
                url,
                params={
                    "space_id": space_id,
                    "page_index": i_page_num,
                    "page_size": i_page_size,
                },
                cast=_PrivateListBotsData,
                is_async=False,
                stream=False,
            )

        return NumberPaged(
            page_num=page_num,
            page_size=page_size,
            requestor=self._requester,
            request_maker=request_maker,
        )

    """
    Update the configuration of the agent.
Through this API, you can update all agents created through the Cozy platform or API. In addition to updating the agent's name and description, avatar, persona, and response logic and opening remarks via the API, it also supports binding knowledge bases and plugins to the agent.
    :param icon_file_id: 
    :param description: 
    :param knowledge: 
    :param workflow_id_list: 
    :param bot_id: 
    :param name: 
    :param model_info_config: 
    :param onboarding_info: 
    :param prompt_info: 
    :return: 
    """

    def update(
        self,
        *,
        icon_file_id: Optional[str] = None,
        description: Optional[str] = None,
        knowledge: Optional[Knowledge] = None,
        workflow_id_list: Optional[WorkflowIdList] = None,
        bot_id: str,
        name: Optional[str] = None,
        model_info_config: Optional[BotModelInfoConfig] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        prompt_info: Optional[BotPromptInfo] = None,
    ) -> UpdateBotResp:
        url = f"{self._base_url}/v1/bot/update"
        return self._requester.request(
            "POST",
            url,
            False,
            cast=UpdateBotResp,
            body={
                "icon_file_id": icon_file_id,
                "description": description,
                "knowledge": knowledge.model_dump() if knowledge else None,
                "workflow_id_list": workflow_id_list.model_dump() if workflow_id_list else None,
                "bot_id": bot_id,
                "name": name,
                "model_info_config": model_info_config.model_dump() if model_info_config else None,
                "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
                "prompt_info": prompt_info.model_dump() if prompt_info else None,
            },
        )

    """
    Create a new agent.
After calling this API to create an agent, the agent will be in an unpublished draft state. After creation, you can view the agent in the Coze platform's agent list. Call the [Publish agent as an API service](https://www.coze.com/docs/developer_guides/publish_bot) API to publish the agent as API service, then you can view this agent by calling [Get agent list](https://www.coze.com/docs/developer_guides/published_bots_list) or [Get agent configs](https://www.coze.com/docs/developer_guides/get_metadata) API. 
When creating an agent via the API, you can set the space where the agent is located, the agent's name and description, avatar, personality and reply logic, and opening remarks.
    :param model_info_config: 
    :param name: 
    :param onboarding_info: 
    :param prompt_info: 
    :param space_id: 
    :param workflow_id_list: 
    :param description: 
    :param icon_file_id: 头像文件id
    :return: 
    """

    def create(
        self,
        *,
        model_info_config: Optional[BotModelInfoConfig] = None,
        name: str,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        space_id: str,
        workflow_id_list: Optional[WorkflowIdList] = None,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/create"
        return self._requester.request(
            "POST",
            url,
            False,
            cast=Bot,
            body={
                "model_info_config": model_info_config.model_dump() if model_info_config else None,
                "name": name,
                "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
                "prompt_info": prompt_info.model_dump() if prompt_info else None,
                "space_id": space_id,
                "workflow_id_list": workflow_id_list.model_dump() if workflow_id_list else None,
                "description": description,
                "icon_file_id": icon_file_id,
            },
        )


"""
Async API Client for bots endpoints
"""


class AsyncClient(object):
    def __init__(self, base_url: str, auth: Auth, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._auth = auth
        self._requester = requester

    """
    Publish the specified agent to API, Web SDK, or custom channels.
    :param bot_id: 
    :param connector_ids: 
    :return: 
    """

    async def publish(
        self,
        *,
        bot_id: str,
        connector_ids: List[str],
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/publish"
        return await self._requester.arequest(
            "POST",
            url,
            False,
            cast=Bot,
            body={
                "bot_id": bot_id,
                "connector_ids": connector_ids,
            },
        )

    """
    To get the configuration of a specified agent, the agent must be published to the Agent as API channel.
This API only supports viewing agents that have already been published as API services. For agents that have never been published as API, you can view the list and configuration on the [Coze platform](https://www.coze.com/).
    :param bot_id: To view the agent ID, go to the agent's development page. The number following the `bot` parameter in the development page URL is the agent ID. For example, in `https://www.coze.cn/space/341****/bot/73428668*****`, the bot ID is `73428668*****`.


Ensure that the space to which the agent belongs has generated an access token.
    :return: 
    """

    async def retrieve(
        self,
        *,
        bot_id: str,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/get_online_info"
        params = {
            "bot_id": bot_id,
        }
        return await self._requester.arequest(
            "GET",
            url,
            False,
            cast=Bot,
            params=params,
        )

    """
    View the list of agents published to the Agent as API channel in the specified space.
    :param space_id: The Space ID of the space where the agent is located. The Space ID is the unique identifier of the space. To enter the specified space, the number following the `space` parameter in the space page URL is the Space ID. For example, `https://www.coze.cn/space/736163827687053****/bot`, the Space ID is `736163827687053****`.
    :param page_num: Page size. The default is 20, meaning 20 data entries are returned per page.
    :param page_size: Page number for pagination. Defaults to 1, which means data is returned starting from the first page.
    :return: 
    """

    async def list(
        self,
        *,
        space_id: str,
        page_num: int,
        page_size: int,
    ) -> AsyncNumberPaged[SimpleBot]:
        url = f"{self._base_url}/v1/space/published_bots_list"

        def request_maker(i_page_num: int, i_page_size: int) -> HTTPRequest:
            return self._requester.make_request(
                "GET",
                url,
                params={
                    "space_id": space_id,
                    "page_index": i_page_num,
                    "page_size": i_page_size,
                },
                cast=_PrivateListBotsData,
                is_async=True,
                stream=False,
            )

        return await AsyncNumberPaged.build(
            page_num=page_num,
            page_size=page_size,
            requestor=self._requester,
            request_maker=request_maker,
        )

    """
    Update the configuration of the agent.
Through this API, you can update all agents created through the Cozy platform or API. In addition to updating the agent's name and description, avatar, persona, and response logic and opening remarks via the API, it also supports binding knowledge bases and plugins to the agent.
    :param icon_file_id: 
    :param description: 
    :param knowledge: 
    :param workflow_id_list: 
    :param bot_id: 
    :param name: 
    :param model_info_config: 
    :param onboarding_info: 
    :param prompt_info: 
    :return: 
    """

    async def update(
        self,
        *,
        icon_file_id: Optional[str] = None,
        description: Optional[str] = None,
        knowledge: Optional[Knowledge] = None,
        workflow_id_list: Optional[WorkflowIdList] = None,
        bot_id: str,
        name: Optional[str] = None,
        model_info_config: Optional[BotModelInfoConfig] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        prompt_info: Optional[BotPromptInfo] = None,
    ) -> UpdateBotResp:
        url = f"{self._base_url}/v1/bot/update"
        return await self._requester.arequest(
            "POST",
            url,
            False,
            cast=UpdateBotResp,
            body={
                "icon_file_id": icon_file_id,
                "description": description,
                "knowledge": knowledge.model_dump() if knowledge else None,
                "workflow_id_list": workflow_id_list.model_dump() if workflow_id_list else None,
                "bot_id": bot_id,
                "name": name,
                "model_info_config": model_info_config.model_dump() if model_info_config else None,
                "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
                "prompt_info": prompt_info.model_dump() if prompt_info else None,
            },
        )

    """
    Create a new agent.
After calling this API to create an agent, the agent will be in an unpublished draft state. After creation, you can view the agent in the Coze platform's agent list. Call the [Publish agent as an API service](https://www.coze.com/docs/developer_guides/publish_bot) API to publish the agent as API service, then you can view this agent by calling [Get agent list](https://www.coze.com/docs/developer_guides/published_bots_list) or [Get agent configs](https://www.coze.com/docs/developer_guides/get_metadata) API. 
When creating an agent via the API, you can set the space where the agent is located, the agent's name and description, avatar, personality and reply logic, and opening remarks.
    :param model_info_config: 
    :param name: 
    :param onboarding_info: 
    :param prompt_info: 
    :param space_id: 
    :param workflow_id_list: 
    :param description: 
    :param icon_file_id: 头像文件id
    :return: 
    """

    async def create(
        self,
        *,
        model_info_config: Optional[BotModelInfoConfig] = None,
        name: str,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        space_id: str,
        workflow_id_list: Optional[WorkflowIdList] = None,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/create"
        return await self._requester.arequest(
            "POST",
            url,
            False,
            cast=Bot,
            body={
                "model_info_config": model_info_config.model_dump() if model_info_config else None,
                "name": name,
                "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
                "prompt_info": prompt_info.model_dump() if prompt_info else None,
                "space_id": space_id,
                "workflow_id_list": workflow_id_list.model_dump() if workflow_id_list else None,
                "description": description,
                "icon_file_id": icon_file_id,
            },
        )
