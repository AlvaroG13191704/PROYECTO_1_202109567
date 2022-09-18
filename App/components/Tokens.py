# Tokens

from enum import Enum

# Token to validate an HTML structure

class L_Tokens(Enum):
    # general tokens
    TK_MINOR = "<"
    TK_MAYOR = ">"
    TK_SLASH = "/"
    TK_EQUAL = "="
    TK_KEY_LEFT = "\["
    TK_KEY_RIGHT = "\]"
    # first read the deep end <Numero> 4.5 </Numero>
    TK_E_NUMBER = "Numero"
    TK_NUMBER = "[0-9]*[.]?[0-9]+"
    # second read the operator
    TK_E_OPERATOR = "Operacion"
    TK_O_SUM = "SUMA"
    TK_O_REST = "RESTA"
    TK_O_MULT = "MULTIPLICACION"
    TK_O_DIV = "DIVISION"
    TK_O_PO = "POTENCIA"
    TK_O_SQR = "RAIZ"
    TK_O_INV = "INVERSO"
    TK_O_SEN = "SENO"
    TK_O_COS = "COSENO"
    TK_O_TAN = "TANGENTE"
    TK_O_MOD = "MOD"
    # Third read the type
    TK_TYPE = "Tipo"
    # Fourth read 
    TK_E_TEXT = "Texto"
    TK_TEXT = "[A-Za-z0-9_ .,]*"
    # Fifth raed
    TK_E_FUN = "Funcion"
    TK_E_WRITE = "ESCRIBIR"
    TK_E_TITLE = "Titulo"
    TK_TITLE =  "[A-Za-z0-9_ .,]*"
    TK_E_DESCRIPTION = "Descripcion"
    TK_E_CONTENT = "Contenido"
    TK_U_TEXT = "TEXTO"
    TK_U_TYPE = "TIPO"
    # Sixth read
    TK_E_STYLE = "Estilo"
    TK_E_COLOR = "Color"
    Tk_E_SIZE = "Tamanio"
    TK_STYLE_NUMBER = "[0-9]*"
    # Colors
    TK_RED = "ROJO"
    TK_BLUE = "AZUL"
    TK_YELLOW = "AMARILLO"
    TK_GREEN = "VERDE"
    TK_ORANGE = "NARANJA"
    TK_PURPLE = "MORADO"
    TK_BLACK = "NEGRO"

    