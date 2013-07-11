#!/bin/R
# *****************************************************
# Script para Estudo de bifurcações na mapa Logistico
# Versão: 0.1
# Autor: Rafael Lima
# Data: 08/05/2013
# *****************************************************

# Definindo o Processo Iterativo:
P <- function(x=0, l=1) {
	return(l*x*(1-x))
};

P.inter <-function(x0=0,l=1,n=1){
  x = x0;
  for(i in 0:n){
   x = c(x,P(x[i],l));
  }
 return(x);
}

P.inter2 <-function(x0=0,l=0,n=100){
  x = c(x0,P(x0,l));
  i=1;
  while((abs(x[i+1]-x[i])==0)&&(i<n)){
    x = c(x,P(x[i],l));
    i= i+1;
  }
  return(x);
}

# Calculando os pontos fixos:
P.pontoFixo <- function(x0=0,l=1){
  x = c(x0,P(x0,l));
  i=1;
  while((abs(x[2]-x[1])==0)&&(i<100)){
    x0 = x[2];
    x = c(x0,P(x0,l));
    i=i+1;
  }
  print(sprintf('Total de interações feitas: %d',i));
  
  if(i<100){
    return(x[2]);
  } 
  else
  {
    return(NaN);
  }
}

P.pontoFixo2 <- function(x0=0,l=1,err=0.1){
  x = c(x0,P(x0,l));
  i=1;
  while((abs(x[i+1]-x[i])>err)&&(i<100)){
    x = c(x,P(x[i],l));
    i= i+1;
  }
  if(i<100){
    return(x[i]);
  } 
  else 
  { 
    return(NaN);
  }
}

# Questão 2
graph <- function(x0=0,n=100){
   l = 0;
   xi =0;
   for(i in 1:n){
     l = c(l,3*i/n);
     xi = c(xi,P.pontoFixo2(x0,l[i],0));
   }
   png("./image/graph_lambda_xi.png");
   title(bquote(Gráfico \lambda vs X* (X_0 = .(x0))));
   plot(l,xi);
   dev.off();
}

# Questão 3
P.pontoFixo3 <- function(x0=0,l=1,n=100){
  x = c(x0,P(x0,l));
  i=2;
  xi = x0;
  flag=FALSE;
  
  while((i<=n)){
    # Aplica o processo iterativo
    x = c(x,P(x[i],l));
    for(k in 1:i){
      # Encerra caso comece a repetir os pontos fixos encontrados:
      if(flag==TRUE) break;
      # Verifica se existe elementos iguais e armazena:
      if((x[k]==x[i])&&(x[i]!=Inf)&&(x[i]!=-Inf)){
        # Verifica se repetiu algum ponto fixo encontrado:
        for(k in 1:length(xi)){
          if(xi[k]==x[i]){
            i=n+1;
            flag=TRUE
            break;
          }
        }
       xi = c(xi,x[k]);
      }
    }
    i= i+1;
  }
  if(length(xi)>1){
    return(xi);
  }
  else 
  {
    return(NaN);
  }
}

P.numPontoFixo <- function(x0=0,l=1,n=100){
  return(length(P.pontoFixo3(x0,l,n))-1);
}
