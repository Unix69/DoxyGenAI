#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <fcntl.h>
#define N 20

int main(void)
{
    pid_t p;
    int file[2], f, nr, nw, nw2, nlette;
    char str[N], str2[N];

    if(pipe(file)==0)
    {
        p=fork();
        assert(p!=-1);
        if(p==0) //Figlio
        {
            close(file[0]);
            f=open("testo.txt", O_RDONLY);
            while((nr=read(f, str, N))>0)
            {
                nw=write(file[1], str, nr);
                assert(nr==nw);
            }
            close(f);
            exit(0);
        }
        else //Padre
        {
            close(file[1]);
            while((nlette=read(file[0], str2, N))>0)
            {
                nw2=write(1, str2, nlette);
                assert(nw2==nlette);
            }
        }
    }
    return 0;
}
