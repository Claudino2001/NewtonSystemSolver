# ========================================================
#  Title:          Calculadora de Sistemas Não Lineares - Newton
#  Description:    Método de Newton para sistemas
#  Author:         Gabriel Claudino
#  Created on:     27/08/2024
#  Last updated:   28/08/2024
#  Version:        0.2
#  Python Version: 3.12.3
#  GitHub:         Claudino2001
# ========================================================
#  DESCRIÇÃO DO CÓDIGO:
#  1. Perguntar o número de funções (duas ou tres)
#  2. Irá solicitar o erro:
#        Entrada esperada: 0,001, 0,1, 0,0001, 0,00000001
#  3. Pergutar o chute inicial para o usuário:
#        Para o caso de duas funções será solicitado dois numeros (chute_x e chute_y);
#        Para o caso de tres funções será solicitado tres numeros(chute_x, chute_y e chute_z).
#        Exemplo de chutes que serão inseridas: 0,5, 1/2, 1000, 0, 1, 10
#  4. Então o usuário irá fornecer as funções (funcao_1 e funcao_2 ou funcao_1, funcao_2 e funcao_3)
#        Exemplo das funções que serão inseridas: 2+SEN(x), (-x+y-COS(z)), (2*x-x-COS(y))
#  5. Proximo passo é substituir o chute nas funções E montar o vetor com esse resultado.
#        Exemplo:
#            funcao_1 = 2+SEN(x)
#            chute_x = 1
#            Cria-se um vetor para F(x) onde F[0] tera a resultado de 2+SEN(1)
#            E assim para todos.
#  6. Criar uma matriz Jacobiana J(x). Ou seja pegar cada função e derivar em relação a x y e z.
#        Montando assim uma matriz.
#  7. Achar a inversa dessa matriz Jacobiana.
#  8. Uma vez com a matriz jacobiana J(x)^{-1} foi encontrada o proximo passo é encontrar o DeltaX.
#        O DeltaX é  resultado da multiplicação das duas matrizes.
#        São elas: (J(x)^{-1}) * (-F(x)). (Importante notar que é -F(x)).
#  9. Uma vez encontrado a matriz DeltaX que representa o resultado de x y e z.
#        O chutes agora passam a assumir o valor do chute anterior + os valores de deltax.
#        o chute_x por exemplo seria: chute_x + DeltaX na primeira posição.
#  10. Agora _todo o processo se repete novamente a partir da 5 etapa.
#        O loop so devera parar quando a o erro for menor ou igual ao ERRO absoluto e o erro relativo.
#        Ou seja mostrar quantas interação do loop foram necessárias para se chegar no erro esperado.
#        Erro relativo = Ultimo_Valor_do_chute - penultimo_Valor_do_chute/Ultimo_Valor_do_chute
#        Erro absoluto = Ultimo_Valor_do_chute - penultimo_Valor_do_chute
#  ===============================================================

import numpy as np
from sympy import symbols, diff, sin, cos, exp


def jacobian_matrix(funcs, vars):
    J = np.zeros((len(funcs), len(vars)), dtype=object)
    for i, func in enumerate(funcs):
        for j, var in enumerate(vars):
            J[i, j] = diff(func, var)
    return J


def evaluate_funcs_at(funcs, values):
    results = []
    for func in funcs:
        result = func.subs(values)
        results.append(float(result))  # Avaliação numérica
    return np.array(results)


def newton_method(funcs, vars, initial_guess, error_tolerance):
    values = {var: val for var, val in zip(vars, initial_guess)}
    iteration_count = 0
    prev_values = None

    abs_error_iteration = None
    rel_error_iteration = None

    while True:
        iteration_count += 1

        # Etapa 5: Avaliar funções
        F_x = evaluate_funcs_at(funcs, values)

        # Etapa 6: Criar matriz Jacobiana
        J_x = jacobian_matrix(funcs, vars)
        J_x_num = np.array([[float(J_ij.subs(values)) for J_ij in J_row] for J_row in J_x])  # Avaliação numérica
        J_x_inv = np.linalg.inv(J_x_num)

        # Etapa 8: Encontrar DeltaX
        delta_x = -np.dot(J_x_inv, F_x)

        # Atualizar chutes
        new_values = {var: val + delta for (var, val), delta in zip(values.items(), delta_x)}

        # Verificação de erro
        if prev_values:
            absolute_errors = [abs(new_values[var] - prev_values[var]) for var in vars]
            relative_errors = [abs(new_values[var] - prev_values[var]) / abs(new_values[var]) for var in vars]

            max_abs_error = max(absolute_errors)
            max_rel_error = max(relative_errors)

            # Registro da iteração onde os erros são satisfeitos pela primeira vez
            if abs_error_iteration is None and max_abs_error <= error_tolerance:
                abs_error_iteration = iteration_count
            if rel_error_iteration is None and max_rel_error <= error_tolerance:
                rel_error_iteration = iteration_count
        else:
            max_abs_error = float('inf')
            max_rel_error = float('inf')

        if max_abs_error <= error_tolerance and max_rel_error <= error_tolerance:
            break

        prev_values = values
        values = new_values

    return values, iteration_count, abs_error_iteration, rel_error_iteration


def main():
    # Step 1: Perguntar número de funções
    num_funcs = int(input("Número de funções (2 ou 3): "))

    # Step 2: Solicitar erro tolerado
    error_tolerance = float(input("Erro tolerado (ex: 0.001): "))

    # Step 3: Solicitar chute inicial
    if num_funcs == 2:
        initial_guess = [float(input("Chute inicial para x: ")), float(input("Chute inicial para y: "))]
        vars = symbols('x y')
    elif num_funcs == 3:
        initial_guess = [float(input("Chute inicial para x: ")), float(input("Chute inicial para y: ")),
                         float(input("Chute inicial para z: "))]
        vars = symbols('x y z')
    else:
        print("Número de funções deve ser 2 ou 3")
        return

    # Step 4: Solicitar funções do usuário
    funcs = []
    for i in range(num_funcs):
        func_str = input(f"Digite a função {i + 1} (ex: 2+sin(x) ou x^2 ou exp(x): ")
        func_str = func_str.replace('^', '**')  # Substitui ^ por **
        # Incluindo exp no dicionário de funções permitidas
        func = eval(func_str, {"x": vars[0], "y": vars[1], "z": vars[2] if num_funcs == 3 else None, "sin": sin, "cos": cos, "exp": exp})
        funcs.append(func)

    # Step 5-10: Método de Newton
    result, iteration_count, abs_error_iteration, rel_error_iteration = newton_method(funcs, vars, initial_guess, error_tolerance)

    # Exibir resultado final
    for var in vars:
        print(f'{var}: {result[var]}')
    print(f'Número total de iterações: {iteration_count}')
    print(f'Iteração onde o erro absoluto foi atingido: {abs_error_iteration}')
    print(f'Iteração onde o erro relativo foi atingido: {rel_error_iteration}')


if __name__ == "__main__":
    main()
