"""
Another way to model data is to make it a state machine.

Modeling an options exercise:
    - Object: OptionExercise (id, exerciser_id, status)

Problems:
    - This approach tends to explode the model size because for every state that it needs to handle, there may be
      information associated with that state. You're likely to say, "I want to be able to figure out everything related
      to this object just be reading this object".
    - For instance, if the status is APPROVED, how do we see the approvers? We can link them directly (on the model) or
      indirectly (through foreign keys).
    - The state may be out of sync with reality. If this is linked through foreign keys and I go and add an approval in
      a separate table, what does setting it to UNAPPROVED mean?
    - To sync, you will definitely need a multi-table transaction.

Advantages:
    - Easier to query for state.

"""