from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class DataAccessor:
    def __init__(self, key,
        user_template=None, member_template=None,
        server_template=None, bot_template=None):
        self._key = key
        self._fernet = Fernet(self._key)
        self._user_template = user_template
        self._member_template = member_template
        self._server_template = server_template
        self._bot_template = bot_template

    def _encrypt(self, value):
        return self._fernet.encrypt(value.encode()).decode()
    
    def _decrypt(self, encrypted_value):
        return self._fernet.decrypt(encrypted_value.encode()).decode()

    def _get_user_hash(self, value):
        kdf = Scrypt(salt=self._key, length=32, n=2**14, r=8, p=1)
        return kdf.derive(value.encode()).hex()
