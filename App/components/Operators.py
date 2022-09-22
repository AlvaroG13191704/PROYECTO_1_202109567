

import math


class  Double_Operations:
    def __init__(self,n1, sign , n2) -> None:
        
        self.n1 = float(n1)
        self.sign = sign
        self.n2 = float(n2)
        self.size = 3
    
    def print_operation(self):
        # print each operation
        if self.sign == "+":
            result = self.n1 + self.n2
            return {'result':str(result),'text':'Operacion Suma','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
        
        elif self.sign == "-":
            result = self.n1 - self.n2
            return {'result':str(result),'text':'Operacion resta','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}

        elif self.sign == "*":
            result = self.n1 * self.n2
            return {'result':str(result),'text':'Operacion multiplicacion','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
        
        elif self.sign == "/":
            try:
                result = self.n1 / self.n2
                return {'result':str(result),'text':'Operacion division','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}
            except ZeroDivisionError :
                return {'result':'No se puede efectuar la división','text':'Operación division','sign':self.sign,'n1': str(self.n1),'n2': str(self.n2)}

        elif self.sign == "**":
            result = self.n2 ** self.n1
            return {'result':str(result),'text':'Operacion potencia','sign':self.sign,'n1': str(self.n2),'n2': str(self.n1)}
        
        elif self.sign == "mod":
            result = self.n1 % self.n2
            return {'result':str(result),'text':'Operacion mod','sign':'%','n1': str(self.n1),'n2': str(self.n2)}

        elif self.sign == 'sqr':
            result = (self.n2)**(1/self.n1)
            return {'result':str(result), 'text': 'Operacion raiz', 'sign': self.sign, 'n1': str(self.n1),'n2': str(self.n2)}

class Single_Operations:
    def __init__(self, n, sign) -> None:
        
        self.n = float(n)
        self.sign = sign
        self.size = 2
    
    def print_operation(self):
        # return an dict from an operation
        if self.sign == 'inv':
            result = 1/self.n
            return {'result':str(result), 'text': 'Operacion inverso', 'sign': '1/', 'n':str(self.n)}
            
        elif self.sign == 'sen':
            result_n = self.n*(math.pi/180)
            result = math.sin(result_n)
            return {'result':str(result), 'text': 'Operacion seno', 'sign': self.sign, 'n':str(self.n)}

        elif self.sign == 'cos':
            result_n = self.n*(math.pi/180)
            result = math.cos(result_n)
            return {'result':str(result), 'text': 'Operacion coseno', 'sign': self.sign, 'n':str(self.n)}
        
        elif self.sign == 'tan':
            result_n = self.n*(math.pi/180)
            result = math.tan(result_n)
            return {'result':str(result), 'text': 'Operacion tangente', 'sign': self.sign, 'n':str(self.n)}
        