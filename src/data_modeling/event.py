"""
One way to model data is to see things as events, where events encapsulate the information associated with the event.

Modeling an options exercise:
    - Resource: OptionGrant (id, owner_id, issuer_corporation_id, vesting_schedule_id, num_approvers_required)
    - Event: ExerciseRequest (id, exerciser_id, grant_id, timestamp, quantity, price)
    - Event: ExerciseApproval (id, approver_id, exercise_request_id, timestamp)

What is a completed exercise?
    - One where, an ExerciseRequest event is associated with as many approvers as is required for the grant.

Problems:
    - Additional complexity for objects that are frequently modified because modifying an "event" that happened some
      time ago has implications.
    - ExerciseModification (id, exercise_request_id, quantity)
    - ExerciseCancellation (id, exercise_request_id)

Advantages:
    - Great for auditing!

Strategies:
    - Compaction, if needed (very specific use cases)
"""
