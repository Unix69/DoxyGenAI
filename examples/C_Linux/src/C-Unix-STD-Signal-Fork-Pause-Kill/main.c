#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/stat.h>

void handler(int s)
{
    return;
}

int main(void)
{
    pid_t p1;

    (void)signal(SIGINT, handler);
    (void)signal(SIGCHLD, handler);

    p1=fork();
    assert(p1!=-1);

    if(p1==0) //Figlio
    {
        pause();
        printf("\nSono il figlio con PID %d\n", getpid());
        exit(0);
    }
    else if(p1!=0) //Padre
    {
        pause();
        kill(p1, SIGINT);
        pause();
        printf("Padre terminato\n");
    }

    return 0;
}
