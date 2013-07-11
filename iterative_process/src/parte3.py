#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import subprocess


def tolist(func):
    u'''
    Decorador para transformar uma função geradora em uma função
    que retorna uma lista.
    '''
    def inner(*args, **kwargs):
        return list(func(*args, **kwargs))
    return inner

try:
    #raise ImportError
    from mpmath import mpf, mp, sqrt, exp, linspace, pi, fabs
    
    # Precisão em decimais
    mp.dps = 20

    
except ImportError:
    # Caso não consiga importar a biblioteca, faça com float's normais
    import math
    from math import exp, fabs, pi
    
    def mpf(n):
        return float(n)
        
    def sqrt(n):
        return math.sqrt(n) if n >= 0.0 else math.sqrt(-n)*1j
    
    @tolist
    def linspace(a, b, n):
        a, b = mpf(a), mpf(b)
        n = int(n)
        inc = (b-a) / (n-1)
        
        v = a
        for i in range(n):
            yield v
            v += inc


def my_plot(data_x=[], data_y=[], title='', xlabel='', ylabel='', plot_title='', filename='', print_line=True):
    u'''
    Chama o processo gnuplot para plotar um gráfico dos dados no vetor y
    versus os dados no vetor x.
    '''
    if isinstance(data_x, str):
        data_x = [mpf(n) for n in data_x.split(',')]
    if isinstance(data_y, str):
        data_y = [mpf(n) for n in data_y.split(',')]
    
    if True:
        handler, data_file = tempfile.mkstemp()
        fp = open(data_file, 'w')
        for (x, y) in zip(data_x, data_y):
                fp.write('%f\t%f\n' % (x, y))
        fp.close()
        
        if print_line:
            command = '''
            
set style line 1 lc rgb "blue" lt 1 lw 2 pt 7 pi -1 ps 0.5
'''
        else:
            command = '''
            
set style points pc rgb "blue" pt 7 pi -1 ps 0.5
'''
            
        command += '''

set title "%(title)s"
set xlabel "%(xlabel)s"
set ylabel "%(ylabel)s"
set grid

set pointintervalbox 1

plot "%(data_file)s" title "%(plot_title)s" with linespoints ls 1
        ''' % vars()
        
        command = command.encode('utf-8')
        os.system("echo '%(command)s' | gnuplot -persist" % vars())
        
        if filename:
            # Agora salvando num arquivo PNG
            command = '''
set term png
set output "%(filename)s"''' % vars() + command
            os.system("echo '%(command)s' | gnuplot" % vars())
        
        os.remove(data_file)


def multiple_plot(data_x=[], data_y=[], title='', xlabel='', ylabel='', plot_titles=[], filename=''):
    u'''
    Chama o processo gnuplot para plotar um gráfico dos dados no vetor y
    versus os dados no vetor x.
    '''
    
    handler, data_file = (1, 'saida.txt')
    
    command = '''

set title "%(title)s"
set xlabel "%(xlabel)s"
set ylabel "%(ylabel)s"
set grid
set key right bottom
set style line 1 lc rgb "blue" lt 1 lw 2 pt 7 pi -1 ps 0.5
set pointintervalbox 1

plot ''' % vars()
    
    
    for i in range(len(data_y)):
        command += (' "%s" using 1:%d title "%s" with linespoints ls 1 lc %d' %
                        (data_file, i+2, plot_titles[i], i+1) )
        if i != len(data_y)-1:
            command += ', '
    
    fp = open(data_file, 'w')
    
    for i in range(len(data_x)):
        line_nums = [data_x[i]]
        for vec_y in data_y:
            line_nums.append(vec_y[i])
    
        s = ''
        for n in line_nums:
            s += '%f ' % n
        s += '\n'
        fp.write(s)
        
    command = command.encode('utf-8')
    fp.close()
    
    os.system("echo '%(command)s' | gnuplot -persist" % vars())
    
    if filename:
        # Agora salvando num arquivo PNG
        command = '''
set term png
set output "%(filename)s"''' % vars() + command
        os.system("echo '%(command)s' | gnuplot" % vars())
    

    
        
def iter_proc(x, l=0.33):
    return l * x * (1.0-x)
    
def ponto_fixo(func, x0):
    x0 = float(x0)
    x = func(x0)
    
    while fabs(x0 - x) > 0.000000001:
        x0 = x
        x = func(x0)
    
    return x

def questao2a():
    data_lambda = linspace(0.01, 2.99, 100)
    data_x = [ponto_fixo(lambda x: iter_proc(x, l), 0.1) for l in data_lambda]
    
    my_plot(data_lambda, data_x,
            xlabel='Lambda',
            ylabel='Ponto fixo x*',
            title='Lambda versus Ponto fixo',
            filename='questao2a.png')


def gerar_questao2b(lambdas, filename, n_iter=50):
    x_axis = range(n_iter)
    y_axes = []
    
    plot_titles = ['lambda = %.1f' % l for l in lambdas]
    
    for l in lambdas:
        y_axis = []
        x0 = 0.1
        for n in range(n_iter):
            y_axis.append(x0)
            x0 = iter_proc(x0, l)
        
        y_axes.append(y_axis)
    
    multiple_plot(x_axis, y_axes, plot_titles=plot_titles, filename=filename)


def questao2b():
    gerar_questao2b((0.1, 0.5, 1.0, 2.0, 2.5, 2.9), 'questao2b1.png')
    gerar_questao2b((3.0, 3.25, 3.75), 'questao2b2.png', n_iter=25)
    gerar_questao2b((4.0, 4.5, 4.75, 5), 'questao2b3.png', n_iter=5)


def achar_ponto_fixo(l, n_iter=50):
    l = float(l)
    x0 = 0.1
    vec = []
    fixos = []
    
    for n in range(n_iter):
        for val in vec:
            if fabs(val - x0) < 0.0000001:
                for fixo in fixos:
                    if fabs(fixo - x0) < 0.0000001:
                        return fixos
                else:
                    fixos.append(x0)
                
        vec.append(x0)
        x0 = iter_proc(x0, l)
    
    return None

def achar_ponto_fixo2(l, n_iter=50):
    l = float(l)
    x0 = 0.1
    vec = []
    
    for n in range(n_iter):
        for i, v in enumerate(vec):
            if v == x0:
                return (n-i)
        else:
            vec.append(x0)
        
        x0 = iter_proc(x0, l)
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'NENHUMA FUNCAO'
        sys.exit(1)
    
    kwargs = {}
    args = []
    for arg in sys.argv[2:]:
        key, sep, val = arg.partition('=')
        if val:
            kwargs[key] = val
        else:
            args.append(arg)
    
    result = vars()[sys.argv[1]](*args, **kwargs)
    if result: print result
    
