#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int a, b;

void handler (int sig)
{
    if(sig==SIGUSR1)
    {
        printf("La differenza di a e b e': %d\n", (a-b));
    }
    else if(sig==SIGUSR2)
    {
        printf("La somma di a e b e': %d\n", (a+b));
    }
    else if(sig==SIGINT) exit(0);
    return;
}

int main(void)
{
    (void)signal(SIGUSR1, handler);
    (void)signal(SIGUSR2, handler);
    (void)signal(SIGINT, handler);
    printf("Dammi due interi:\n");
    scanf("%d %d", &a, &b);
    while(0==0) pause();
    return 0;
}
