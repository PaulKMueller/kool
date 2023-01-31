import enum

class ENDPOINT(enum.Enum):
    KEYBERT = "/ask_keybert/"
    XLNET = "/ask_xlnet/"
    BLOOM = "/ask_bloom/"
    GALACTICA = "/ask_galactica/"
    GPT_NEO = "/ask_gpt_neo/"

    @classmethod
    def get_endpoint(cls, name):
        for endpoint in cls:
            if endpoint.name == name.upper():
                return endpoint.value
        return None