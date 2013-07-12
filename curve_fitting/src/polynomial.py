#! /usr/bin/env python
"""

autors Diogenes, Felipe , Rafael Lima

"""
# import numpy as np
import sys, os, math
#from fractions import Fraction


# read data of table1.dat:
def lerMatriz():
	matriz = [] 
	# contador
	i = 0
	#dimensoes da matriz
	linhas = 0
	colunas = 0

	arquivo = open('../data/table1.dat','r')
	print str(file)
	print str('\n')

	#Trasforma o arquivo lido em uma matriz 2D
	for linha in arquivo:
		linha = linha.strip().split('\t')
		matriz.append([])
		matriz[i] = linha
		i += 1

	linhas = len(matriz)

	for c in matriz[0]:
		colunas += 1

	arquivo.close()

	return (matriz,linha,colunas)

# print matrix:
def imprimeMatriz(matriz):
	for i in range(len(matriz)):
		for j in range(len(matriz[i])):
			print str(matriz[i][j])
		print # pula uma linha


# testando funcoes:
# TODO Verificar se funciona
matriz = lerMatriz()
imprimeMatriz(matriz)


# Ajuste polinomial
"""
1 definir matrizes A , transposta de A e Y
2 Calcular os produtos de matrizes A*AT e AT*Y
3 Resolver o sistema.
"""



# do polymonial fitting:


