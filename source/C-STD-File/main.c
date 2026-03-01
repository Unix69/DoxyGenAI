#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main (int argc, char **argv) 
{
	FILE *f1, *f2;
	char c=0;

	if(argc!=3)
	{
		fprintf(stderr, "Errore numero di argomenti");
	}
	
	f1=fopen(argv[1], "r");
	if(f1==NULL)
	{
		fprintf(stderr, "Errore apertura primo file");
	}

	f2=fopen(argv[2], "w");
	assert(f2!=NULL);
	
	while(c	!=EOF)
	{
		c=fgetc(f1);
		if(c!=EOF)
		{
			fputc(c, f2);	
		}
	}
	return 0;
}