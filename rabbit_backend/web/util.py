from rabbit_backend.settings import settings


def get_api_prefix() -> str:
    """Versioned API prefix using version from environment variables.

    Returns
    -------
    str
        API prefix
    """
    return f"/api/v{settings.api_version}"
