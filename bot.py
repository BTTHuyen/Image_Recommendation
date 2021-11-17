# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Text
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext,CardFactory
#from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
    SuggestedActions
)
from image_search import image_search

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    '''
    This Bot implementation can find the image by area, word, context.
    '''

    def __init__(self):
        self.user_area = None
        self.user_query = None
        self.area = None
        self.query = None
    async def on_message_activity(self, turn_context: TurnContext):
        if self.user_area.text == "Where are you from?":
            self.area = turn_context.activity.text
            print("area:",self.area)
            self.user_area.text = None
            return await self._suggestAnswer_question_2(turn_context)

        elif self.user_query.text == "What are you looking for?":
            self.query = turn_context.activity.text
            print("query:",self.query)
            self.user_query.text = None

            result = image_search(self.query, self.area)
            if result:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Here are some recommended images for you."))
                for url in result:
                    print(url)
                    await self._handle_outgoing_attachment(url,turn_context)
                    
                await self._display_options(turn_context)
                        
        else:
            await self._process_option(turn_context)


    async def on_members_added_activity(self, members_added: ChannelAccount,turn_context: TurnContext):
        return await self._send_welcome_message(turn_context)


    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Hi, This is AIRS-iBot."     
                    )
                )
                self.user_area = ""
                self.user_query = ""

                await self._suggestAnswer_question_1(turn_context)
                

    async def _suggestAnswer_question_1(self, turn_context: TurnContext):
        reply = MessageFactory.text("Where are you from?")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="England",
                    type=ActionTypes.im_back,
                    value="England",
                ),
                CardAction(
                    title="Vietnam",
                    type=ActionTypes.im_back,
                    value="Vietnam",
                ),
                CardAction(
                    title="Japan",
                    type=ActionTypes.im_back,
                    value="Japan",
                ),
                CardAction(
                    title="Korea",
                    type=ActionTypes.im_back,
                    value="Korea",
                ),
                CardAction(
                    title="China",
                    type=ActionTypes.im_back,
                    value="China",
                ),
                CardAction(
                    title="USA",
                    type=ActionTypes.im_back,
                    value="USA",
                ),
            ]
        )
        self.user_area = reply
        return await turn_context.send_activity(reply)

    async def _suggestAnswer_question_2(self, turn_context: TurnContext):
        reply = MessageFactory.text("What are you looking for?")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Cat",
                    type=ActionTypes.im_back,
                    value="Cat",
                ),
                CardAction(
                    title="Food",
                    type=ActionTypes.im_back,
                    value="Food",
                ),
                CardAction(
                    title="Japanese People",
                    type=ActionTypes.im_back,
                    value="Japanese People",
                ),
                CardAction(
                    title="online class",
                    type=ActionTypes.im_back,
                    value="online class",
                ),
                CardAction(
                    title="TV Show",
                    type=ActionTypes.im_back,
                    value="TV Show",
                ),
                CardAction(
                    title="Social Media",
                    type=ActionTypes.im_back,
                    value="Social Media",
                ),
            ]
        )
        self.user_query = reply
        return await turn_context.send_activity(reply)

    
    def _get_internet_attachment(self,url) -> Attachment:
        """
        Creates an Attachment to be sent from the bot to the user from a HTTP URL.
        :return: Attachment
        """
        return Attachment(
            name="",
            content_type="image/png,image/jpg,image/jpeg,image/gif",
            content_url=url,
        )


    async def _handle_outgoing_attachment(self,url, turn_context: TurnContext):
        reply = MessageFactory.text("")
        reply.attachments = [self._get_internet_attachment(url)]
        await turn_context.send_activity(reply)


    async def _display_options(self, turn_context: TurnContext):
        """
        Create a HeroCard with options for the user to interact with the bot.
        :param turn_context:
        :return:
        """

        # Note that some channels require different values to be used in order to get buttons to display text.
        # In this code the emulator is accounted for with the 'title' parameter, but in other channels you may
        # need to provide a value for other parameters like 'text' or 'displayText'.
        card = HeroCard(
            text="You can select one of the following choices",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="1. Continue learning", value="1"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="2. Developer", value="2"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="3. Quit", value="3"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)

    async def _process_option(self, turn_context: TurnContext):
        '''
        Process the option of user
        '''

        reply = Activity(type=ActivityTypes.message)

        value = turn_context.activity.text[0]
        if value == "1":
            reply.text = "Thank you for using AIRS-iBot for learning."
            await turn_context.send_activity(reply)
            self.user_area = ""
            self.user_query = ""
            await self._suggestAnswer_question_1(turn_context)
            
        elif value == "2":
            reply.text = "Research Center for Computing and Multimedia Studies, Hosei University."
            #reply.attachments = [self._get_internet_attachment()]
            await turn_context.send_activity(reply)

        elif value == "3":
            reply.text = "Thank you for using our application."
            await turn_context.send_activity(reply)

        else:
            reply.text = "Your input was not recognized, please try again."
            await turn_context.send_activity(reply)

        