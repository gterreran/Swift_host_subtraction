class FilterError(Exception):
    def __init__(self):
        super().__init__('No filter recognized.')
    
class ListError(Exception):
    def __init__(self,file):
        super().__init__('No usable file found in {}.'.format(file))
        
class FileNotFound(Exception):
    def __init__(self):
        super().__init__('Cannot interpret input file.')
