import uuid


def zero_uuid() -> uuid.UUID:
    """Get zero UUID.

    Returns
    -------
    uuid.UUID
        Zero UUID.
    """
    return uuid.UUID("00000000-0000-4000-8000-000000000000")
