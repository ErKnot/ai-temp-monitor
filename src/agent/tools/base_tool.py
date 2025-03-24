from abc import ABC, abstractmethod



class Tool(ABC):
    """
    Abstract base class for defining tools.

    This class serves as a blueprint for creating tools. In particular subclasses are
    required to implement  the methods `name` and `description`.
    Implementing these methods ensures that each tool has a name,
    a description when created, which will be necessary for the orchestrator.

    Abstract Methods:
        name (str): Returns the name of the tool.
        description (str): Provides a description of the tool's functionality.
        use: Executes the tool's primary action with the given arguments.
    """
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def use(self, *args, **kwargs):
        pass


