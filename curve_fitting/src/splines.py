#!/usr/bin/env python
# -*- coding: utf-8 *-*

import sys
import unittest
import os

from utilities import(
        get_size,
        new_matrix,
        transpose,
        product,
        add_and_multiply,
        get_column,
        solve_system,
        print_matrix,
        to_str
)

def read_table():
    """
    Le a tabela de dados do arquivo table1.dat e a retorna na forma
    de uma matriz.
    """
    table = []
    datafile = open('../data/table1.dat','r')
    
    # read data of table1.dat:
    for line in datafile:
        try:
            i, t_i, y_i = [n for n in line.split() if n]
            table.append([float(t_i), float(y_i)])
        except ValueError:
            pass
    
    datafile.close()

    return table

def get_D_system(coef):
    """
    Retorna as matrizes A e B do sistema que resolve A * D = B.
    """
    n, _ = get_size(coef)
    coef = [row[0] for row in coef]
    
    a = [[2.0, 1.0] + [0.0]*(n-2)]
    b = [[3.0*(coef[1]-coef[0])]]
    
    for i in range(0, n-2):
        a.append([0.0]*i + [1.0, 4.0, 1.0] + [0.0]*(n-i-3))
        b.append([3.0*(coef[i+2]-coef[i])])
    
    a.append([0.0]*(n-2) + [1.0, 2.0])
    b.append([3.0*(coef[-1] - coef[-2])])
    
    return a, b
    

def get_coef(d_list, w, i):
    """
    Retorna os 4 coeficientes (d, c, b, a) da spline cúbica i:
    a * s^3 + b * s^2 + c * s + d
    
    d_list => derivadas na coordenada w
    w => valores na coordenada w
    """
    a = d_list[i+1] + d_list[i] - 2.0 * w[i+1] + 2.0 * w[i]
    b = -d_list[i+1] - 2.0 * d_list[i] + 3.0 * w[i+1] - 3.0 * w[i]
    c = d_list[i]
    d = w[i]
    
    return [a,b,c,d]


def adjust_splines(table, column):
    """
    Obtém uma lista dos coeficientes das splines cúbicas ajustadas
    à coordenada column na tabela.
    [(d0, c0, b0, a0), (d1, c1, b1, a1), ...]
    """
    data = get_column(table, column)
    a, b = get_D_system(data)
    n, _ = get_size(table)
    D = solve_system(a, b)
    
    return [get_coef(D, transpose(data)[0], i) for i in range(n-1)]
    


def plot_parametric(y_splines, t_splines, s_range=(0.0, 1.0)):
    """
    Plota 
    """
    
    command = ''
    #command = 'set parametric\n'
    #command += 'set trange[%f:%f]\n' % s_range
    
    #for y_spline, t_spline in zip(y_splines, t_splines):
        #command += 'plot %s, %s\n' % (to_str(t_spline, var='t'), to_str(y_spline, var='t'))
    
    #command += 'set noparametric\n'
    command += 'plot \"../data/table1.dat\" u 2:3 t \"Dados\"\n'
    os.system("echo '%s' | gnuplot -persist" % command)
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        unittest.main()
    else:
        table = read_table()
        _, cols = get_size(table)
        
        t = adjust_splines(table, 0)
        y = adjust_splines(table, 1)
        
        print t, y
        plot_parametric(y, t)
