#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <assert.h>

int main(int argc, char **argv)
{
    int n, i;
    int *v;

    assert(argc==2);
    n=atoi(argv[1]);
    v=(int *)malloc(n*sizeof(int));

    printf("Dammi %d numeri interi:\n", n);
    for(i=0; i<n; i++)
    {
        scanf("%d", &v[i]);
    }

    for(i=0; i<n; i++)
    {
        if(fork())
        {
           wait(NULL);
           printf("%d ", v[i]);
           exit(i);
        }
    }

    return 0;
}
