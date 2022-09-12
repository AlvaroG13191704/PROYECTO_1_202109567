# Tokens

from enum import Enum

# Token to validate an HTML structure

class L_Tokens(Enum):
    # general tokens
    TK_MINOR = "<"
    TK_MAYOR = ">"
    TK_SLASH = "/"
    TK_EQUAL = "="
    # first read the deep end <Numero> 4.5 </Numero>
    TK_E_NUMBER = "Numero"
    TK_NUMBER = "[0-9]*[.]?[0-9]+"
    # second read the operator
    TK_E_OPERATOR = "Operacion"
    TK_O_SUM = "SUMA"
    TK_O_REST = "RESTA"
    TK_O_MULT = "MULTIPLICACION"
    TK_O_DIV = "DIVISON"
    TK_O_PO = "POTENCIA"
    TK_O_SQR = "RAIZ"
    TK_O_INV = "INVERSO"
    TK_O_SEN = "SENO"
    TK_O_COS = "COSENO"
    TK_O_TAN = "TANGENTE"
    TK_O_MOD = "MOD"
    # Third read the type
    TK_TYPE = "Tipo"