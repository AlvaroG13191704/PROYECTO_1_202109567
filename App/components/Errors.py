

# This class represent all the errors in the structure

class Lexical_Errors:

    #Constructor
    def __init__(self,_token, _row, _col, _descrip = "") -> None:
        self._token = _token
        self._row = _row
        self._col = _col
        self._descrip = _descrip

    def getError(self):
        return {'token':self._token, 'row': self._row, 'col': self._col , 'description': self._descrip}
