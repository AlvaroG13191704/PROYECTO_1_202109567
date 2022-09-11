

# This class is who going to analyze the textArea
import re

from posixpath import split

from components.Tokens import L_Tokens


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

    def nextLine(self):
        _tmp = self.string_list[self.line] # pass the first line

        if _tmp == self.tmp_string: # if the temp is the same that the value store in tmp_string
            self.line += 1 # then read the next line
            self.tmp_string = "" # restart the _tmp
            self.col = 0 # restar col



    def Number(self, _string:str): # define the analyze of <Numero>4.50</Numero>
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
                return {'result':_number,'string':_string,'error':True}

        #return the string
        print(f'Número extraido -> {_number}')
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
        self.Number(new_string)


