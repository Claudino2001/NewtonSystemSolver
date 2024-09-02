# controller/controller.py

from model.calc_newton import newton_method
from view.simplegui import criar_janela
import PySimpleGUI as sg
from sympy import symbols, sin, cos, exp

def main():
    # Cria a janela da GUI
    window = criar_janela()

    while True:
        event, values = window.read()

        # Atualiza a interface conforme o número de funções
        if event == '-NUM_FUNCOES-':
            if values['-NUM_FUNCOES-'] == '3':
                window['-FUNCAO3_TEXT-'].update(visible=True)
                window['-FUNCAO3-'].update(visible=True)
                window['-Z0_TEXT-'].update(visible=True)
                window['-Z0-'].update(visible=True)
            else:
                window['-FUNCAO3_TEXT-'].update(visible=False)
                window['-FUNCAO3-'].update(visible=False)
                window['-Z0_TEXT-'].update(visible=False)
                window['-Z0-'].update(visible=False)

        if event == sg.WIN_CLOSED:
            break

        if event == 'Calcular':
            # Pega os valores da GUI
            num_funcs = int(values['-NUM_FUNCOES-'])
            error_tolerance = float(values['-ERRO-'])
            initial_guess = [float(values['-X0-']), float(values['-Y0-'])]

            if num_funcs == 3:
                initial_guess.append(float(values['-Z0-']))
                vars = symbols('x y z')
            else:
                vars = symbols('x y')

            funcs = []
            funcs.append(eval(values['-FUNCAO1-'].replace('^', '**'), {"x": vars[0], "y": vars[1], "z": vars[2] if num_funcs == 3 else None, "sin": sin, "cos": cos, "exp": exp}))
            funcs.append(eval(values['-FUNCAO2-'].replace('^', '**'), {"x": vars[0], "y": vars[1], "z": vars[2] if num_funcs == 3 else None, "sin": sin, "cos": cos, "exp": exp}))
            if num_funcs == 3:
                funcs.append(eval(values['-FUNCAO3-'].replace('^', '**'), {"x": vars[0], "y": vars[1], "z": vars[2], "sin": sin, "cos": cos, "exp": exp}))

            # Chama o método de Newton
            result, iteration_count, abs_error_iteration, rel_error_iteration = newton_method(funcs, vars, initial_guess, error_tolerance)

            # Formata e mostra o resultado
            output = ""
            for var in vars:
                output += f'{var}: {result[var]}\n'
            output += f'Número total de iterações: {iteration_count}\n'
            output += f'Iteração onde o erro absoluto foi atingido: {abs_error_iteration}\n'
            output += f'Iteração onde o erro relativo foi atingido: {rel_error_iteration}\n'

            window['-RESULTADO-'].update(output)

    window.close()


if __name__ == "__main__":
    main()
