import os
import copy
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

HOME_DIR = os.path.expanduser("~")

class DataAccessor:
    def __init__(self, key,
        user_template=None, member_template=None,
        server_template=None, bot_template=None,
        storage_location = "DiscordDataStorage"):
        self._key = key
        self._fernet = Fernet(self._key)
        self._user_template = user_template
        self._member_template = member_template
        self._server_template = server_template
        self._bot_template = bot_template
        self._storage_location = os.path.join(HOME_DIR,storage_location)
        if not os.path.isdir(self._storage_location):
            os.makedirs(self._storage_location)

    def read(self, server_id = "", user_id = ""):
        template = self._get_template(server_id != "", user_id != "")
        if template == None and not self._file_exists(server_id, user_id):
            raise FileNotFoundError("No data file found")

        if not self._file_exists(server_id, user_id):
            data = copy.deepcopy(template)
        else:
            data = json.loads(self._read_file(server_id, user_id))
            if isinstance(data, dict) and isinstance(template, dict):
                DataAccessor._apply_template(data, template)
        return data

    def write(self, data, server_id = "", user_id = ""):
        self._write_file(json.dumps(data), server_id, user_id)

    def _read_file(self, server_id = "", user_id = ""):
        with open(self._get_file_path(server_id, user_id), "r") as data_file:
            data = data_file.read()
        return self._decrypt(data)

    def _write_file(self, data, server_id = "", user_id = ""):
        data = self._encrypt(data)
        with open(self._get_file_path(server_id, user_id), "w") as data_file:
            data = data_file.write(data)

    def _file_exists(self,  server_id = "", user_id = ""):
        return os.path.isfile(self._get_file_path(server_id, user_id))

    def _get_template(self, is_server, is_user):
        if not is_server and not is_user:
            return self._bot_template
        elif not is_server:
            return self._user_template
        elif not is_user:
            return self._server_template
        else:
            return self._member_template

    def _get_file_path(self, server_id = "", user_id = ""):
        return os.path.join(
            self._storage_location,
            self._get_file_name(server_id, user_id)
        )

    def _get_file_name(self, server_id = "", user_id = ""):
        base_file_name = "{}:{}".format(server_id, user_id)
        return self._get_user_hash(base_file_name)

    def _encrypt(self, value):
        return self._fernet.encrypt(value.encode()).decode()

    def _decrypt(self, encrypted_value):
        return self._fernet.decrypt(encrypted_value.encode()).decode()

    def _get_user_hash(self, value):
        kdf = Scrypt(salt=self._key, length=32, n=2**14, r=8, p=1)
        return kdf.derive(value.encode()).hex()

    @staticmethod
    def _apply_template(value, template):
        for key in template:
            if key not in value:
                value[key] = copy.deepcopy(template[key])
            elif isinstance(value[key], dict):
                DataAccessor._apply_template(value[key], template[key])
