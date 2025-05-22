

class Singleton:
    """
    A implementation of Singleton pattern.
    This class ensures that only one instance of the class is created.
    """

    __instance : 'Singleton' = None

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class if it doesn't exist, otherwise return the existing instance.
        """
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance
