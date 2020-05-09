"""
How would you design the infrastructure for a hotel reservation system?

Use cases:
    - what can this system do?
        - exposing customers to a broad set of hotels across independent clients
        - amortizing infrastructure costs across multiple clients
        - being a single source of truth for reservation information
        - aggregating data from independent clients to better understand the target market


Users:
    - Individuals
        - on vacation, business trips, need to reserve a room for variable number of days close to their location
        - pay for reservations
        - cancel existing reservations
        - compare multiple room offerings
        - request customer service
    - Administrators
        - make new rooms available for booking / remove existing rooms
        - handle payments by individuals / refunds to individuals
        - handle customer service requests


Constraints:
    - Reservations are at the "day" granularity


(User_1) --> (Browser)
                  --> (hotels.com, authentication flows: home page)
                  <-- data: html/css/js for homepage
                  --> (hotels.com: search for hotels)

(Hotel Service):
    API: hotels.com/api/
        - GET admin/v1/reservations
        - GET search/v1/rooms?location=(metro convention center)&max_dist=5km
        - GET booking/v1/reservations
        - GET booking/v1/reservations/<id>
        - POST booking/v1/reservations (if we want the user to pay as they reserve)
            - {
                hotel_id=...,
                from_date=...,
                to_date=...,
                payment: {
                    type: VISA,
                    amount: 500.03.
                    metadata: {
                        card: 1234123412341234,
                        cvc: 123,
                    }
                }
            }
        - GET booking/v1/rooms/<id>
            - {
                name=...,
                description=...,
            }
        - GET booking/v1/rooms/<id>/prices?from_date=2020-11-14&to_date=2020-11-17&options=...
            - {
                2020-11-14: 500.03,
                2020-11-15: 375.12,
                ...
            }
        - POST booking/v1/hotels (TBD)
        - POST booking/v1/rooms (TBD)
        - GET service/v1/requests (TBD)
        - POST service/v1/requests (TBD)

    Service Decomposition:
        - Bookings, which contains information about reservations and hotel rooms, should be a core service.
        - Search can be its own service, scaled independently, and record metadata/analysis on what users are
          interested in.
        - Customer service can be its own service, scaled independently, and be an entrypoint into the hotel's customer
          operations.
        - Benefits:
            - Clearer team ownership
            - When something goes down, it only affects a select domain and not all customers
            - Mitigates deployment risk

    Database:
        - SQL vs. NoSQL
            - We need to sometimes worry about transactions because multiple users may want to book the same room at
              the same time --> SQL
            - Not having a strongly consistent view of what's available may cause a user to make erroneous reservations
                --> SQL

        - Schema
            locations: id, latitude, longitude
            hotels: id, name, description, location_id
            rooms: id, hotel_id, name, description, pricing_strategy_id
            pricing_strategy: id, metadata (json)
            reservations: id, user_id, hotel_id, room_id, payment_id
            reservation_days: reservation_id, day (date)
            payments: id, amount

        - Scaling
            - There are likely not nearly as many businesses as there are customers.
            - We are going to want to add indices to the query patterns that we see most often and want to optimize for
              speed.

        - Get all reservations within the last month/quarter (admin)
            - Search the reservations (indexed by hotel_id, date) and filter by date range.
        - Get all upcoming reservations (user)
            - Search the reservations (indexed by user_id) and filter by date. There may not be enough reservations for
              a given user to warrant using another column in the index.

    User Experience:
        - As contention may be a problem, we will likely want to use a lightweight protocol to send messages between the
          client and the hotel service. Websockets is a good way to establish a connection and send updates when
          reservation status changes.
        - Users can subscribe to a bunch of rooms that they're interested in and the time window. The server can detect
          whether or not availability exists within that time window, and if not, which days that room is not available.
            - {
                type: "subscribe",
                room_id: 12334,
                date_range: [2020-11-14, 2020-11-15, 2020-11-17],
            }
            - {
                room_id: 12334,
                availability: {
                    2020-11-14: True,
                    2020-11-15: False,
                    2020-11-17: True,
                }
            }
"""