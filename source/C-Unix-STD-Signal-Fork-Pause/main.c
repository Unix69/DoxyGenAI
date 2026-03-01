#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#define N 51

void handler(int sig)
{
    if(sig==SIGUSR1)
    {
        printf("Avvio figlio\n");
    }
    else if(sig==SIGCHLD)
    {
        printf("Figlio terminato\n");
    }
    return;
}

int main(void)
{
    pid_t son1, son2;
    char txt1[N], txt2[N];
    int f1, f2;

    f1=open("son1.txt", O_RDONLY);
    f2=open("son2.txt", O_RDONLY);
    (void)signal(SIGUSR1, handler);
    (void)signal(SIGCHLD, handler);

    son1=fork();
    if(son1==-1)
    {
        fprintf(stderr, "Errore fork 1!!!\n");
        exit(0);
    }
    else if(son1==0) //figlio1
    {
        pause();
        read(f1, txt1, 50);
        fwrite(txt1, sizeof(char), 50, stdout);
        printf("\n");
        exit(2);
    }
    else
    {
        son2=fork();
        if(son2==-1)
        {
            fprintf(stderr, "Errore fork 1!!!\n");
            exit(1);
        }
        else if(son2==0) //figlio 2
        {
            pause();
            read(f2, txt2, 50);
            fwrite(txt2, sizeof(char), 50, stdout);
            printf("\n");
            sleep(5);
            exit(3);
        }
        else //padre
        {
            printf("PID figlio 1: %d\nPID figlio 2: %d\n", son1, son2);
            sleep(2);
            kill(son1, SIGUSR1);
            pause();
            kill(son2, SIGUSR1);
            pause();
        }
    }

    close(f1);
    close(f2);
    return 0;
}
