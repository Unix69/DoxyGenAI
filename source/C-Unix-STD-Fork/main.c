#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <semaphore.h>
#define max 100

int main()
{
    int i;
    char tmp[max];
    char *string;
    int n=strlen(string);
    sem_t *s=(sem_t*)malloc(sizeof(sem_t));
    pid_t *pid=malloc(n*sizeof(pid_t));

    sem_init(s,0,0);
    fscanf(stdin, "%s", tmp);
    string=strdup(tmp);

    for(i=0;i<n;i++){
    pid[i]=fork();
    if(!pid[i]){//figlio i-esimo
        sem_wait(s);
        printf("%c", string[i]);
        fflush(stdout);
        exit(0);
    }}

    while((i--)>0)
        sem_post(s);
}
