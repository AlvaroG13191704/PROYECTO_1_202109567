

import math


class  Double_Operations:
    def __init__(self,n1, sign , n2) -> None:
        
        self.n1 = float(n1)
        self.sign = sign
        self.n2 = float(n2)
    
    def print_operation(self):
        # print each operation
        if self.sign == "+":
            result = self.n1 + self.n2
            return {'result':str(result),'text':'Operación Suma','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
        
        elif self.sign == "-":
            result = self.n1 - self.n2
            return {'result':str(result),'text':'Operación resta','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}

        elif self.sign == "*":
            result = self.n1 * self.n2
            return {'result':str(result),'text':'Operación multiplicacion','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
        
        elif self.sign == "/":
            try:
                result = self.n1 / self.n2
                return {'result':str(result),'text':'Operación división','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
            except ZeroDivisionError :
                return {'result':'No se puede efectuar la división','text':'Operación multiplicacion','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}

        elif self.sign == "**":
            result = self.n1 ** self.n2
            return {'result':str(result),'text':'Operación potencia','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
        
        elif self.sign == "mod":
            result = self.n1 % self.n2
            return {'result':str(result),'text':'Operación mod','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}

class Single_Operations:
    def __init__(self, n, sign) -> None:
        
        self.n = float(n)
        self.sign = sign
    
    def print_operation(self):
        # return an dict from an operation
        if self.sign == 'sqr':
            result = math.sqrt(self.n)
            return {'result':str(result), 'text': 'Operación raiz', 'sign': self.sign, 'n':str(self.n)}
        
        elif self.sign == 'inv':
            result = 1/self.n
            return {'result':str(result), 'text': 'Operación inverso', 'sign': '1/', 'n':str(self.n)}
        
        elif self.sign == 'inv':
            result = 1/self.n
            return {'result':str(result), 'text': 'Operación inverso', 'sign': '1/', 'n':str(self.n)}
        
        elif self.sign == 'sen':
            result = math.sin(self.n)
            return {'result':str(result), 'text': 'Operación seno', 'sign': self.sign, 'n':str(self.n)}

        elif self.sign == 'cos':
            result = math.cos(self.n)
            return {'result':str(result), 'text': 'Operación coseno', 'sign': self.sign, 'n':str(self.n)}
        
        elif self.sign == 'tan':
            result = math.tan(self.n)
            return {'result':str(result), 'text': 'Operación tangente', 'sign': self.sign, 'n':str(self.n)}
        