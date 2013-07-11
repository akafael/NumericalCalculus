# Define compiler
CC = lualatex

ALL: iterative_process_.pdf

%.pdf: %.tex Makefile
	$(CC) --enable-write18 $< &&	$(CC) $< && $(CC) $<

clean:
	  rm -f *.aux *.bbl	*.blg	*.log	*.pdf 
