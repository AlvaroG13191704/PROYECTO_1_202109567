

class Styles:
    def __init__(self, label, color, size ) -> None:
        self.label = label
        self.color = color
        self.size = size
    
    def getStyles(self):
        color = None
        if self.color == 'ROJO':
            color = 'red'
        elif self.color == 'AZUL':
            color = 'blue'
        elif self.color == 'AMARILLO':
            color = 'yellow'
        elif self.color == 'VERDE':
            color = 'green'
        elif self.color == 'NARANJA':
            color = 'orange'
        elif self.color == 'MORADO':
            color = 'purple'
        elif self.color == 'NEGRO':
            color = 'black'
        else:
            color = 'black'
        return {'label':self.label, 'color': color, 'size':self.size}