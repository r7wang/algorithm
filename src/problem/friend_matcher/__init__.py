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
import random
from collections import defaultdict
from typing import List, Tuple


class FriendMatcher:
    """
    Strategy 1:
        - Pop random item from list to select every user, but cost is O(n) to select a user.
    """
    users = []
    history = defaultdict(set)

    def add_user(self, name: str) -> None:
        self.users.append(name)

    def suggest_matches(self) -> List[Tuple[str, str]]:
        matches = []
        remaining_users = list(self.users)
        while len(remaining_users) >= 2:
            # Get first user.
            user_a = remaining_users[0]

            # Generate potential matches.
            potential_matches = []
            for user_idx in range(1, len(remaining_users)):
                user_b = remaining_users[user_idx]
                if user_b in self.history[user_a]:
                    continue
                potential_matches.append(user_b)

            # Get second user.
            if len(potential_matches) == 0:
                remaining_users.remove(user_a)
                continue

            user_idx = random.randint(0, len(potential_matches) - 1)
            user_b = potential_matches[user_idx]

            # Add history.
            self.history[user_a].add(user_b)
            self.history[user_b].add(user_a)

            # Update remaining users.
            remaining_users.remove(user_a)
            remaining_users.remove(user_b)

            matches.append((user_a, user_b))
        return matches
