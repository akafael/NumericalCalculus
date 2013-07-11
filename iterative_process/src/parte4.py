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
        
    
erf_coef =  (1.0,
             0.0705230784,
             0.0422820123,
             0.0092705272,
             0.0001520143,
             0.0002765672,
             0.0000430638)
u'''
Coeficientes para o cálculo da aproximação da função erro.
'''

def soma(z):
    u'''
    Função auxiliar para o cálculo da função erro.
    '''
    a = erf_coef
    
    return mpf(1) + z*a[1] + (z**2)*a[2] + (z**3)*a[3] + (z**4)*a[4] + (z**5)*a[5] + (z**6)*a[6]
    

def erfc(z):
    u'''
    Definição da função erro
    '''
    z = mpf(z)
    return soma(z) ** (-16)


def erfc_z(z):
    u'''
    Definição da derivada da função erro
    '''
    z = mpf(z)
    return (exp(-z**2) * (-2) / sqrt(pi))


def temp(t, x=mpf(1), Q=mpf(1), A=mpf(1), Ti=mpf(10)):
    u'''
    Definição da função temperatura temp = T(t, x)
    '''
    t = mpf(t)
    colchete1 = mpf(2) * sqrt(t*A/pi) * exp(-x**2/(t*4*A))
    colchete2 = x * erfc(x/( mpf(2) * sqrt(t*A)))
    
    return Ti + Q * (colchete1 - colchete2)


def temp_t(t, x=mpf(1), Q=mpf(1), A=mpf(1), Ti=mpf(10)):
    u'''
    Definição da derivada da temperatura em relação ao tempo, temp_t = T_t(t, x)
    '''
    t = mpf(t)
    termo1 = sqrt(A/(t*pi)) * exp(-x**2/(t*4*A))
    termo2 = sqrt(A/(t*pi)) * (x**2/(t**2 * 2 * A)) * exp(-x**2/(t*4*A))
    termo3 = (x**2/(sqrt(t**3 * A) * 4)) * erfc_z(x / (mpf(2) * sqrt(t * A)))
    
    return Q * (termo1 + termo2 + termo3)


def resolver_equacao(a, b, c):
    u'''
    Resolve uma equação do segundo grau.
    '''
    a, b, c = mpf(a), mpf(b), mpf(c)
    d = b ** 2 - 4 * a * c
    return ( (-b+sqrt(d))/(2*a), (-b-sqrt(d))/(2*a) )
    
    
def chute_temp(x=mpf(1), Q=mpf(1), A=mpf(1), Ti=mpf(10), Tf=mpf(50)):
    u'''
    Obtém um chute inicial para o tempo, baseando-se nos parâmetros informados.
    '''
    x, Q, A, Ti, Tf = mpf(x), mpf(Q), mpf(A), mpf(Ti), mpf(Tf)
    a = 1
    b = -x**2/(2*A) - ((Tf-Ti)**2/(Q**2 * 4)) * (pi / A)
    c = (x ** 4) / ((A ** 2) * 16)
    
    t1, t2 = resolver_equacao(a, b, c)
    return t1 if t1 > t2 else t2
    
    
def newton(f, f_x, x0, erro, max_iter, valor=mpf(0.0)):
    u'''
    Implementa:
    
    Parâmetros:
    - f: function(x) => 
    - f_x: function(x) =>
    - x0:       num => chute inicial
    - erro:     num => valor de erro no qual o método vai parar
    - max_iter: num => máximo de iterações
    - valor:    num => valor que o método espera a função alcançar
    
    Retorna (valor, numero_iter), onde:
    - valor: valor obtido pelo método
    - numero_iter: número de iterações necessárias
    '''
    x0, erro, valor = mpf(x0), fabs(erro), mpf(valor)
    
    for i in range(max_iter):
        try:
            x1 = x0 - (f(x0)-valor) / f_x(x0)
        except TypeError:
            x1 = x0 + 300.0
            #raise ValueError('O metodo teve uma aberracao')
        
        erro_iter = fabs(x1 - x0)
        x0 = x1
        
        if erro_iter < erro:
            break
    else:
        raise ValueError('O metodo nao convergiu, o ultimo foi: %f' % x0)
    
    return (x0, i)


def bissecao(func, a, b, erro, valor=mpf(0.0)):
    u'''
    Implementa o método da bisseção para encontrar o ponto onde a 
    função encontra o valor desejado.
    
    Retorna (valor, numero_iter)
    '''
    f = lambda x: func(x) - valor
    a, b = mpf(a), mpf(b)
    erro = fabs(erro)
    i = mpf(0)
    
    while True:
        i += 1
        e = fabs(a-b) / 2
        x = (a+b) / 2
        
        if e <= erro:
            return (x, i)
        
        if f(a) * f(x) > 0:
            a, b = x, b
        elif f(x) * f(b) > 0:
            a, b = a, x
        else:
            raise ValueError('Nao ha variacao de sinal entre os dois.')
    

