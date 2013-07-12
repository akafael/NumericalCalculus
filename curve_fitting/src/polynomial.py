#! /usr/bin/env python
"""

autors Diogenes, Felipe , Rafael Lima

"""
# import numpy as np
import sys, os, math
#from fractions import Fraction

# read data of table1.dat:
def readMatrix(filename = '../data/table1.dat'):

	matrix = [] 
	# cont:
	i = 0
	# matriz dimmension:
	lines = 0
	columns = 0

	file = open(filename,'r')
	print "table1.dat"
	print str(file.read())

	#Transform file content in 2D - matrix:
	for line in file.readlines():
		line = line.strip().split('\t')
		matrix.append([])
		matrix[i] = line
		i += 1

	lines = len(matrix)
	colummns = len(matrix[0])
	
	print(matrix)

	file.close()

	return (matrix,lines,columns)

# print matrix:
def printMatrix(matrix):
	for line in matrix:
		for e in line:
			print str(e)
		print # line step

# print polynomial
def printPolynomial(pol):
	polynomial = ""
	i = 0
	for a in pol:
		if(i==0):
			polynomial += a
		elif(i==1):
			polynomial += a+"x"
		else:
			polynomial += a+"x^"+i
		polynomial+=" "
		i+=1
	print("p(x) = "+polynomial)

# Eval p(x)
def evalPolynomial(pol,x):
	value = 0
	i = 0
	for a in po:
		value = a*(x^i)

# testando funcoes:
# TODO Verificar se funciona
matrix,l,c = readMatrix()
printMatrix(matrix)


# Ajuste polinomial
"""
1 definir matrizes A , transposta de A e Y
2 Calcular os produtos de matrizes A*AT e AT*Y
3 Resolver o sistema.
"""

# do polymonial fitting:


