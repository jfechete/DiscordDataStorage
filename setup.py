from setuptools import setup

setup(
    name = "discord_data_storage",
    description = "Encrypted data storage with a format based on Discord",
    url = "https://github.com/jfechete/DiscordDataStorage",
    author = "jfechete",
    packages = ["discord_data_storage"],
    install_requires = [
        "cryptography"
    ]
)
