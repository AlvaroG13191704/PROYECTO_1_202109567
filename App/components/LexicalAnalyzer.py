

# This class is who going to analyze the textArea
import re

from posixpath import split
from components.Errors import Lexical_Errors

from components.Tokens import L_Tokens


# global 
global_list_errors = []

class LexicalAnalyzer: 
    def __init__(self) -> None:
        self.string = "" # the character being read
        self.line = 0 # line being executed
        self.col = 0 # the column being read
        self.string_list = [] # save the values
        self.tmp_string = "" # temporary variable
    
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
                global_list_errors.append(e)
                return {'result':_number,'string':_string,'error':True}

        #return the string
        print(f'Número extraido -> {_number}')
        return {'result':_number,'string':_string,'error':False}
        
    # verified which label is
    def isLabel(self, _string:str, _label:str):
        _tmp = "" # save all values
        count = 0
        for i in _string:
            if count < len(_label):
                _tmp += i
            count += 1
        
        if _tmp == _label:
            return True
        else:
            return False

    # Operator
    def Operator(self, _string : str):
        _number = ""
        _operator = None
        # to recognized the whole operator strucutre
        tokens = [
            L_Tokens.TK_MINOR.value,        # <
            L_Tokens.TK_E_OPERATOR.value,   # Operacion
            L_Tokens.TK_EQUAL.value,        # =
            "OPERADOR",                         # find which operator is
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
                if "NUMERO" == i:
                    if self.isLabel(_string, "<Numero>"):
                        _result = self.Number(_string)
                        _string = _result['string']
                        if _result['error']:
                            # save the error
                            print('Ocurrio un error')
                            return {'result':_number,'string':_string,'error':True}

                    elif self.isLabel(_string,"<Operacion="):
                        _result = self.Operator(_string)
                        _string = _result['string']
                        if _result['error']:
                            # save the error
                            print('Ocurrio un error')
                            return {'result':_number,'string':_string,'error':True}

                    else:
                        print('Ocurrio un error')
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

                        if _operator == None:
                             # save the error
                            print('Ocurrio un error en operacion')
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
                print('Ocurrio un error')
                return {'result':_number,'string':_string,'error':True}

        #make the operation
        return {'result':_number,'string':_string,'error':False}

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
                            print('Ocurrio un error en Tipo')
                        if self.isLabel(_string,"</Tipo>"):
                            exit = False
                            # return {'result':_number,'string':_string,'error':True}
                else:
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
                print('Ocurrio un error en tipo')
                return {'result':_number,'string':_string,'error':True}
        
        #make the operation
        return {'result':_number,'string':_string,'error':False}
        
    # Method to extact the info 
    def compile(self,value):
        # from the text area should be
        content = value.split('\n')

        # Clean the empty values and "\n"
        new_string = ""
        string_list = []
        # using replace 
        for i in content:
            i = i.replace(' ', '') # replace empty values
            i = i.replace('\n','') # replace jump lines
            if i != '': # verified if ins't empty lines
                new_string += i
                string_list.append(i)

        print(new_string)
        print(string_list)
        # identify when we makee a new line change
        self.string_list = string_list
        
        #call the Number method
        print(self.Type(new_string))


