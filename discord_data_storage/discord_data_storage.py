class DataAccessor:
    def __init__(self, key,
        user_template = None, member_template = None,
        server_template = None, bot_template = None):
        self._key = key
        self._user_template = user_template
        self._member_template = member_template
        self._server_template = server_template
        self._bot_template = bot_template
