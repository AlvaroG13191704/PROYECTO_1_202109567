

# This class is who going to analyze the textArea
import re

from posixpath import split
from components.errosHTML import errorsHTML
from components.resultsHTML import generateHTMLResult
from components.styles import Styles
from components.Operators import Double_Operations, Single_Operations
from components.Errors import Lexical_Errors

from components.Tokens import L_Tokens




class LexicalAnalyzer: 
    def __init__(self) -> None:
        self.string = "" # the character being read
        self.line = 0 # line being executed
        self.col = 0 # the column being read
        self.string_list = [] # save the values
        self.tmp_string = "" # temporary variable

        # global 
        self.global_list_errors = [] # to save global errrors
        self.global_list_operations = [] # to save the operations 
        self.global_list_styles = [] # save the styles
        self.dict_t_t = {} # dic to save title
    
    # Remove the character being read
    def remove(self, _string:str, _num:int):
        _tmp = "" 
        count = 0
        for i in _string:
            if count >= _num: # the number of character saved
                _tmp += i
            else:
                self.tmp_string += i
            count += 1

        return _tmp
    
    # Move to the next line
    def nextLine(self):
        _tmp = self.string_list[self.line] # pass the first line

        if _tmp == self.tmp_string: # if the temp is the same that the value store in tmp_string
            self.line += 1 # then read the next line
            self.tmp_string = "" # restart the _tmp
            self.col = 0 # restar col
    
    # verified which label is
    def isLabel(self, _string:str, _label:str):
        _tmp = "" # save all values
        count = 0
        for i in _string:
            if count < len(_label):
                _tmp += i
            count += 1
        # if the label is the same as _tmp return True instead False
        if _tmp == _label:
            return True
        else:
            return False

    # define the analyze of <Numero>4.50</Numero>
    def Number(self, _string:str): 
        _number = '' # the extraction of the number

        tokens = [
            L_Tokens.TK_MINOR.value, # <
            L_Tokens.TK_E_NUMBER.value, # Numero
            L_Tokens.TK_MAYOR.value, # >
            L_Tokens.TK_NUMBER.value, # 4.50 or any number
            L_Tokens.TK_MINOR.value, # <
            L_Tokens.TK_SLASH.value, # /
            L_Tokens.TK_E_NUMBER.value, # Numero
            L_Tokens.TK_MAYOR.value # >
        ]
        # compare the token with the string
        for i in tokens:
            try:
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column

                #Save the token -> next class

                if i == L_Tokens.TK_NUMBER.value: # get the number
                    _number += s.group()

                _string = self.remove(_string,s.end()) # .end the column end in the pattern

                # next line
                self.nextLine()
            except:
                # Save the error
                print('Ocurrio un Error')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':_number,'string':_string,'error':True}

        #return the string
        # print(f'Número extraido de la etiqueta <Numero> -> {_number}')
        return {'result':_number,'string':_string,'error':False}
          
    # Operator
    def Operator(self, _string : str):
        _number = ""
        _operator = None
        # to recognized the whole operator strucutre
        tokens = [
            L_Tokens.TK_MINOR.value,        # <
            L_Tokens.TK_E_OPERATOR.value,   # Operacion
            L_Tokens.TK_EQUAL.value,        # =
            "OPERADOR",                     # find which operator is
            L_Tokens.TK_MAYOR.value,        # >
            "NUMERO",                       # get the number
            "NUMERO",                       # get the second number 
            L_Tokens.TK_MINOR.value,        # <
            L_Tokens.TK_SLASH.value,        # /
            L_Tokens.TK_E_OPERATOR.value,   # Operacion
            L_Tokens.TK_MAYOR.value         # >
        ]

        # this part is the same as the first part, with some changes
        for i in tokens:
            try:
                
                if "NUMERO" == i: # if the token is an "Number"
                    if self.isLabel(_string, "<Numero>"):
                        _result = self.Number(_string)
                        _string = _result['string']

                        # get the number and their operator
                        _number += f'{_result["result"]} ' 

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendo NUMERO en OPERACIÓN')
                            return {'result':_number,'string':_string,'error':True}

                    elif self.isLabel(_string,"<Operacion="):
                        _result = self.Operator(_string)
                        _string = _result['string']

                        # rescued the value from the result of the operation
                        _number += f'{_result["result"]} ' 

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendo OPERACIÓN en OPERACIÓN ')
                            return {'result':_number,'string':_string,'error':True}

                    else:
                        _number += f'Unique ' 

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendo NUMERO en OPERACIÓN')
                            return {'result':_number,'string':_string,'error':True}

                else:
                     
                    if "OPERADOR" == i:
                        # this pattern is for sum
                        spatter = re.compile(f'^SUMA')
                        t = spatter.search(_string)
                        if t != None:
                            i = "SUMA"
                            _operator = L_Tokens.TK_O_SUM

                        # this pattern is for rest
                        spatter = re.compile(f'^RESTA')
                        t = spatter.search(_string)
                        if t != None:
                            i = "RESTA"
                            _operator = L_Tokens.TK_O_REST
                        
                        # Add the another operators
                        # this pattern is for multiplication
                        spatter = re.compile(f'^MULTIPLICACION')
                        t = spatter.search(_string)
                        if t != None:
                            i = "MULTIPLICACION"
                            _operator = L_Tokens.TK_O_MULT
                        
                        # this pattern is for divison
                        spatter = re.compile(f'^DIVISION')
                        t = spatter.search(_string)
                        if t != None:
                            i = "DIVISION"
                            _operator = L_Tokens.TK_O_DIV
                            
                        # this pattern is for power
                        spatter = re.compile(f'^POTENCIA')
                        t = spatter.search(_string)
                        if t != None:
                            i = "POTENCIA"
                            _operator = L_Tokens.TK_O_PO
                        
                        # this pattern is for sqr
                        spatter = re.compile(f'^RAIZ')
                        t = spatter.search(_string)
                        if t != None:
                            i = "RAIZ"
                            _operator = L_Tokens.TK_O_SQR
                        
                        # this pattern is for inv
                        spatter = re.compile(f'^INVERSO')
                        t = spatter.search(_string)
                        if t != None:
                            i = "INVERSO"
                            _operator = L_Tokens.TK_O_INV
                        
                        # this pattern is for SEN
                        spatter = re.compile(f'^SENO')
                        t = spatter.search(_string)
                        if t != None:
                            i = "SENO"
                            _operator = L_Tokens.TK_O_SEN
                        
                        # this pattern is for COS
                        spatter = re.compile(f'^COSENO')
                        t = spatter.search(_string)
                        if t != None:
                            i = "COSENO"
                            _operator = L_Tokens.TK_O_COS
                        
                        # this pattern is for TAN
                        spatter = re.compile(f'^TANGENTE')
                        t = spatter.search(_string)
                        if t != None:
                            i = "TANGENTE"
                            _operator = L_Tokens.TK_O_TAN
                        
                        # this pattern is for MOD
                        spatter = re.compile(f'^MOD')
                        t = spatter.search(_string)
                        if t != None:
                            i = "MOD"
                            _operator = L_Tokens.TK_O_MOD

                        if _operator == None:
                             # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error BUSCANDO DIFERENTES OPERADORES')
                            return {'result':_number,'string':_string,'error':True}


                    # build our pattern "^" recognize the first element
                    pattern = re.compile(f'^{i}')

                    s = pattern.search(_string) # search if the patterns compile with the first character

                    print(f'| {self.line} | {self.col} | {s.group()}')

                    self.col += int(s.end()) # get the column

                    #Save the token -> next class

                    if i == L_Tokens.TK_NUMBER.value: # get the number
                        _number += s.group()

                    _string = self.remove(_string,s.end()) # .end the column end in the pattern

                # next line
                self.nextLine()
            except:
                # save the error
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                print('Ocurrio un error')
                return {'result':_number,'string':_string,'error':True}


        # Number1 Operation Number2
        # make the operation
        value = _number.rstrip()

        if _operator.value == "SUMA":
            complete = value.replace(" ", " + ")

        elif _operator.value == "RESTA":
            complete = value.replace(" ", " - ")
        
        elif _operator.value == "MULTIPLICACION":
            complete = value.replace(" ", " * ")
        
        elif _operator.value == "DIVISION":
            complete = value.replace(" ", " / ")
        
        elif _operator.value == "POTENCIA":
            complete = value.replace(" ", " ** ")
        
        elif _operator.value == "MOD":
            complete = value.replace(" ", " mod ")
        
        elif _operator.value == "RAIZ":
            complete = value.replace(" ", " sqr ")

        elif _operator.value == "INVERSO":
            complete = value.replace("Unique", "inv")
        
        elif _operator.value == "SENO":
            complete = value.replace("Unique", "sen")
        
        elif _operator.value == "COSENO":
            complete = value.replace("Unique", "cos")
        
        elif _operator.value == "TANGENTE":
            complete = value.replace("Unique", "tan")

        
        list_numbers = complete.split(" ")
        print(f'{list_numbers}  -> tamaño {len(list_numbers)}')
        # print(f'{_operations} -> Operacion compleja')
        result = None
        if len(list_numbers) == 3:
            operation = Double_Operations(list_numbers[0],list_numbers[1],list_numbers[2])
            self.global_list_operations.append(operation)
            result = operation.print_operation()

        elif len(list_numbers) == 2:
            if list_numbers[1] == 'sqr' or list_numbers[1] == 'inv' or list_numbers[1] == 'sen' or list_numbers[1] == 'sen' or list_numbers[1] == 'cos' or list_numbers[1] == 'tan':
                operation = Single_Operations(list_numbers[0],list_numbers[1])
                self.global_list_operations.append(operation)
                result = operation.print_operation()
            else:
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                print('Ocurrio un error NO SE ACEPTAN MÁS NUMEROS EN OPERACIONES SIMPES')
                return {'result':_number,'string':_string,'error':True}
        else:
            e = Lexical_Errors(i,self.line,self.col,"Error")
            self.global_list_errors.append(e)
            print('Ocurrio un error LEYENDO LISTA DE OPERACIONE')
            return {'result':_number,'string':_string,'error':True}
        
        # print(f'Números obtenidos en operación -> {_number}')
        return {'result':result['result'],'operators':list_numbers,'string':_string,'error':False}

    # The last part -> the Type
    def Type(self,_string: str):
        _number = ""
        # Tokens as the other methods
        tokens = [
            L_Tokens.TK_MINOR.value,        # <
            L_Tokens.TK_TYPE.value,         # Tipo
            L_Tokens.TK_MAYOR.value,        # >
            "OPERACIONES",                  # Operaciones
            L_Tokens.TK_MINOR.value,        # <
            L_Tokens.TK_SLASH.value,        # /
            L_Tokens.TK_TYPE.value,         # Tipo
            L_Tokens.TK_MAYOR.value         # >
        ]
        for i in tokens:
            try:
                if "OPERACIONES" == i:
                    exit = True
                    while exit:
                        print("------------------------")
                        _result = self.Operator(_string)
                        _string = _result['string']

                        if _result['error']:
                            # Save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendo OPERACION EN TIPO')
                            exit = False

                        if self.isLabel(_string,"</Tipo>"):
                            exit = False
                            
                else:
                    # build our pattern "^" recognize the first element
                    pattern = re.compile(f'^{i}')

                    s = pattern.search(_string) # search if the patterns compile with the first character

                    print(f'| {self.line} | {self.col} | {s.group()}')

                    self.col += int(s.end()) # get the column

                    #Save the token -> next class

                    _string = self.remove(_string,s.end()) # .end the column end in the pattern

                # next line
                self.nextLine()
                
            except:
                # save the error
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                print('Ocurrio un error en <Tipo>')
                return {'result':_number,'string':_string,'error':True}
        
        return {'result':_number,'string':_string,'error':False}

    # Read <Text>
    def Text(self, _string: str):
        _text = ""
        # our tokens
        tokens = [
            L_Tokens.TK_MINOR.value,  # < 
            L_Tokens.TK_E_TEXT.value, # Text
            L_Tokens.TK_MAYOR.value,  # >
            L_Tokens.TK_TEXT.value,   # [A-Za-z0-9_ .,]*
            L_Tokens.TK_MINOR.value,  # <
            L_Tokens.TK_SLASH.value,  # /
            L_Tokens.TK_E_TEXT.value, # Tipo
            L_Tokens.TK_MAYOR.value   # >
        ]
        for i in tokens:
            try:
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column

                #Save the token -> next class

                if i == L_Tokens.TK_TEXT.value: # get the number
                    _text += s.group()

                _string = self.remove(_string,s.end()) # .end the column end in the pattern

                # next line
                self.nextLine()
            except:
                # Save the error
                print('Ocurrio un Error leyendo texto')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':_text,'string':_string,'error':True}

        return {'result':_text,'string':_string,'error':False}

    def Title(self, _string: str):
        _color = None
        _size = None
        # our tokens
        tokens = [
            L_Tokens.TK_MINOR.value,        # < 
            L_Tokens.TK_E_TITLE.value,      # Titulo
            L_Tokens.TK_E_COLOR.value,      # Color
            L_Tokens.TK_EQUAL.value,        # =
            "COLOR",
            L_Tokens.Tk_E_SIZE.value,       # Tamanio
            L_Tokens.TK_EQUAL.value,        # =
            L_Tokens.TK_STYLE_NUMBER.value, # Numero
            L_Tokens.TK_SLASH.value,        # /
            L_Tokens.TK_MAYOR.value         # >
        ]
        for i in tokens:
            try:
                if "COLOR" == i:
                    # this pattern is for red
                    spatter = re.compile(f'^ROJO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "ROJO"
                        _color = L_Tokens.TK_RED
                    
                    # this pattern is for blue
                    spatter = re.compile(f'^AZUL')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AZUL"
                        _color = L_Tokens.TK_BLUE
                    
                    # this pattern is for yellow
                    spatter = re.compile(f'^AMARILLO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AMARILLO"
                        _color = L_Tokens.TK_YELLOW
                    
                    # this pattern is for green
                    spatter = re.compile(f'^VERDE')
                    t = spatter.search(_string)
                    if t != None:
                        i = "VERDE"
                        _color = L_Tokens.TK_GREEN
                    
                    # this pattern is for Orange
                    spatter = re.compile(f'^NARANJA')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NARANJA"
                        _color = L_Tokens.TK_ORANGE
                    
                    # this pattern is for pruple
                    spatter = re.compile(f'^MORADO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "MORADO"
                        _color = L_Tokens.TK_PURPLE

                    # this pattern is for pruple
                    spatter = re.compile(f'^NEGRO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NEGRO"
                        _color = L_Tokens.TK_BLACK

                    if _color == None:
                        # Save the error
                        print('Ocurrio un Error en seleccionar color')
                        # Instance an object error
                        e = Lexical_Errors(i,self.line,self.col,"Error")
                        self.global_list_errors.append(e)
                        return {'string':_string,'error':True}
                
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column
                # Save the color type ! 
                if i == L_Tokens.TK_STYLE_NUMBER.value:
                    _size = int(s.group())

                _string = self.remove(_string,s.end()) # .end the column end in the pattern
                # next line
                self.nextLine()

            except:
                # Save the error
                print('Ocurrio un Error leyendo texto')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':'Estilo','string':_string,'error':True}

        # create an object
        style = Styles('Titulo',_color.value,_size)
        print(style.getStyles())
        self.global_list_styles.append(style)
        return {'result':'Estilos','string':_string,'error':False}
    
    def Description(self, _string: str):
        _title = ""
        _color = None
        _size = None
        # our tokens
        tokens = [
            L_Tokens.TK_MINOR.value,        # < 
            L_Tokens.TK_E_DESCRIPTION.value,      # Descripcion
            L_Tokens.TK_E_COLOR.value,      # Color
            L_Tokens.TK_EQUAL.value,        # =
            "COLOR",
            L_Tokens.Tk_E_SIZE.value,       # Tamanio
            L_Tokens.TK_EQUAL.value,        # =
            L_Tokens.TK_STYLE_NUMBER.value, # Numero
            L_Tokens.TK_SLASH.value,        # /
            L_Tokens.TK_MAYOR.value         # >
        ]
        for i in tokens:
            try:
                if "COLOR" == i:
                    # this pattern is for red
                    spatter = re.compile(f'^ROJO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "ROJO"
                        _color = L_Tokens.TK_RED
                    
                    # this pattern is for blue
                    spatter = re.compile(f'^AZUL')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AZUL"
                        _color = L_Tokens.TK_BLUE
                    
                    # this pattern is for yellow
                    spatter = re.compile(f'^AMARILLO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AMARILLO"
                        _color = L_Tokens.TK_YELLOW
                    
                    # this pattern is for green
                    spatter = re.compile(f'^VERDE')
                    t = spatter.search(_string)
                    if t != None:
                        i = "VERDE"
                        _color = L_Tokens.TK_GREEN
                    
                    # this pattern is for Orange
                    spatter = re.compile(f'^NARANJA')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NARANJA"
                        _color = L_Tokens.TK_ORANGE
                    
                    # this pattern is for pruple
                    spatter = re.compile(f'^MORADO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "MORADO"
                        _color = L_Tokens.TK_PURPLE

                    # this pattern is for pruple
                    spatter = re.compile(f'^NEGRO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NEGRO"
                        _color = L_Tokens.TK_BLACK

                    if _color == None:
                        # Save the error
                        print('Ocurrio un Error en seleccionar color')
                        # Instance an object error
                        e = Lexical_Errors(i,self.line,self.col,"Error")
                        self.global_list_errors.append(e)
                        return {'string':_string,'error':True}
                
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column
                # Save the color type ! 
                if i == L_Tokens.TK_STYLE_NUMBER.value:
                    _size = int(s.group())

                _string = self.remove(_string,s.end()) # .end the column end in the pattern
                # next line
                self.nextLine()

            except:
                # Save the error
                print('Ocurrio un Error leyendo texto')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':_title,'string':_string,'error':True}
        # save the style
        style = Styles('Descripcion',_color.value,_size)
        print(style.getStyles())
        self.global_list_styles.append(style)
        return {'result':_title,'string':_string,'error':False}

    def Content(self, _string: str):
        _title = ""
        _color = None
        _size = None
        # our tokens
        tokens = [
            L_Tokens.TK_MINOR.value,        # < 
            L_Tokens.TK_E_CONTENT.value,      # Contenido
            L_Tokens.TK_E_COLOR.value,      # Color
            L_Tokens.TK_EQUAL.value,        # =
            "COLOR",
            L_Tokens.Tk_E_SIZE.value,       # Tamanio
            L_Tokens.TK_EQUAL.value,        # =
            L_Tokens.TK_STYLE_NUMBER.value, # Numero
            L_Tokens.TK_SLASH.value,        # /
            L_Tokens.TK_MAYOR.value         # >
        ]
        for i in tokens:
            try:
                if "COLOR" == i:
                    # this pattern is for red
                    spatter = re.compile(f'^ROJO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "ROJO"
                        _color = L_Tokens.TK_RED
                    
                    # this pattern is for blue
                    spatter = re.compile(f'^AZUL')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AZUL"
                        _color = L_Tokens.TK_BLUE
                    
                    # this pattern is for yellow
                    spatter = re.compile(f'^AMARILLO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "AMARILLO"
                        _color = L_Tokens.TK_YELLOW
                    
                    # this pattern is for green
                    spatter = re.compile(f'^VERDE')
                    t = spatter.search(_string)
                    if t != None:
                        i = "VERDE"
                        _color = L_Tokens.TK_GREEN
                    
                    # this pattern is for Orange
                    spatter = re.compile(f'^NARANJA')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NARANJA"
                        _color = L_Tokens.TK_ORANGE
                    
                    # this pattern is for pruple
                    spatter = re.compile(f'^MORADO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "MORADO"
                        _color = L_Tokens.TK_PURPLE

                    # this pattern is for pruple
                    spatter = re.compile(f'^NEGRO')
                    t = spatter.search(_string)
                    if t != None:
                        i = "NEGRO"
                        _color = L_Tokens.TK_BLACK

                    if _color == None:
                        # Save the error
                        print('Ocurrio un Error en seleccionar color')
                        # Instance an object error
                        e = Lexical_Errors(i,self.line,self.col,"Error")
                        self.global_list_errors.append(e)
                        return {'string':_string,'error':True}
                
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column
                # Save the color type ! 
                if i == L_Tokens.TK_STYLE_NUMBER.value:
                    _size = int(s.group()) 

                _string = self.remove(_string,s.end()) # .end the column end in the pattern
                # next line
                self.nextLine()

            except:
                # Save the error
                print('Ocurrio un Error leyendo texto')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':_title,'string':_string,'error':True}

        # save the style
        style = Styles('Contenido',_color.value,_size)
        print(style.getStyles())
        self.global_list_styles.append(style)
        
        return {'result':_title,'string':_string,'error':False}
    
    # read <Funcion=ESCRIBIR>
    def Function(self, _string: str):
        _title = ""
        # Our tokens
        tokens = [
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_E_FUN.value,            # Funcion
            L_Tokens.TK_EQUAL.value,            # =
            L_Tokens.TK_E_WRITE.value,          # ESCRIBIR
            L_Tokens.TK_MAYOR.value,            # >
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_E_TITLE.value,          # Titulo
            L_Tokens.TK_MAYOR.value,            # >
            L_Tokens.TK_TITLE.value,            # [A-Za-z0-9_ .,]*
            L_Tokens.TK_MINOR.value,            # <
            L_Tokens.TK_SLASH.value,            # /
            L_Tokens.TK_E_TITLE.value,          # Titulo
            L_Tokens.TK_MAYOR.value,            # >
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_E_DESCRIPTION.value,    # Descripcion
            L_Tokens.TK_MAYOR.value,
            L_Tokens.TK_KEY_LEFT.value,         # [
            L_Tokens.TK_U_TEXT.value,           # TEXTO
            L_Tokens.TK_KEY_RIGHT.value,        # ]
            L_Tokens.TK_MINOR.value,            # <
            L_Tokens.TK_SLASH.value,            # /
            L_Tokens.TK_E_DESCRIPTION.value,    # Description
            L_Tokens.TK_MAYOR.value,            # >  
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_E_CONTENT.value,        # Contenido
            L_Tokens.TK_MAYOR.value,            # >
            L_Tokens.TK_KEY_LEFT.value,         # [
            L_Tokens.TK_U_TYPE.value,           # TIPO
            L_Tokens.TK_KEY_RIGHT.value,        # ]
            L_Tokens.TK_MINOR.value,            # <
            L_Tokens.TK_SLASH.value,            # /
            L_Tokens.TK_E_CONTENT.value,        # Contenido
            L_Tokens.TK_MAYOR.value,             # >
            L_Tokens.TK_MINOR.value,             # <
            L_Tokens.TK_SLASH.value,             # /
            L_Tokens.TK_E_FUN.value,             # Funcion
            L_Tokens.TK_MAYOR.value              # >
        ]
        
        for i in tokens:
            try:
                # build our pattern "^" recognize the first element
                pattern = re.compile(f'^{i}')

                s = pattern.search(_string) # search if the patterns compile with the first character

                print(f'| {self.line} | {self.col} | {s.group()}')

                self.col += int(s.end()) # get the column
                
                if i == L_Tokens.TK_TITLE.value: # get the texts
                    _title += s.group()
                    self.dict_t_t['title'] = f"{_title} "
                #Save the token -> next class
                _string = self.remove(_string,s.end()) # .end the column end in the pattern

                # next line
                self.nextLine()

            except:
                # Save the error
                print(f'Ocurrio un Error leyendo funcion -> {i}')
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                return {'result':"",'string':_string,'error':True}

        return {'result':_title,'string':_string,'error':False}
    
    #read <Estilo>
    def Style(self, _string: str):
        style = ""
        tokens = [
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_E_STYLE.value,          # Estilo
            L_Tokens.TK_MAYOR.value,            # >
            "TITULO",
            "DESCRIPCION",
            "CONTENIDO",
            L_Tokens.TK_MINOR.value,            # < 
            L_Tokens.TK_SLASH.value,                  # /
            L_Tokens.TK_E_STYLE.value,          # Estilo
            L_Tokens.TK_MAYOR.value,            # >
        ]

        # this part is the same as the first part, with some changes
        for i in tokens:
            try:
                if "TITULO" == i: 
                    if self.isLabel(_string, "<Titulo"):
                        _result = self.Title(_string)
                        _string = _result['string']

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}
                    else:

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}

                elif "DESCRIPCION" == i: 
                    if self.isLabel(_string, "<Descripcion"):
                        _result = self.Description(_string)
                        _string = _result['string']

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}
                    else:

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}

                elif "CONTENIDO" == i: 
                    if self.isLabel(_string, "<Contenido"):
                        _result = self.Content(_string)
                        _string = _result['string']

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}
                    else:

                        if _result['error']:
                            # save the error
                            e = Lexical_Errors(i,self.line,self.col,"Error")
                            self.global_list_errors.append(e)
                            print('Ocurrio un error leyendoo titulo en estilos')
                            return {'result':style,'string':_string,'error':True}
                else:
                    # build our pattern "^" recognize the first element
                    pattern = re.compile(f'^{i}')

                    s = pattern.search(_string) # search if the patterns compile with the first character

                    print(f'| {self.line} | {self.col} | {s.group()}')

                    self.col += int(s.end()) # get the column

                    #Save the style 

                    _string = self.remove(_string,s.end()) # .end the column end in the pattern

                    # next line
                    self.nextLine()
            except:
                # save the error
                # Instance an object error
                e = Lexical_Errors(i,self.line,self.col,"Error")
                self.global_list_errors.append(e)
                print(f'Ocurrio un error  -> {i}')
                return {'result':style,'string':_string,'error':True}

        return {'result':style,'string':_string,'error':False}

    # Method to extact the info 
    def compile(self,value):
        # from the text area should be
        content = value.split('\n')

        # Clean the empty values and "\n"
        new_string = ""
        string_list = []
        # take the text from <Texto>
        text_list = []
        for t in range(len(content)):
            if content[t] == "<Texto>":
                c = 0
                while content[t+c] != "</Texto>":
                    text_list.append(content[t+c])
                    c += 1

        # using replace
        for i in content:
            i = i.replace(' ', '') # replace empty values
            i = i.replace('\n','') # replace jump lines
            if i != '': # verified if ins't empty lines
                new_string += i
                string_list.append(i)

        # identify when we makee a new line change
        self.string_list = string_list
        print(self.Type(new_string))
        # #call the Type method
        # result_of_Type = self.Type(new_string)

        # # Pass resulto to Text
        # result_of_fun = self.Text(result_of_Type['string'])

        # result_of_styles = self.Function(result_of_fun['string'])

        # print(self.Style(result_of_styles['string']))

        # if self.dict_t_t != {}:
        #     # generate a HTML results
        #     print(self.dict_t_t)
        #     generateHTMLResult(self.global_list_operations,self.global_list_styles,self.dict_t_t['title'],text_list)
        #     # generate the erros
        #     errorsHTML(self.global_list_errors)
        # else:
        #     # generate a HTML results
        #     generateHTMLResult(self.global_list_operations,self.global_list_styles,'Titulo Error',text_list)
        #     # generate the erros
        #     errorsHTML(self.global_list_errors)
    


