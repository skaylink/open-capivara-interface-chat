# turn_context.activity.locale
# context.activity.channel_id == "emulator"
# turn_context.activity.from_property.name
import logging
import traceback
import os
import traceback
from datetime import datetime
import os
import json
import logging

import shared
from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.schema import Activity, ActivityTypes


from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)


from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount



class BaseBot(ActivityHandler):
    name = 'Base Bot'

    def __init__(self, qna_connector):
        self.qna_connector = qna_connector
        super(BaseBot, self).__init__()

    async def on_members_added_activity(
        self, 
        members_added: [ChannelAccount], 
        turn_context: TurnContext,
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(await self.compose_activity_into(turn_context))

    async def on_message_activity(self, turn_context: TurnContext):
        #logging.info(f'>>>>>> dir turn_context: {dir(turn_context)}')
        #""" ['_INVOKE_RESPONSE_KEY', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_activity', '_emit', '_on_delete_activity', '_on_send_activities', '_on_update_activity', '_responded', '_services', '_turn_state', 'activity', 'adapter', 'apply_conversation_reference', 'buffered_reply_activities', 'copy_to', 'delete_activity', 'get', 'get_conversation_reference', 'get_mentions', 'get_reply_conversation_reference', 'has', 'on_delete_activity', 'on_send_activities', 'on_update_activity', 'remove_mention_text', 'remove_recipient_mention', 'responded', 'responses', 'send_activities', 'send_activity', 'send_trace_activity', 'services', 'set', 'turn_state', 'update_activity'] """
        #logging.info(f'>>>>>> dir turn_context.activity: {dir(turn_context.activity)}')
        #""" ['_Activity__is_activity', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_attribute_map', '_classify', '_create_xml_node', '_flatten_subtype', '_get_rest_key_parts', '_infer_class_models', '_subtype_map', '_validation', 'action', 'additional_properties', 'apply_conversation_reference', 'as_contact_relation_update_activity', 'as_conversation_update_activity', 'as_dict', 'as_end_of_conversation_activity', 'as_event_activity', 'as_handoff_activity', 'as_installation_update_activity', 'as_invoke_activity', 'as_message_activity', 'as_message_delete_activity', 'as_message_reaction_activity', 'as_message_update_activity', 'as_suggestion_activity', 'as_trace_activity', 'as_typing_activity', 'attachment_layout', 'attachments', 'caller_id', 'channel_data', 'channel_id', 'code', 'conversation', 'create_contact_relation_update_activity', 'create_conversation_update_activity', 'create_end_of_conversation_activity', 'create_event_activity', 'create_handoff_activity', 'create_invoke_activity', 'create_message_activity', 'create_reply', 'create_trace', 'create_trace_activity', 'create_typing_activity', 'delivery_mode', 'deserialize', 'enable_additional_properties_sending', 'entities', 'expiration', 'from_dict', 'from_property', 'get_conversation_reference', 'get_mentions', 'get_reply_conversation_reference', 'has_content', 'history_disclosed', 'id', 'importance', 'input_hint', 'is_from_streaming_connection', 'is_xml_model', 'label', 'listen_for', 'local_timestamp', 'local_timezone', 'locale', 'members_added', 'members_removed', 'name', 'reactions_added', 'reactions_removed', 'recipient', 'relates_to', 'reply_to_id', 'semantic_action', 'serialize', 'service_url', 'speak', 'suggested_actions', 'summary', 'text', 'text_format', 'text_highlights', 'timestamp', 'topic_name', 'type', 'validate', 'value', 'value_type'] """
        text = turn_context.activity.text

        if 'question:' in text:
            question = text.split('question:')[-1]
            worked, answer = await self.qna_connector.get_answers(question = question)
            await turn_context.send_activity(
                MessageFactory.text(answer)
            )
        else:
            await turn_context.send_activity(
                MessageFactory.text(f"Echo of {turn_context.activity.from_property.name}: {text}")
            )

    async def compose_activity_into(self, turn_context) -> Activity:
        card = HeroCard(
            title="Welcome to Bot Framework!",
            text="Welcome to Welcome Users bot sample! This Introduction card "
            "is a great way to introduce your Bot to the user and suggest "
            "some things to get them started. We use this opportunity to "
            "recommend a few next steps for learning more creating and deploying bots.",
            images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Get an overview",
                    text="Get an overview",
                    display_text="Get an overview",
                    value="https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Ask a question",
                    text="Ask a question",
                    display_text="Ask a question",
                    value="https://stackoverflow.com/questions/tagged/botframework",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Learn how to deploy",
                    text="Learn how to deploy",
                    display_text="Learn how to deploy",
                    value="https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-deploy-azure?view=azure-bot-service-4.0",
                ),
            ],
        )
        return MessageFactory.attachment(CardFactory.hero_card(card))
