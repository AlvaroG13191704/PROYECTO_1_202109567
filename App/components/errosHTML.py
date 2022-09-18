


import os


def errorsHTML(list_e):
    graph = '''
digraph  ERRORES {
    node[shape=plaintext];
    
    tabla[label =< 
    <TABLE>
        <TR>
            <td>No.</td>
            <td>Lexema</td>
            <td>Tipo</td>
            <td>Columna</td>
            <td>Fila</td>
        </TR>
    '''
    for i in range(len(list_e)):
        object = list_e[i]
        dict = object.getError()
        sign = ""
        if dict['token'] == ">":
            sign = "&gt;"
        elif dict['token'] == "<":
            sign = "&lt;"
        else:
            sign = dict['token']

        err = f'''
        <TR>
            <TD>{i+1}</TD>
            <TD>{sign}</TD>
            <TD>{dict['description']}</TD>
            <TD>{dict['col']}</TD>
            <TD>{dict['row']}</TD>
        </TR>
        '''
        graph += err
    
    graph += '''
    </TABLE>
    >];
}
    '''
    # write the dot
    with open('helpers/table.txt','w') as file:
        file.write(graph)
    
    os.system('dot.exe -Tpng helpers/table.txt -o response/img/tableE.png')



    # Generate the HTML
    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROYECTO_1_LFP</title>
</head>
<body>
    <h1>Errores</h1>
    <img src="img/tableE.png">
</body>
    '''

    document = open('response/ERRORES_202109567.html','w')
    document.write(html)
    document.close()

