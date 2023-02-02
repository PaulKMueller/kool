import enum


class ENDPOINT(enum.Enum):
    """Enum for getting the endpoint for the models
    """
    KEYBERT = "/ask_keybert/"
    XLNET = "/ask_xlnet/"
    BLOOM = "/ask_bloom/"
    GALACTICA = "/ask_galactica/"
    GPT_NEO = "/ask_gpt_neo/"

    @classmethod
    def get_endpoint(cls, name):
        """Gets the endpoint for model

        Args:
            name: name of model

        Returns:
            endpoint
        """
        for endpoint in cls:
            if endpoint.name == name.upper():
                return endpoint.value
        return None
