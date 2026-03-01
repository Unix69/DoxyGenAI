#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <assert.h>

int main(int argc, char **argv)
{
    int i, n, t;

    assert(argc==3);
    n=atoi(argv[1]);
    t=atoi(argv[2]);

    for(i=0; i<n; i++)
    {
       if(fork())
       {
            if(fork())
            exit(0);
       }

    }

    sleep(t);
    printf("Il processo foglia e' terminato!\n");
    return 0;
}
