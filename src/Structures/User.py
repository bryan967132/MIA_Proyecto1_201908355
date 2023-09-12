class User:
    def __init__(self, id: str = None, group: str = None, name: str = None, password: str = None):
        self.id: str = id
        self.group: str = group
        self.name: str = name
        self.password: str = password

    def __str__(self) -> str:
        return f'User({self.id}, {self.group}, {self.name}, {self.password})'