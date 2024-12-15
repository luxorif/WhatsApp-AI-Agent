def extract_latest_message(messages, role, user_message_time=None):
    """
    Retrieve the latest message from a specific role (e.g., "assistant").
    Optionally filter by timestamp.
    """
    return next(
        (msg.content[0].text.value for msg in reversed(messages.data)
         if msg.role == role and (not user_message_time or msg.created_at > user_message_time)),
        None
    )