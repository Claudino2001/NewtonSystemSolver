import PySimpleGUI as sg


def criar_janela():
    layout = [
        [sg.Text('Número de funções (2 ou 3):')],
        [sg.Combo(['2', '3'], default_value='2', key='-NUM_FUNCOES-', enable_events=True)],
        [sg.Text('Erro tolerado (ex: 0.001):'), sg.InputText(key='-ERRO-')],
        [sg.Text('Chute inicial para x:'), sg.InputText(key='-X0-')],
        [sg.Text('Chute inicial para y:'), sg.InputText(key='-Y0-')],
        [sg.Text('Chute inicial para z:', key='-Z0_TEXT-', visible=False), sg.InputText(key='-Z0-', visible=False)],
        [sg.Text('Digite a função 1 (ex: 2+sin(x) ou x^2 ou exp(x)):'), sg.InputText(key='-FUNCAO1-')],
        [sg.Text('Digite a função 2 (ex: 2+sin(x) ou x^2 ou exp(x)):'), sg.InputText(key='-FUNCAO2-')],
        [sg.Text('Digite a função 3 (ex: 2+sin(z) ou z^2 ou exp(z)):', key='-FUNCAO3_TEXT-', visible=False),
         sg.InputText(key='-FUNCAO3-', visible=False)],
        [sg.Button('Calcular')],
        [sg.Text('Resultado:', size=(40, 1))],
        [sg.Multiline(size=(60, 10), key='-RESULTADO-', disabled=True)]
    ]

    window = sg.Window('Newton System Solver - v0.2', layout)
    return window
