#!/usr/bin/env python
# -*- coding: utf-8 *-*

import pprint
import numpy
import os
import sys

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
        raise ValueError("Dimensoes incompativeis: %s e %s" % (get_size(a), get_size(b)))
    
    product = new_matrix(a_rows, b_cols)
    for i in range(a_rows):
        for j in range(b_cols):
            for k in range(a_cols):
                product[i][j] += a[i][k] * b[k][j]
    
    return product

def add_and_multiply(a, b, factor=1.0):
    if get_size(a) != get_size(b):
        raise ValueError("Dimensoes incompativeis: %s e %s" % (get_size(a), get_size(b)))
    
    rows, cols = get_size(a)
    r = new_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            r[i][j] = a[i][j] + factor * b[i][j]
    
    return r

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

def to_str(coef, format_str='%+.2f'):
    """
    Retorna uma representacao em string do polinomio.
    """
    s = ''
    for i in reversed(range(1, len(coef))):
        s += (format_str + '*x**%d ') % (coef[i], i)
    return s + ' ' + format_str % coef[0]

def print_matrix(matrix, format_str='%f'):
    """
    Imprime a matriz na tela de uma forma conveniente.
    """
    for row in matrix:
        for elem in row:
            print (format_str+' ') % elem,
        print ''
