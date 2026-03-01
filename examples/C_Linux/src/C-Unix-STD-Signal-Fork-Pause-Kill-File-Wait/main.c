#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/stat.h>
#define N 100

void handler(int s){
    return;
}

int main(void){
    pid_t p1, p2, *pp1, *pp2;
    pp1=&p1;
    pp2=&p2;
    int f1, f2, nR1, nW1, nR2, nW2;
    char buff[N], buff2[N];

    (void)signal(SIGUSR1, handler);
    (void)signal(SIGCHLD, handler);

    p1=fork();
    assert(p1!=-1);

    if(p1==0) //Figlio1
    {
       pause();
       f1=open("testo_1.txt", O_RDONLY);
       while((nR1=read(f1, buff, N))>0)
       {
            nW1=write(1, buff, nR1);
            printf("\n");
            kill(*pp2, SIGUSR1);
            pause();
            assert(nR1==nW1);
       }
       close(f1);
       kill(*pp2, SIGUSR1);
       exit(0);
    }
    else if(p1!=0) //Padre
    {
        p2=fork();
        assert(p2!=-1);
        if(p2==0) //Figlio2
        {
            pause();
            f2=open("testo_2.txt", O_RDONLY);
            while((nR2=read(f2, buff2, N))>0)
            {
                nW2=write(1, buff2, nR2);
                printf("\n");
                kill(*pp1, SIGUSR1);
                pause();
                assert(nR2==nW2);
            }
            close(f2);
            kill(*pp1, SIGUSR1);
            exit(0);
        }
        else if(p2!=0) //Padre
        {
            sleep(1);
            kill(p1, SIGUSR1);
            pause();
            kill(p2, SIGUSR1);
            pause();
            printf("Padre terminato\n");
        }
    }

    return 0;
}
