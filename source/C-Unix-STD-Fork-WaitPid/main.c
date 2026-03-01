#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <assert.h>
#define N 5
#define M 3

int main()
{
    int i, status;
    pid_t childID[N];

    for(i=0; i<N; i++)
    {
        if(childID[i]=fork()==(-1))
        {
            fprintf(stderr, "Errore fork!\n");
            exit(EXIT_FAILURE);
        }
        else if(childID[i]==0)
            exit(EXIT_SUCCESS);
    }

    for(i=N; i>M; i++)
        waitpid(childID[i], &status, 0);

    return 0;
}
