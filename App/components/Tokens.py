# Tokens

from enum import Enum

# Token to validate an HTML structure

class L_Tokens(Enum):
    # general tokens
    TK_MINOR = "<"
    TK_MAYOR = ">"
    TK_SLASH = "/"
    # first read the deep end <Numero> 4.5 </Numero>
    TK_E_NUMBER = "Numero"
    TK_NUMBER = "[0-9]*[.]?[0-9]+"