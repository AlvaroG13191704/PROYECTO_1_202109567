


# This function received some parameters to build an HTML document 

def generateHTMLResult(list_r, list_s, title="Titulo",text=[]):
    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROYECTO_1_LFP</title>
</head>
<style>
    '''
    # styles
    for st in list_s:
        dict = st.getStyles()
        if dict['label'] == "Titulo":
            str = '''
            h1 {
                
            '''
            style = f'''
            color:{dict["color"]};
            font-size:{dict["size"]}px;
            '''
            str += f'''
            {style}
            '''
            str += '''
            }
            '''
            html += str
        elif dict['label'] == "Descripcion":
            str = '''
            h3 {
                
            '''
            style = f'''
            color:{dict["color"]};
            font-size:{dict["size"]}px;
            '''
            str += f'''
            {style}
            '''
            str += '''
            }
            '''
            html += str

        elif dict['label'] == "Contenido":
            str = '''
            p {
                
            '''
            style = f'''
            color:{dict["color"]};
            font-size:{dict["size"]}px;
            '''
            str += f'''
            {style}
            '''
            str += '''
            }
            '''
            html += str

    html += '''
</style>
    '''
    # modified text
    text_v = ""
    # list = text.pop(0)
    for i in text:
        print(i)
        text_v += f'{i} <br>'
    
    # title
    n_title = title.replace('Operaciones',' Operaciones ')
    html += f'''
<body>
    <h1>{n_title}</h1>
    <h3>{text_v}</h3>
    '''
    # Made the operations
    html_operations = """
    <div>
    """
    for op in list_r:
        if op.size == 3:
            dict = op.print_operation()
            if dict['sign'] == "sqr":
                operation = f'''
                <p>
                    {dict["text"]}: <br>
                    <br>
                    ({dict["n2"]})^(1/{dict["n1"]}) = {dict["result"]}
                </p>
                '''
            else:
                operation = f'''
                <p>
                    {dict["text"]}: <br>
                    <br>
                    {dict["n1"]} {dict["sign"]} {dict["n2"]} = {dict["result"]}
                </p>
                '''
            html_operations += operation

        elif op.size == 2:
            dict = op.print_operation()
            if dict['sign'] == "inv":
                operation = f'''
                <p>
                    {dict["text"]}: <br>
                    <br>
                    1/{dict["n"]} = {dict["result"]}
                </p>
                '''
            else:
                operation = f'''
                <p>
                    {dict["text"]}: <br>
                    <br>
                    {dict["sign"]}({dict["n"]})  = {dict["result"]}
                </p>
                '''
            html_operations += operation

        html_operations += """
    </div>
    """
    html += html_operations
    html += '''
</body>
    '''
    document = open('response/RESULTADOS_202109567.html','w')
    document.write(html)
    document.close()
