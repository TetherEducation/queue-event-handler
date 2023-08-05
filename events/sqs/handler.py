import base64
import json
import logging
from typing import Dict

from chalice.app import SQSEvent, SQSRecord
from utils.errors import AdmissionNotFoundError
from .qualtrics_sqs_handler import QualtricsSQSHandler
from .payment_sqs_handler import PaymentSQSHandler
from .event_types import EventType

log = logging.getLogger("logdna")


class SQSHandler:
    """A class for handling SQS events."""

    @classmethod
    def process_and_decode_sqs_record(cls, record: SQSRecord) -> Dict:
        """Process an SQS event. Decodes the event if encoded and handles it.
        Args:
            record (): The SQS record to process.
        Returns:
            dict: A dictionary containing the response of the event handling.
        """
        json_body = json.loads(record.body)
        if "body_encoded" in json_body:
            if json_body["body_encoded"]:
                log.info(
                    "Encoded message received. Decoding message...",
                    {"message": f"{record.body}"},
                )
                content = json_body["content"]
                return json.loads(base64.b64decode(content).decode("utf-8"))
        log.info("Not encoded message, returning record body", {"message": f"{record.body}"})
        return json_body

    @staticmethod
    def handle(event_object: SQSEvent, event_type: EventType):
        """Handle an SQS event.
        Args:
            event_object (SQSEvent): The SQS event to handle.
            event_type (EventType): The type of the event.
        Returns:
            dict: A dictionary containing the response of the event handling.
        """
        for record in event_object:
            try:
                log.debug(
                    f"Processing message {record.to_dict().get('messageId', None)} from queue",
                    {"message": f"{record.body}"},
                )
                body = SQSHandler.process_and_decode_sqs_record(record=record)
                if event_type == EventType.UPDATE_ADMISSION_FILLING_ENROLLMENT_STATUS:
                    return QualtricsSQSHandler.handle(event=body)
                elif event_type == EventType.UPDATE_ADMISSION_PAYMENT_STATUS:
                    return PaymentSQSHandler.handle(event=body)
            except Exception as error:
                log.info(
                    f"Returning message {record.to_dict().get('messageId')} to queue"
                )
                if isinstance(error, AdmissionNotFoundError):
                    raise AdmissionNotFoundError(error)
                else:
                    raise Exception(error)
