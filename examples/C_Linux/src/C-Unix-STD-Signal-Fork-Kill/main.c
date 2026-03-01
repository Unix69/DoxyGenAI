#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void handler(int sig)
{
    printf("Ricevuto segnale %d\n", sig);
    if(sig==SIGUSR1)
    {
        kill(getppid(), SIGUSR2);
    }
    else if(sig==SIGUSR2)
    {
        kill(getppid(), SIGUSR1);
    }
    else if(sig==SIGINT)
    {
        kill(getppid(), SIGINT);
    }
    return;
}

int main(int argc, char **argv)
{
    int i, j, *s;
    pid_t child;

    s=malloc((argc-1)*sizeof(int));
    for(i=1; i<argc; i++)
    {
        j=i-1;
        s[j]=atoi(argv[i]);
    }
    i=0;

    (void)signal(SIGUSR1, handler);
    (void)signal(SIGUSR2, handler);
    (void)signal(SIGINT, handler);

    child=fork();
    if(child==-1)
    {
        fprintf(stderr, "Errore fork");
        exit(0);
    }
    else if(child==0)
    {
        while(0==0)
        {
            pause();
        }
    }
    else
    {
        while(i!=5) //ciclo infinito del padre
        {
            sleep(1);
            kill(child, s[i]);
            i++;
            if(i>(argc-1)) i=0;
        }
    }
    free(s);
    free(s);
    return 0;
}
