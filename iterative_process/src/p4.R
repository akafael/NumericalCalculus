#!/usr/bin/env R

# Script para calcular as Raizes através de processos iterativos
# Autor: Rafael Lima
# Versão: 0.000032
# Data: 09/05/2013

# Define a função erf junto dos parâmetros:


erf <- function(x=0){
  a <- c(0.0705230784,
    0.0422820123,
    0.0092705272,
    0.0001520143,
    0.0002765672,
    0.0000430638);
  b <- 1/(1+a[1]*x+a[2]*x^2+a[3]*x^3+a[4]*x^4+a[5]*x^5+a[6]*x^6);
  return(b);
}

# definindo a derivada da função:
erf.D <- function(x =0){
  a <- c(0.0705230784,
    0.0422820123,
    0.0092705272,
    0.0001520143,
    0.0002765672,
    0.0000430638);
  b <- -(a[1]+2*a[2]*x^2+3*a[3]*x^2+4*a[4]*x^3+5*a[5]*x^3+6*a[6]*x^5)/
        (1+a[1]*x+a[2]*x^2+a[3]*x^3+a[4]*x^4+a[5]*x^5+a[6]*x^6)^2;
  return(b);
}


# Função principal T(x, t)
T <- function(x, t, a, q, Ti){
  Tf <- Ti + q*(2*(a*t/pi)^(1/2)*exp(x^2/(4*a*t)-x*erf(x/(2*(a*t)^(1/2)))));
  return(Tf);
}


# Derivada de T(x, t) em relação a T
T_t <- function(x,t, a, q, Ti){
  b <- q*(2*(a/pi)*exp(x^2/4*a*t) +
         (2*(a*t/pi)^(1/2))*exp(x^2/(4*a*t))*(-x^2/4*a*t^2) -
         erf(x/(2*(a*t)^(1/2)))-
         x*erf.D(x/(2*(a*t)^(1/2)))*(-a*x/(4*(a*t)^(3/2))));
  return(b);
}

Temp_t <- function(x, t, a, q, Ti) {

}


# Definindo a função de iteração do método
P <- function(x, t, a, q, Ti, Tf) {
    return(t - (T(x, t, a, q, Ti) - Tf) / T_t(x, t, a, q, Ti));
}


iter4 <- function(t) {
    Ti <- 10;
    Tf <- 50;
    q  <- 1;
    a  <- 1;
    x  <- 1;
    return(P(x, t, a, q, Ti, Tf))   ;
}


# Método iterativo principal
newton <- function(x0, error, max_tries) {
    exausted <- TRUE;
    x1 <- x0;
    for(i in 1:max_tries) {
        print(i)
        print(x1)
        print("-----------")
        x2 <- iter4(x1);
        
#        if(-error <= (x2-x1) || (x2-x1) <= error) {
#            exausted <- FALSE;
#        #    break;
#        #}
        x1 <- x2;
    }
    
    if(exausted) {
        print("ESGOTARAM");
    }
    
    return(x1);
}

