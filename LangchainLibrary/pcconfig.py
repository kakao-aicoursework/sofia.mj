import pynecone as pc

class LangchainlibraryConfig(pc.Config):
    pass

config = LangchainlibraryConfig(
    app_name="LangchainLibrary",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)