#!/usr/bin/env python
# -*- coding: utf-8 *-*

"""

@autors Diógenes Oliveira, Felipe Bressan, Rafael Lima

"""
import pprint
import numpy
import os
import sys

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
    
    x = transpose([coef])
    
    # Calculando o vetor erro a partir de e = y - Ax
    erro = add_and_multiply(Y, product(A, x), -1.0)
    print 'ERRO: %f' % numpy.linalg.norm(erro)
    return coef

def interpolador(table):
    
    A = get_A(table, len(table)-1)
    Y = get_column(table, 1)
    coef = solve_system(A, Y)
    
    return coef


def derivative_first(table):
    
    deltaT = 0.1
    d = [(-1.5 * table[0][1] + 2 * table[1][1] - 0.5 * table[2][1])/deltaT]
    
    for i in range(1, len(table)-1):
        d.append((-0.5 * table[i-1][1] + 0.5 * table[i+1][1])/deltaT)
    
    d.append((-1.5 * table[-1][1] + 2 * table[-2][1] - 0.5 * table[-3][1])/deltaT)
    return d

def derivative_second(table):
    
    deltaT = 0.1
    d = [(2 * table[0][1]  -5 * table[1][1] +4 * table[2][1] -1 * table[3][1])/(deltaT**2)]
    
    for i in range(1, len(table)-1):
        d.append((1.0 * table[i-1][1] -2.0 * table[i][1] +1.0*table[i+1][1])/(deltaT**2))
        
    d.append((2 * table[-1][1]  -5 * table[-2][1] +4 * table[-3][1] -1 * table[-4][1])/(deltaT**2))
    return d


def integral_trapezio(table):
    """
    Calcula a integral dos pontos atraves da Regra do Trapezio.
    """
    
    deltaT = table[1][0] - table[0][0]
    soma = (table[0][1] + table[-1][1]) / 2.0
    for i in range(1, len(table)-1):
        soma += table[i][1]
    return soma * deltaT


def integral_simpson(table):
    """
    Calcula a integral dos pontos atraves da regra 1/3 de Simpson.
    """
    deltaT = table[1][0] - table[0][0]
    soma = (table[0][1] + table[-1][1])
    
    for impar in range(1, len(table)-1, 2):
        soma += 2.0 * table[impar][1]
        soma += 4.0 * table[impar+1][1]
    
    return soma * deltaT / 3.0


def printDat_matrix(matrix,filename,format_str='%f',):
    """
    Imprime a matriz em um arquivo
    """
    
    datafile = open(filename,'w')

    for row in matrix:
        for elem in row:
            datafile.write()

def pol2tex(coef,filename="equation.tex", format_str='%+.2f'):
    """
    Imprime arquivo .tex com o polinomio
    """
    s = '$'
    for i in reversed(range(1, len(coef))):
        s+= (format_str + '\\cdot x^{%d} ') % (coef[i], i)
    s+= ' ' + format_str % coef[0] + '$'

    texfile = open("../tex/"+filename,'w')
    texfile.write(s)
    texfile.close()


def multiple_plot(polynomials, titles,nameGraph="graph1.png", yrange=(-20.0, 20.0)):
    u"""
    Chama o processo gnuplot para plotar um gráfico dos dados no vetor y
    versus os dados no vetor x.
    """
    command = ""
    command += "set terminal pngcairo enhanced font \'Verdana,10\'\n"
    command += 'set yrange [%f:%f]\n' % yrange
    command += 'set key top\n'
    command += 'outfile = \"%s\" \n' % str('../image/'+nameGraph)
    command += 'set output outfile\n'
    for i, polynomial in enumerate(polynomials):
        command += 'f%d(x) = %s\n' % (i, to_str(polynomial))
        pol2tex(polynomial,'pol%d.tex'% (len(polynomial)-1))
        
    command += 'plot '
    command += ', '.join(['f%d(x) title "%s"' % (i, titles[i]) for i in range(len(polynomials))] +
                         ["\"../data/table1.dat\" u 2:3 t \"Dados\""])
    print command
    os.system("echo '%(command)s' | gnuplot -persist" % vars())
    
def multiple_integrate(data,nameFile="tableIntegrate.dat"):
    datafile = open("../data/"+nameFile,'w')

    s = str(integral_trapezio(data))+'\t'
    s += str(integral_simpson(data))+'\n'

    datafile.write(s)
    datafile.close
    
if __name__ == '__main__':
    table = read_table()
    polynomials = []
    titles = []
    
    # Questão 1
    for degree in (1, 3, 5, 10):
        coef = fit_polynomial(table, degree)
        polynomials.append(coef)
        titles.append('Grau %d' % degree)
        print 'Grau %d => ' % degree + to_str(coef)
    
    multiple_plot(polynomials, titles)
    
    # Questão 2
    interp = interpolador(table)
    
    multiple_plot([interp], ['Interpolacao'],"graph2.png", (-100, 100))
    print 'Interpolador => %s' % to_str(interp)
    
    
    # Questão 3
    # TODO calcular derivada para as funções de aproximação
    first = derivative_first(table)
    second = derivative_second(table)
    
    print 'Derivada primeira'
    print_matrix([first])
    print 'Derivada segunda'
    print_matrix([second])


    multiple_plot([first], ['1 derivada'],"graph3.png",(-100,100))
    multiple_plot([second], ['2 derivada'],"graph4.png",(-100,100))
    #multiple_plot([table,first,second],['dados','1','2'],"graph3.png")
    
    # Questão 4
    # TODO Calcular integral para as funções de aproximação
    
    multiple_integrate(table)

    integral = integral_trapezio(table)
    print 'Integral pelo metodo do trapezio: %f' % integral
    
    integral = integral_simpson(table)
    print 'Integral pelo metodo 1/3 de Simpson: %f' % integral 
    
