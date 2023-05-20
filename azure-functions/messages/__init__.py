import logging
import azure.functions as func
import traceback
import os
import traceback
import os
import json
import logging

import shared
from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.schema import Activity


async def on_error(context: TurnContext, error: Exception):
    text = f"The bot encountered an error: {error}, {traceback.format_exc()}"
    logging.error(text)
    await context.send_activity(text)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    if ("Content-Type" in req.headers) and ("application/json" in req.headers["Content-Type"]):
        body = req.get_json()
    else:
        return func.HttpResponse('', status_code=415)

    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    settings = BotFrameworkAdapterSettings(os.getenv('APP_ID'), os.getenv('APP_PASSWORD'))
    adapter = BotFrameworkAdapter(settings)
    adapter.on_turn_error = on_error

    activity = Activity().deserialize(body)
    response = await adapter.process_activity(activity, auth_header, shared.BOT.on_turn)
    if response:
        return func.HttpResponse(data=json.dumps(response.body), status_code=response.status)
    return func.HttpResponse('', status_code=200)