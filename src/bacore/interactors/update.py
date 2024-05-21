
"""Set functionality module."""
import keyring
from bacore.domain import settings
from pydantic import SecretStr


def secret_from_keyring(key: settings.Keyring) -> SecretStr:
    if key.secret is not None:
        try:
            keyring.set_password(service_name=key.service_name, username=key.secret_name, password=key.secret.get_secret_value())
        except Exception as e:
            raise Exception("Unable to set secret") from e
    else:
        raise ValueError("Value must be provided for secret.")
    return key.secret

