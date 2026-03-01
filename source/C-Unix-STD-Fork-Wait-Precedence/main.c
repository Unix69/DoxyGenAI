#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#define N 13

int main(void)
{
    pid_t p1, p2, p3;
    int status;
    int i=1;

    p1=fork(); //P1
    if(p1==0)
    {
       fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
       exit(i);
    }
    else //master
    {
        wait(&status);
        p1=fork(); //p2
        i++;
        if(p1!=0) //nel master
        {
            p2=fork(); //p3
            i++;
            if(p2==0)
            {
                fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                exit(i);
            }
            wait(&status);
        }
        else if(p1==0) //p2
        {
            fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
            exit(i);
        }
        wait(&status);
        p1=fork(); //p4
        i++;
        if(p1==0)
        {
            fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
            exit(i);
        }
        else if(p1!=0) //master
        {
            p2=fork();
            i++;
            if(p2==0) //p5
            {
                fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                exit(i);
            }
            else if(p2!=0) //master
            {
                p3=fork();
                i++;
                if(p3==0) //p6
                {
                    fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                    exit(i);
                }
                wait(&status);
            }
            wait(&status);
        }
        wait(&status);
        p1=fork(); //p7
        i++;
        if(p1==0)
        {
            fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
            exit(i);
        }
        else if(p1!=0) //master
        {
            p2=fork();
            i++;
            if(p2==0) //p8
            {
                fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                exit(i);
            }
            else if(p2!=0) //master
            {
                p3=fork();
                i++;
                if(p3==0) //p9
                {
                    fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                    exit(i);
                }
                wait(&status);
            }
            wait(&status);
        }
        wait(&status);
        p1=fork(); //p10
        i++;
        if(p1==0)
        {
            fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
            exit(i);
        }
        else if(p1!=0) //master
        {
            p2=fork(); //p11
            i++;
            if(p2==0)
            {
                fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
                exit(i);
            }
            wait(&status);
        }
        wait(&status);
        p1=fork(); //p12
        i++;
        if(p1==0)
        {
            fprintf(stdout, "%d PID: %d Padre: %d\n", i++, getpid(), getppid());
            exit(i);
        }
        wait(&status);
    }
    return 0;
}
