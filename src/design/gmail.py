"""
How would you design Gmail?

Use cases:
    - what is Gmail good at?
        - non-intrusive communication
        - flexible array of formats
        - not as sensitive to latency
        - can connect chains of messages
        - can forward messages to multiple recipients with history


Users:
    - Individuals
        - create messages & send to a set of recipients
        - read messages
        - search for messages
        - create user accounts
    - Administrators
        - moderate content
        - moderate users
        - ensure reliability of infrastructure (performance, scaling)

Compliance:
    - Data privacy
    - Data locality

(User_1) --> (Browser)
                 --> (gmail.com)
                          --> (DNS server chain)
                          <-- IP address
                 --> (gmail.com: get page)
                 <-- redirect to auth.google.com to enter credentials
                 --> (auth.google.com: username/password)
                 <-- redirect to original request, set cookie with auth token
                 --> (gmail.com: get page w/ credentials)
                 <-- data: html/css/js for homepage
                 --> render html/css/js
                        --> (gmail.com: get last 50 messages w/ credentials)
                        <-- data: subject/body/attachment_ids for last 50 messages
                 --> click attachment
                        --> (gmail.com: get attachment by id w/ credentials)
                        <-- data: attachment type and bytes
(Gmail Service)
      API: mail.google.com/v1/
            - GET messages?messages=50&page=1 (get messages)
            - GET messages?messages=50&page=1&search=job,interview (search messages)
            - GET attachments/<id> (dynamically loading attachments)
            - POST messages (create message)
                - {
                      subject: ...,
                      body: "test message",
                      recipients: [tom@gmail.com, jim@gmail.com],
                      content_type: text/plain,
                }
                - {
                      subject: ...,
                      body: <html ...>,
                      recipients: [tom@gmail.com, jim@gmail.com],
                      content_type: text/html,
                }
                - Likely going to want to disable scripting within these types of messages and also scan them for
                  potentially malicious activity.

      Database:
            - SQL vs. NoSQL?
                - Emails tend to be immutable --> NoSQL
                - Emails tend not to require transactional behavior --> NoSQL
                - Emails don't tend to have very strong consistency requirements, eventually consistent is good enough.
                    --> NoSQL
                - Pick a database technology that is really fast at doing certain types of searches.
                    --> BigTable and Cloud Spanner are very good at prefix searches on extremely large data sets.
            - Schema
                - user (replicated multi-region):
                    - id: UUID
                    - name: str (John Doe)
                    - account_name: str (xyz@gmail.com)
                    - region: str (us-east-1)
                - emails_by_time: user_id:time:...
                    - Allows you to find the last n emails for a user with a single limited-range scan
                - emails_by_id: user_id:email_id:...
                    - Allows you to easily find an email for a user
                - emails_by_keyword: keyword:user_id:time:email_id:...
                    - Allows you to easily find all emails where there was a specific keyword
                - email_versions: email_id:version_id
                    - Allows for email migrations to happen piecemeal, only really required for mass migrations.

            - Scaling
                - Picked keys that typically start with user_id because we're likely going to be using a multi-tenant
                  architecture where everyone's data is in the same data store.
                - If we were to split out the data stores by user_id, there would be a lot of overhead and data skew
                  depending on the type of user. We can be reasonably certain that across a wide pool of users, there
                  will be some average load across multiple sets of users.
                - user_id will make it very efficient to load data per user (the typical use case).
                - user_id will eliminate data hotspots in a server because the data access patterns will be effectively
                  random, provided that we have a randomized implementation of user_id (UUID, as opposed to incrementing
                  an integer).

            - Multi-Region
                - We can likely establish clusters of servers tied to a home region, because users don't tend to move
                  from region to region very frequently.
                - user table can be replicated multi-region but may be too expensive to replicate email tables
                  multi-region.

            - Get last n messages for user_id
                - Scan emails_by_time with prefix user_id get last n rows, return data associated with those rows.
            - Get last n messages that contain keyword
              OPTION A
                - Scan emails_by_keyword with prefix keyword:user_id and get last n rows.
                - Scan emails_by_id with prefix user_id:email_id for each of n email_ids. This requires n queries.
                - Return all data from these queries.
              OPTION B
                - Scan emails_by_keyword with prefix keyword:user_id and get last n rows.
                - Find the min/max time range for these emails. If the estimated number of emails in this time range is
                  small, scan emails_by_time from prefix user_id:start -> user_id:end, with filter on email_id in list
                  of email_ids. This requires 1 query, or perhaps multiple queries but fewer than n queries.
                - Return all data from these queries.
            - Write new email
                - Generate a UUID and timestamp for the email.
                - Scan keywords within email, and write each keyword to emails_by_keyword.
                - Write to email_versions, emails_by_time, emails_by_id.
                - Client does not need to wait for all of this to finish, they can be satisfied with just posting an
                  email to a message queue and then waiting for the underlying infrastructure to deal with it.
                - What you use as a message queue depends on your load requirements, durability, etc.
                - Kafka does a lot of things very nicely, especially allowing multiple consumer groups to consume
                  messages within the queue at different rates and fo different reasons.
"""