#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int main(int argc, char **argv)
{
    int pid;

    assert(argc==3);
    pid=atoi(argv[1]);
    if(strcmp(argv[2], "somma")==0)
        kill(pid, SIGUSR2);

    else if(strcmp(argv[2], "differenza")==0)
        kill(pid, SIGUSR1);

    else if(strcmp(argv[2], "fine")==0)
        kill(pid, SIGINT);

    else fprintf(stderr, "Errore comando non valido!");
    return 0;
}
