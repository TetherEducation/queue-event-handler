import boto3
import logging

log = logging.getLogger("logdna")


def get_sqs_client():
    """
    Returns an SQS client object.
    Returns:
        obj: SQS client object
    """
    session = boto3.session.Session()
    return session.client(service_name="sqs")


def return_sqs_to_queue(queue_url: str, receipt_handle: str, message_id: str):
    """
    Returns a message to the SQS queue.
    Args:
        queue_url (str): The URL of the SQS queue.
        receipt_handle (str): The receipt handle of the message to return.
        message_id (str): The ID of the message to return.
    """
    client_sqs = get_sqs_client()
    try:
        client_sqs.change_message_visibility(
            QueueUrl=queue_url, ReceiptHandle=receipt_handle, VisibilityTimeout=0
        )
        log.info(
            f"Message {message_id} returned to queue",
            {"Queue": f"{queue_url}", "MessageId": f"{message_id}"},
        )
    except client_sqs.exceptions.ReceiptHandleIsInvalid:
        log.error(
            f"Receipt Handle {receipt_handle} not present in the queue",
            {"Queue": f"{queue_url}", "message_Id": f"{message_id}"},
        )
    except Exception as error:
        log.error(
            f"An error occurred while trying to return the message to the queue: {error}",
            {"Queue": f"{queue_url}", "message_Id": f"{message_id}"},
        )


def delete_sqs_message(queue_url: str, receipt_handle: str, message_id: str):
    """
    Delete a message from the SQS queue.
    Args:
    queue_url (str): The URL of the SQS queue.
    receipt_handle (str): The receipt handle of the message to delete.
    message_id (str): The ID of the message to delete.
    """
    client_sqs = get_sqs_client()
    try:
        client_sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        log.info(
            f"Message {message_id} deleted from queue",
            {"Queue": f"{queue_url}", "MessageId": f"{message_id}"},
        )
    except client_sqs.exceptions.ReceiptHandleIsInvalid:
        log.error(
            f"Receipt Handle {receipt_handle} not present in the queue",
            {"Queue": f"{queue_url}", "message_Id": f"{message_id}"},
        )
    except Exception as error:
        log.error(
            f"An error occurred while trying to delete the message to the queue: {error}",
            {"Queue": f"{queue_url}", "message_Id": f"{message_id}"},
        )
