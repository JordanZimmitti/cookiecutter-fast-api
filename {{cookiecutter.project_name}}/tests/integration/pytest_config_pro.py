from pytest import Config


class PytestConfigPro:

    def __init__(self, config: Config):
        """
        Class that adds extra functionality
        to the default pytest config

        :param config: the pytest config
        """
        self.config = config

    def get_cli_argument(self, argument_name: str, argument_default: str):
        """
        Function that gets a cli-argument. With this helper function when the cli returns
        'None' or 'Null' the default argument will be used

        :param argument_name: The name of the cli-argument to get
        :param argument_default: The default when the argument does not exist

        :return: The cli-argument
        """

        # Gets the cli argument
        argument = self.config.getoption(argument_name, default=argument_default)
        if argument is None or argument == "None" or argument == "NULL":
            return argument_default

        # Returns the cli argument
        return argument