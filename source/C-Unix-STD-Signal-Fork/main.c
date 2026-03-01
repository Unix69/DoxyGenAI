#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <assert.h>

void manager(int sig)
{
    if(sig==SIGUSR1)
    {
        printf("Il padre ha PID %d, io sono il figlio con PID %d, ho ricevuto il seganle %d\n", getppid(), getpid(), sig);
    }
    return;
}

int main(int argc, char **argv)
{
    assert(argc==2);

    int n=atoi(argv[1]), i;
    pid_t pid;
    signal(SIGUSR1, manager);

    for(i=0; i<n; i++)
    {
        pid=fork();
        if(pid==-1)
        {
            fprintf(stderr, "Errore fork %d", i);
            exit(0);
        }
        else if(pid==0)
        {
            pause();
            exit(i);
        }
        else
        {
            sleep(2);
            printf("Sono il padre con PID %d e il figlio %d ha PID %d\n", getpid(), i, pid);
            kill(pid, SIGUSR1);
        }
    }
    return 0;
}
