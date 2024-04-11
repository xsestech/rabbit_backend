from rabbit_backend.settings import settings


def get_api_prefix() -> str:
    """Return versioned API prefix using version from environment variables."""
    return f"/api/v{settings.api_version}"
