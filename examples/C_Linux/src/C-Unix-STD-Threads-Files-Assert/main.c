#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pthread.h>
#include <string.h>
#include <assert.h>
#define N 50


struct nf
{
    
char filein[N];
char fileout[N];
int *buf;
int nr;

};


typedef struct nf nomifile;



void ReadFileIn(void *ptr);
void bubblesort(void *ptr);
void WriteFileOut(void *ptr);


void *funzione(void *ptr)
{
ReadFileIn(ptr);
bubblesort(ptr);
WriteFileOut(ptr);
return NULL;
}




void ReadFileIn(void *ptr)
{
FILE *fin;
int i;

nomifile *arg=(nomifile *)ptr;

fin=fopen(arg->filein, "r");
fscanf(fin, "%d", &arg->nr);
arg->buf=malloc((arg->nr)*sizeof(int));

for(i=0; i<arg->nr; i++){
	fscanf(fin, "%d", &arg->buf[i]);
}

fclose(fin);

return;

}







void bubblesort(void *ptr)
{

int i, j, tmp;

nomifile *arg=(nomifile *)ptr;


for(i=1; i<arg->nr; i++){

for(j=0; j<(arg->nr-i); j++)
{
           
if(arg->buf[j]>arg->buf[j+1])
{
  
tmp=arg->buf[j];

arg->buf[j]=arg->buf[j+1];

arg->buf[j+1]=tmp;

}
}

}
    
return;

}








void WriteFileOut(void *ptr)
{
    
FILE *fout;
    
int i;
    
nomifile *arg=(nomifile *)ptr;

    
fout=fopen(arg->fileout, "w");

    
for(i=0; i<arg->nr; i++)
{
        
fprintf(fout, "%d\n", arg->buf[i]);
    
}

fclose(fout);
    
return;

}



int main(int argc, char **argv)
{
    
if((argc<=2)||(argc%2==0))  //Gli argomenti devono essere almeno 3 e sempre dispari
{
	fprintf(stderr, "Errore negli argomenti!\n");
	exit(0);
}

    
int n=(argc-1)/2, i, j=1, err; //Il numero di thread è il numero di file/2
pthread_t *tid;
nomifile **v;
tid=malloc(n*sizeof(pthread_t)); //Allocazione vettori
v=malloc(n*sizeof(nomifile *));

for(i=0; i<n; i++)
v[i]=malloc(sizeof(nomifile));

for(i=0; i<n; i++)  //Inizializzazione vettore struct
{       
strcpy(v[i]->filein, argv[j]);
j++;
strcpy(v[i]->fileout, argv[j]);    
j++;
err=pthread_create(&tid[i], NULL, funzione, v[i]);    
assert(err==0);
}

pthread_join(tid[n-1], NULL);

return 0;

}

