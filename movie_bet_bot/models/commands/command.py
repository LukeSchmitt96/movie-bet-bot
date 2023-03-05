class Command:
    # the name of the command
    name: str
    # the description of the command
    description: str
    # the function that is called when the command is executed
    function: any
    # the constructor for the Command class
    def __init__(
        # the instance of the Command class it
        self,
        # the name of the command
        name,
        # the description of the command
        description,
        # the function that is called when the command is executed
        function
    ) -> None:
        # set the name of the command
        self.name = name
        # set the description of the command
        self.description = description
        # set the function that is called when the command is executed
        self.function = function
