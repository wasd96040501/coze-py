"""
This example is about how to create conversation and retrieve.
"""

import logging
import os

from cozepy import (  # noqa
    COZE_COM_BASE_URL,
    BotPromptInfo,
    ChatEventType,
    Coze,
    Message,
    MessageContentType,
    MessageRole,
    TokenAuth,
    setup_logging,
)

# Get an access_token through personal access token or oauth.
coze_api_token = os.getenv("COZE_API_TOKEN")
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = os.getenv("COZE_API_BASE") or COZE_COM_BASE_URL
# Whether to print detailed logs
is_debug = os.getenv("DEBUG")

if is_debug:
    setup_logging(logging.DEBUG)

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

conversation = coze.conversations.create()
print("Create conversation: ", conversation)

conversation_retrieve = coze.conversations.retrieve(conversation_id=conversation.id)
print("Retrieve conversation:", conversation_retrieve)

message = coze.conversations.messages.create(
    conversation_id=conversation.id,
    role=MessageRole.USER,
    content="hi",
    content_type=MessageContentType.TEXT,
)

print("Append message to conversation:", message)
