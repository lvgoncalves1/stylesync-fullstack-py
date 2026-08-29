from wsgiref.simple_server import make_server

def aplicacao_web(environ, start_response):
    produtos = [
        {'nome': 'Notebook', 'valor': 3000},
        {'nome': 'Celular', 'valor': 1000},
        {'nome': 'Relogio', 'valor': 800},
        {'nome': 'Teclado', 'valor': 200}
    ]

    linhas_html = ''
    for produto in produtos:
        linhas_html += f'<li>{produto['nome']} - R$ {produto['valor']}</li>'

    start_response('200 Ok', [('Content-Type', 'text/html;charset=utf-8')])

    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    html_final = html.replace('{{PRODUTOS}}', linhas_html)
    return [html_final.encode('utf-8')]

make_server('', 5000, aplicacao_web).serve_forever()