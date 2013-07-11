#!/usr/bin/env R

# Função auxiliar para o cálculo da função erro
soma <- function(z) {
    a <- c(0.0705230784,
           0.0422820123,
           0.0092705272,
           0.0001520143,
           0.0002765672,
           0.0000430638);
           
    return (1 + a[1]*z + a[2]*z^2 + a[3]*z^3 + a[4]*z^4 + a[5]*z^5 + a[6]*z^6);
}

# Definição da função erro
erf <- function(z) {
    return(1 - (soma(z))^(-16));
}

# Derivada da função erro
erf_z <- function(z) {
    a <- c(0.0705230784,
           0.0422820123,
           0.0092705272,
           0.0001520143,
           0.0002765672,
           0.0000430638);
    
    soma_z <- (a[1] + 2*a[2]*z + 3*a[3]*z^2 + 4*a[4]*z^3 + 5*a[5]*z^4 + 6*a[6]*z^5);
    
    return(1 + 16 * (soma(z))^(-17) * soma_z);
}

erfc <- function(z) {
    return(1-erf(z));
}

erfc_t <- function(z) {
    return(-erf(z));
}

# Função principal Temp = T(x, t)
Temp <- function(t, x=1, Q=1, A=1, Ti=10) {
    return(Ti + Q * (2 * sqrt(A*t/pi) * exp(-(x^2)/(4*A*t))
                     - x * erfc(x/(2*sqrt(A*t)))));
}

# Derivada da função principal Temp_t = T_t(x, t)
Temp_t <- function(t, x=1, Q=1, A=1, Ti=10) {
    d <-(  sqrt(A / (t*pi)) * exp(-x^2/(4*A*t))
         + sqrt(A*t/pi) * (x^2 / (2*A*t^2)) * exp(-x^2/(4*A*t))
         + (x^2 / (4*sqrt(A*t^3))) * erfc_t(x / (2 * sqrt(A*t))) );
    
    return(d * Q);
}

# Método iterativo de Newton-Rapson
newton <- function(f, f_x, x0, erro, max_iter, valor=0.0) {
    x1 <- x0;
    exausted <- TRUE;
    
    for(i in 1 : max_iter) {
        x1 <- x0 - (f(x0)-valor) / f_x(x0);
        print("---------------------")
        print(x0)
        print(f(x0))
        print(f_x(x0))
        print(x1)
        x0 <- x1;
    }
    
    if(exausted) {
        stop("O método não convergiu.");
    }
    
    return(x1);
}
