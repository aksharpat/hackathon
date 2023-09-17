class ElectronicComponent:
    """
    Class that defines an electronic component.
    Name: Name of the component; C1, C2, etc.
    Type: Type of the component; R, C, L.
    """

    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
