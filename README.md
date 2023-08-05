## Queue Event Handler

The Queue Event Handler is a lightweight wrapper designed to streamline 
the management of Amazon Simple Queue Service (SQS) and Simple Notification 
Service (SNS) queues. This utility is intended to simplify the integration 
of queues within AWS Lambda functions developed using Chalice. For the moment,
it only supports SQS queues.

### Features

- **SQS Integration**: Easily handle messages from SQS queues with a clean and straightforward interface.
- **Chalice Compatibility**: Specifically designed for use with AWS Chalice, making it simple to handle queue messages in your serverless applications.

### Installation

To start using the Queue Event Handler, follow these simple steps:

1. Install the required dependencies:

   ```bash
   pip install queue-event-handler
   ```

2. Import the Queue Event Handler module in your AWS Lambda function:

   ```python
   from queue_event_handler import SQSHandler
   ```

### Usage

Using the Queue Event Handler is straightforward. Here's a basic example of how to set it up in your Lambda function:

```python
from chalice import Chalice
from queue_event_handler import SQSHandler

app = Chalice(app_name='my-app-name')


@app.on_sqs_message(queue='my-sqs-queue')
def process_sqs_message(event):
   # Process the SQS message here
   try:
      return SQSHandler.handle(
         event_object=event,
      )
   except Exception as error:
      log.error(f"Error processing request: {error}", exc_info=True)
      raise Exception(error)

```

Make sure to replace `'my-sqs-queue'` with the actual names of your SQS queue. Now, whenever new messages arrive in the SQS queue, the corresponding function will be triggered to process the messages.

### Contribution

We welcome contributions to improve the Queue Event Handler. If you encounter any issues or have suggestions for enhancements, please feel free to submit a pull request or create an issue in the GitHub repository.

### License

The Queue Event Handler is open-source software licensed under the MIT License. See the `LICENSE` file for more details.