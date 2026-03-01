#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#define n(a) (a-1)/2
void proc(char *inputfile, char *outputfile);
void *thread_function(void *arg);
struct file{char *input_file;char *output_file;};
typedef struct file ftype;

void main(int argc, char **argv){
ftype *v;
pthread_t *tid;
int r;
int i_file=((argc>2)&&(argc%2!=0)?n(argc):-1);
int i=0;
int j=0;
int r=0;

if(i_file==-1)
exit(-1);

v=malloc(sizeof(ftype)*i_file);
tid=malloc(sizeof(pthread_t)*i_file);

while(i<i_file){
tid[i]=i;
v[i].input_file=malloc(sizeof(char)*strlen(argv[j]) + 1);
strcpy(v[i].input_file,argv[j++]);
v[i].output_file=malloc(sizeof(char)*strlen(argv[j]) + 1);
strcpy(v[i++].output_file,argv[j++]);
}

for(i=0; i<i_file; i++, assert(r==0))
    r=pthread_create(&tid[i],NULL, thread_function, &v[i]);
    pthread_join(tid[i_file-1], NULL);
    return 0;
}

void proc(char *inputfile, char *outputfile){
int buffer[MAX];
FILE *fi;
FILE *fo;
int i=0;
int nr=0;
fi=fopen(inputfile, "r");
fscanf(fi, "%d", &nr);
for(; i<nr; i++)
    fscanf(fi, "%d", &buffer[i]);
    fclose(fi);
buffer=sort(&buffer, nr);
fo=fopen(outputfile, "w+");
for(i=0; i<nr; i++)
    fprintf(fo, "%d", buffer[i]);
    return NULL;
}

void *thread_function(void *arg){
    ftype *seg=(ftype *)arg;
    proc(seg->input_file, seg->output_file);
    return NULL;
    }

int *sort(int *buffer, int nr){
int i,j;
int temp;
for(i=0; i<nr-1; i++)
for(j=i; j<nr; j++)
    if(buffer[i]>buffer[j]){
        temp=buffer[i];
        buffer[i]=buffer[j];
        buffer[j]=temp;
    }
return(buffer);
}

