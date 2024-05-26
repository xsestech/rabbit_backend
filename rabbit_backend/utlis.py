import uuid


def zero_uuid() -> uuid.UUID:
    """Get zero UUID.

    Returns
    -------
    uuid.UUID
        Zero UUID.
    """
    return uuid.UUID(int=0)
