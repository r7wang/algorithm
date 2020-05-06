"""
Build a class that has the two following methods:
    def add_user(...)
        Adds a user, by name.
            - Assume that there are no duplicate users by name.
    def suggest_matches()
        Finds as many possible matches as it can. A match is defined as a tuple of two different users.
        Constraints:
            - On any given call, a user can be matched with up to one other user.
            - A user cannot be matched with a user that they have already been matched with, in previous calls.
            - All matches must be generated randomly.

Notes:
    - Design the system to handle up to 1000 users.
"""
