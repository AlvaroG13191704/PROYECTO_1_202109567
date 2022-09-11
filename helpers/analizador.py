# Ejemplo de un analizador 

# esta libreria hace una estructura clave valor 
from enum import Enum
import re


class L_tokens(Enum):
    TK_MENOR = '<'
    TK_E_NUMERO = 'Numero'
    TK_MAYOR = '>'
    TK_NUMERO = '[0-9]*'
    TK_INV_SLASH = '/'
    TK_E_OPERACION  = 'Operacion'
    TK_IGUAL = '='
    TK_SUMA = 'SUMA'
    TK_RESTA = 'RESTA'

class Analizador: 
    def __init__(self) -> None:
        self.cadena = ""
        self.linea = 0
        self.col = 0
        self.lista_cadena = []
        self.tmp_cadena = ""



    def quitar(self, _cadena : str, _num : int):
        _tmp = ""
        count = 0
        for i in _cadena:
            if count >= _num:
                _tmp += i
            else: 
                self.tmp_cadena += i
            count += 1

        return _tmp

    def aumentarLinea(self):
        _tmp = self.lista_cadena[self.linea]

        if _tmp == self.tmp_cadena: 
            self.linea += 1
            self.tmp_cadena = ""
            self.col = 0

    def Numero(self, _cadena : str):
        tokens = [
            L_tokens.TK_MENOR.value, # <
            L_tokens.TK_E_NUMERO.value, # Numero 
            L_tokens.TK_MAYOR.value, # >
            L_tokens.TK_NUMERO.value, # int
            L_tokens.TK_MENOR.value, # <
            L_tokens.TK_INV_SLASH.value, # /
            L_tokens.TK_E_NUMERO.value, # Numero 
            L_tokens.TK_MAYOR.value # >
        ]
        #esta variable será la extracción 
        _numero = ""
        for i in tokens: 
            try: 
                patron = re.compile(f'^{i}')
                s = patron.search(_cadena)
                print(f'| {self.linea} | {self.col} | {s.group()}')
                self.col += int(s.end()) #Sumar columna
                # Guardar el token

                if i == L_tokens.TK_NUMERO.value: 
                    _numero += s.group()
                _cadena = self.quitar(_cadena, s.end())

                self.aumentarLinea() # Leer nueva linea 
            except:
                # Guardar error
                print('Ocurrio un error')
                return {'resultado': _numero, 'Cadena':_cadena, 'Error':True}

        return {'resultado': _numero, 'Cadena':_cadena, 'Error':False}


    def Operador(self, _cadena : str):
        tokens = [
            L_tokens.TK_MENOR.value,        # <
            L_tokens.TK_E_OPERACION.value,  # Operacion 
            L_tokens.TK_IGUAL.value,        # =
            "OPERACION",                    # OPERADOR
            L_tokens.TK_MAYOR.value,        # >
            "NUMERO",                       # NUMERO
            "NUMERO",                       # NUMERO
            L_tokens.TK_MENOR.value,        # <
            L_tokens.TK_INV_SLASH.value,    # /
            L_tokens.TK_E_OPERACION.value,  # Operacion 
            L_tokens.TK_MAYOR.value         # >
        ]
        


    def compile(self):
        # Leer el archivo de entrada
        archivo = open('helpers/entrada.txt','r')
        contenido = archivo.readlines()
        archivo.close()

        #print(contenido)

        # Limpiar entrada
        nueva_cadena = ""
        lista_cadena = []

        

        for i in contenido:
            # Replace, cambiar lo que haya en una string
            i = i.replace(' ','') # Quitando espacios
            i = i.replace('\n','') # Quitando espacios de linea
            if i != '':
                nueva_cadena += i 
                lista_cadena.append(i)
        
        # print(nueva_cadena)
        # print(lista_cadena)
        self.lista_cadena = lista_cadena
        self.Numero(nueva_cadena)



Analizador().compile()