class TempDir(str):
    u'''
    This class defines a new generator of temporary directories with a context
    manager that automatically deletes the directory when exiting.
    '''
    def __new__(self, *args, **kwargs):
        u'''
        Os argumentos são os mesmos de tempfile.mkdtemp().
        '''
        s = str.__new__(self, tempfile.mkdtemp(dir=os.environ['HOME']))
        return s
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self)
        return exc_type is not None
        
        
def my_plot(data_x=[], data_y=[], title='', xlabel='', ylabel='', plot_title='', filename=''):
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
        
        command = '''

set title "%(title)s"
set xlabel "%(xlabel)s"
set ylabel "%(ylabel)s"
set grid

set style line 1 lc rgb "blue" lt 1 lw 2 pt 7 pi -1 ps 0.5
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
        
        
def questao6():
    
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = []
    chute = chute_temp()
    print 'Chute inicial: %12f' % chute
    print ' i    n   valor'
    
    for i in x:
        valor, n_iter = newton(temp, temp_t, x0=i*chute, max_iter=50, erro=0.000001, valor=50.0)
        print '%02d   %02d   %s' % (i, n_iter, valor)
        y.append(n_iter)
    
    my_plot(x, y, title=u'Número de iterações para múltiplos de %f' % chute,
                  xlabel='n * %f' % chute,
                  ylabel=u'Número de iterações',
                  filename='questao6.png')
    
    
def questao7():
    chute = chute_temp()
    t_star = 1319.7542885 # Obtido no item anterior
    delta = fabs(t_star - chute) + 3
    
    print 'Intervalo inicial: [1100, 1300]'
    valor, n_iter = bissecao(temp, chute-delta, chute+delta, 0.000001, valor=50.0)
    print 'Valor encontrado: %f' % valor
    print 'Numero de iteracoes: %d' % n_iter


def questao8():
    print '%3s %20s %20s %20s' % ('n', 'x', 't0', 't*')
    data_x = linspace(1, 5, 10)
    data_y = []
    for x in data_x:
        t0 = chute_temp(x=x)
        valor, n_iter = newton(lambda t: temp(t, x=x),
                               lambda t: temp_t(t, x=x),
                               x0=t0, max_iter=50000, erro=0.000001, valor=50.0)
        data_y.append(valor)
        print '%3s %20f %20f %20f' % (n_iter, x, t0, valor)
    
    my_plot(data_x, data_y, u'Posição versus Tempo necessário', u'x', u't*', filename='questao8.png')

def questao9a():
    print '%3s %20s %20s %20s' % ('n', 'q', 't0', 't*')
    data_q = linspace(1, 10, 10)
    data_y = []
    for q in data_q:
        t0 = chute_temp(Q=q)
        valor, n_iter = newton(lambda t: temp(t, Q=q),
                               lambda t: temp_t(t, Q=q),
                               x0=t0, max_iter=50, erro=0.000001, valor=50.0)
        data_y.append(valor)
        print '%3s %20f %20f %20f' % (n_iter, q, t0, valor)
    
    my_plot(data_q, data_y, u'Tempo necessário versus parâmetro Q', u'Q', u't*', filename='questao9a.png')

def questao9b():
    print '%3s %20s %20s %20s' % ('n', 'a', 't0', 't*')
    data_a = linspace(1, 10, 10)
    data_y = []
    for a in data_a:
        t0 = chute_temp(A=a)
        valor, n_iter = newton(lambda t: temp(t, A=a),
                               lambda t: temp_t(t, A=a),
                               x0=t0, max_iter=50, erro=0.000001, valor=50.0)
        data_y.append(valor)
        print '%3s %20f %20f %20f' % (n_iter, a, t0, valor)
    
    my_plot(data_a, data_y, u'Tempo necessário versus parâmetro Alpha', u'Alpha', u'Tempo necessário (t*)', filename='questao9b.png')


def questao10():
    print '%3s %20s %20s %20s' % ('n', 'Ti', 't0', 't*')
    data_Ti = linspace(0.1, 49.9, 10)
    data_y = []
    for Ti in data_Ti:
        t0 = chute_temp(Ti=Ti)
        valor, n_iter = newton(lambda t: temp(t, Ti=Ti),
                               lambda t: temp_t(t, Ti=Ti),
                               x0=t0, max_iter=50, erro=0.000001, valor=50.0)
        data_y.append(valor)
        print '%3s %20f %20f %20f' % (n_iter, Ti, t0, valor)
    
    my_plot(data_Ti, data_y, u'Tempo necessário versus Temperatura inicial', u'Ti', u'Tempo necessário (t*)', filename='questao10.png')

    
    
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
    
