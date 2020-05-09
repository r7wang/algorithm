"""
How would you design the infrastructure for a messaging application?

Use cases:
    - Real-time communication between two or more users


Users:
    - Individuals
        - send message to another user (text, image, etc.)
        - view / update user profile


Constraints:
    - Must support groups of users (channels)
    - Must support chat history up to 7 days
    - Must support sending pictures
    - Channel must be able to support up to 1000 users


(User_1) --> (MobileApp)
                --> (messaging.com, authentication flows: get user info)
                <-- data: user profile or user subscriptions
                --> point to specific channel
                        --> (messaging.com: get messages in channel from current offset)
                        <-- data: messages from given offset to current offset
                --> render messages


(Messaging Service):
    Websocket: wss://ws.messaging.com?token=...
        SEND
        {
            type: "subscribe",
            channel_id: 12312,
            offset: <int64>, (only works for single partition topics)
        }
        {
            type: "unsubscribe",
            channel_id: 12311,
        }
        {
            type: "message",
            channel_id: 12312,
            type: TEXT,
            content: "What did you do yesterday?"
        }
        RECEIVE
        {
            timestamp: 1232342134,
            channel_id: 12312,
            type: TEXT,
            content_id: 1235,
            content: "What did you do yesterday?",
            offset: <int64>, (only works for single partition topics)
        }
        {
            timestamp: 1232342134,
            channel_id: 12312,
            type: IMAGE,
            content_id: 1234,
            offset: <int64>, (only works for single partition topics)
        }

    API: messaging.com/api/v1/
        - images/<id> (gets a time-limited content url for content dumped to an S3 bucket)

    Intermediaries:
        - We don't want clients talking directly to Kafka, but rather talking to services that can make requests on
          behalf of the client. These services are essentially more sophisticated load balancers / gateways.
            - Authentication
            - Load balancing (understand how many clients they're interacting with, and what channels they serve)

    Scaling:
      Groups / Channels
        - We can start by using a Kafka topic for every channel_id, where every topic only has a single partition.
          This, however, doesn't scale beyond a certain amount of load.
        - We can then extend the solution to have multiple partitions per topic, where a given user writes to a single
          partition (assigned randomly) and a given user reads from all partitions simultaneously, using some form of
          timestamp-based merge sorting to put the messages back in the right order.
        - This increases the write capacity, but doesn't help read capacity, because every client still needs to read
          from all partitions.
        - This potentially introduces a slight amount of delay and complexity on the client-side, but allows Kafka to
          handle greater consumer load.
      1:1
        - Unlikely to have sufficient load to be problematic. All of these conversations can have their own topic and
          will likely not require more than 1 broker.
"""
