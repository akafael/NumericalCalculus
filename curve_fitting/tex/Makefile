# Define compiler
CC = lualatex

ALL: curve_fitting.pdf

curve_fitting.pdf: curve_fitting.tex #Makefile
	$(CC) --enable-write18 $< &&	$(CC) $< && $(CC) $<

clean:
	  rm -f *.aux *.bbl	*.blg	*.log	*.pdf 
