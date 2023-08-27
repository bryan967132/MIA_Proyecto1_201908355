import os

class Execute:
    def __init__(self, path: str = None):
        self.path = path
        if self.path:
            self.path = self.path.replace('"', '')
        else:
            self.path = path

    def exec(self, parser):
        if not self.path:
            print(' ->  Error execute: No se especificó la ruta del script:')
            return
        absolutePath = os.path.abspath(self.path)
        if not os.path.exists(absolutePath):
            print(' ->  Error execute: No existe el script en la ruta especificada.')
            return
        input = open(self.path, encoding='utf-8').read()
        parser.parse(input)

    def __str__(self) -> str:
        return 'Execute'