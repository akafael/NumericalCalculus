#!/usr/bin/env python
# -*- coding: utf-8 *-*

"""


@autor Diógenes
@autor Rafael Lima

"""
import pprint
import numpy
import os

def read_table():
    """
    Le a tabela de dados do arquivo table1.dat e a retorna na forma
    de uma matriz.
    """
    table = []

    # read data of table1.dat:
    for line in open('../data/table1.dat','r'):
        try:
            i, t_i, y_i = [n for n in line.split() if n]
            table.append([float(t_i), float(y_i)])
        except ValueError:
            pass
    
    return table


def get_size(matrix):
    """
    Retorna uma tupla com as dimensoes da matriz (linhas, colunas)
    """
    return len(matrix), len(matrix[0])


def new_matrix(rows, cols):
    """
    Cria uma nova matriz nula com as dimensoes especificadas.
    """
    return [ [0.0] * cols for i in range(rows) ]
    
    
def transpose(matrix):
    """
    Retorna a matriz transposta.
    """
    return [list(row) for row in zip(*matrix)] # Acho que não pode usar isso


def product(a, b):
    """
    Retorna a matriz produto.
    """
    a_rows, a_cols = get_size(a)
    b_rows, b_cols = get_size(b)
    
    if a_cols != b_rows:
        raise ValueError("Tamanhos incompativeis.")
    
    product = new_matrix(a_rows, b_cols)
    for i in range(a_rows):
        for j in range(b_cols):
            for k in range(a_cols):
                product[i][j] += a[i][k] * b[k][j]
    
    return product


def get_column(matrix, column):
    """
    Retorna a coluna da matriz.
    """
    return [[matrix[i][column]] for i in range(len(matrix))]

def solve_system(a, b):
    """
    Retorna uma matriz linha com a solucao do sistema.
    """
    try:
        r = numpy.linalg.solve(a, b)
    except:
        raise ValueError('Singular matrix')
    
    return [r[n,0] for n in range(r.size)]


def get_A(table, degree):
    """
    Retorna a matriz A do metodo de ajuste polinomial.
    """
    A = []
    for (t, _) in table:
        A.append([t**i for i in range(degree+1)])
    
    return A


def fit_polynomial(table, degree):
    """
    Encontra o melhor ajuste polinomial.
    """
    A = get_A(table, degree)
    A_t = transpose(A)
    Y = get_column(table, 1)
    coef = solve_system(product(A_t, A), product(A_t, Y))
    
    return coef

def interpolador(table):
    
    A = get_A(table, degree)
    Y = get_column(table, 1)
    coef = solve_system(A, Y)
    
    return coef

def print_matrix(matrix, format_str='%f'):
    """
    Imprime a matriz na tela de uma forma conveniente.
    """
    for row in matrix:
        for elem in row:
            print (format_str+' ') % elem,
        print ''


def to_str(coef, format_str='%+.2f'):
    """
    Retorna uma representacao em string do polinomio.
    """
    s = ''
    for i in reversed(range(1, len(coef))):
        s += (format_str + '*x**%d ') % (coef[i], i)
    return s + ' ' + format_str % coef[0]


def multiple_plot(polynomials, titles):
    u"""
    Chama o processo gnuplot para plotar um gráfico dos dados no vetor y
    versus os dados no vetor x.
    """
    
    command = 'set xrange [0.0:1.8]\n'
    for i, polynomial in enumerate(polynomials):
        command += 'f%d(x) = %s\n' % (i, to_str(polynomial))
        
    command += 'plot '
    command += ', '.join('f%d(x) title "%s"' % (i, titles[i]) for i in range(len(polynomials)))
    
    os.system("echo '%(command)s' | gnuplot -persist" % vars())
    
    
if __name__ == '__main__':
    table = read_table()
    polynomials = []
    titles = []
    
    for degree in (1, 3, 5, 10):
        coef = fit_polynomial(table, degree)
        polynomials.append(coef)
        titles.append('Grau %d' % degree)
        print 'Grau %d => ' % degree + to_str(coef)
    
    multiple_plot(polynomials, titles)
    
    interp = interpolador(table)
    print 'Interpolador => %s' % to_str(interp)
    
