# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from filter_data import FilterData

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEV = False

EXCEPTION_MESSAGE = "Sorry, an error occurred."
HELP_MESSAGE = "Du kannst tehade Mensa sagen um mich nach den Gerichten der Mensa zu fragen."
HELP_REPROMPT = "Wie kann ich dir denn helfen?"
FALLBACK_MESSAGE = "FB"
FALLBACK_REPROMPT = "FB Reprompt"
STOP_MESSAGE = "Ok, Tschüss!"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        # filt_json = FilterData()
        # out = filt_json.getHauptgericht("28.10.2019")
        out = "Hallo, ich bin Alexa, wie heißt du?"

        handler_input.response_builder.speak(out).ask("1")
        return handler_input.response_builder.response


class CaptureAllIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or is_intent_name("CaptureAllIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        """
        
        Note:
        There is a difference between: 
        
        date = slots['datum']
        and 
        date = slots['datum'].resolutions.resolutions_per_authority[0].values[0].value
        
        See the snippet of the alexa response below:
        
        "vorliebe": {
					"name": "vorliebe",
					"value": "vegetarisches",
					
		and
		
		"values": [
									{
										"value": {
											"name": "Vegetarisch",
        
        E.g. the first value represents the actual input by the user. The second value represents the slot value
        as we have defined it in the alexa model.
        
        """

        date = slots['datum']
        preference = slots['vorliebe']
        allergie = slots['allergie']

        if date.value:
            date = date.value
        else:
            if DEV:
                date = 'None'
            else:
                date = None

        if preference.value:
            preference = preference.resolutions.resolutions_per_authority[0].values[0].value.name
        else:
            if DEV:
                preference = 'None'
            else:
                preference = None

        if allergie.value:
            allergie = allergie.resolutions.resolutions_per_authority[0].values[0].value.name
        else:
            if DEV:
                allergie = 'None'
            else:
                allergie = None

        fj = FilterData(warengruppe="hauptgericht", dt=date, kennz=preference, attributes=allergie)
        out = fj.get_response()

        if DEV:
            out = date + " ; " + preference + " ; " + allergie

        handler_input.response_builder.speak(out)
        return handler_input.response_builder.response


class AutoDelegationIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AutoDelegationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots

        """

        Note:
        There is a difference between: 

        date = slots['datum']
        and 
        date = slots['datum'].resolutions.resolutions_per_authority[0].values[0].value

        See the snippet of the alexa response below:

        "vorliebe": {
                    "name": "vorliebe",
                    "value": "vegetarisches",

        and

        "values": [
                                    {
                                        "value": {
                                            "name": "Vegetarisch",

        E.g. the first value represents the actual input by the user. The second value represents the slot value
        as we have defined it in the alexa model.

        """

        date = slots['datum']
        preference = slots['vorliebe']
        allergie = slots['allergie']

        if date.value:
            date = date.value
        else:
            if DEV:
                date = 'None'
            else:
                date = None

        if preference.value:
            preference = preference.resolutions.resolutions_per_authority[0].values[0].value.name
        else:
            if DEV:
                preference = 'None'
            else:
                preference = None

        if allergie.value:
            allergie = allergie.resolutions.resolutions_per_authority[0].values[0].value.name
        else:
            if DEV:
                allergie = 'None'
            else:
                allergie = None

        fj = FilterData(warengruppe="hauptgericht", dt=date, kennz=preference, attributes=allergie)
        out = fj.get_response()

        if DEV:
            out = date + " ; " + preference + " ; " + allergie

        handler_input.response_builder.speak(out)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AutoDelegationIntentHandler())
sb.add_request_handler(CaptureAllIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
