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
        - GET images/<id> (gets a time-limited content url for content dumped to an S3 bucket)
        - POST users
            - {
                user_name: the_user_1,
                email: bob@gmail.com,
                password: ...,
            }
            - Service will likely have to check that a given IP or range isn't spamming user creation or a bot.
        - GET users/<id>/profile
            - {
                ... # whatever information is relevant to this user
            }
            - The result payload may change depending on whether the user is requesting his own profile or someone
              else's profile.

    Intermediaries:
        - We don't want clients talking directly to Kafka, but rather talking to services that can make requests on
          behalf of the client. These services are essentially more sophisticated load balancers / gateways.
            - Authentication
            - Load balancing (understand how many clients they're interacting with, and what channels they serve)
            - Rate limiting

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

    Database:
        - SQL vs. NoSQL?
            - No transactional requirements --> NoSQL
            - Eventual consistency of of non-message data is okay --> NoSQL

        - Schema
            - users: id (UUID), name (str), alias (str)
            - channels: id, description, visibility (enum)
          BASIC: remember which channels the users were part of
            - subscriptions: user_id, channel_id
          ADVANCED: remember which channels the users were part of and also the last consumed timestamp
            - subscriptions: user_id, channel_id, timestamp


(Moderation Service):
    - Hook into Kafka brokers for all channels and either sample (or read all) of the messages, before running some
      kind of moderation function (text: regex, machine learning model, image: machine learning model, hash comparison
      against known illegal images)
    - Constantly update information about users that have been known to post illegal or offensive content.
    - User information to scale up searches within other channels (if not already looking at all channels).
    - Issue actions against specific users.
    - A lot of processing around moderation can be expensive and may not run in a timely manner, hence the potential
      need for heuristics to allow us to better redirect our search.
    - Found illegal content has to be removed from the platform and archived for authorities. No easy way to delete
      content from a Kafka topic but can identify set of content_ids that are illegal and should be skipped.
"""
