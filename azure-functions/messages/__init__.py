import logging
import azure.functions as func
import traceback
import os
import traceback
from datetime import datetime
import os
import json
import logging


from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.schema import Activity, ActivityTypes



###############
# turn_context.activity.locale
# context.activity.channel_id == "emulator"
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
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


print('V0.0.1')
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, 
        members_added: [ChannelAccount], 
        turn_context: TurnContext,
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(await self.compose_activity_into(turn_context))

    async def on_message_activity(self, turn_context: TurnContext):
        logging.info(f'>>>>>> dir turn_context: {dir(turn_context)}')
        logging.info(f'>>>>>> dir turn_context.activity: {dir(turn_context.activity)}')
        await turn_context.send_activity(
            MessageFactory.text(f"Echo from {turn_context.activity.from_property.name}: {turn_context.activity.text}")
        )
        await turn_context.send_activity(
            MessageFactory.text(f"Echo again :)")
        )
        # If 'question:' in turn_context.activity.text.lower():
        # serach in QnA maker
        # return response
        # else:
        # return echo

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

###########


# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(os.getenv('APP_ID'), os.getenv('APP_PASSWORD'))
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = EchoBot()


#####
async def on_error(context: TurnContext, error: Exception):
    text = f"The bot encountered an error: {error}, {traceback.format_exc()}"
    logging.error(text)
    await context.send_activity(text)
ADAPTER.on_turn_error = on_error


async def main(req: func.HttpRequest) -> func.HttpResponse:
    if ("Content-Type" in req.headers) and ("application/json" in req.headers["Content-Type"]):
        body = req.get_json()
    else:
        return func.HttpResponse('', status_code=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return func.HttpResponse(data=json.dumps(response.body), status_code=response.status)
    return func.HttpResponse('', status_code=200)