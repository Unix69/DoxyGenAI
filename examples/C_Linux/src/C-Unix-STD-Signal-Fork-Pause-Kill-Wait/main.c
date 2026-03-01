#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>

void handler(int s)
{
    return;
}

int main(void)
{
    pid_t p1, p2;

    (void)signal(SIGUSR1, handler);
    (void)signal(SIGUSR2, handler);

    p1=fork();
    assert(p1!=(-1));
    if(p1==0) //Figlio 1
    {
        sleep(1);
        printf("Figlio 1 manda SIGUSR1\n");
        kill(getppid(), SIGUSR1);
        pause();
        printf("Figlio 1 riceve SIGUSR2 ed esce\n");
        exit(0);
    }
    else
    {
        p2=fork();
        if(p2==0)  //Figlio  2
        {
            pause();
            printf("Figlio 2 riceve SIGUSR1, invia SIGUSR2 ed esce\n");
            kill(getppid(), SIGUSR2);
            exit(1);
        }
        else //Padre
        {
            pause();
            printf("Padre intercetta e inoltra SIGUSR1\n");
            kill(p2, SIGUSR1);
            pause();
            printf("Padre intercetta e inoltra SIGUSR2\n");
            kill(p1, SIGUSR2);

        }
    }
    printf("Padre termina\n");
    return 0;
}
