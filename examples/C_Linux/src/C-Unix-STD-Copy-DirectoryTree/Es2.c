#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <assert.h>
#include <fcntl.h>
#define N 1000

void copia (char *, char *);

int main (int argc, char **argv)
{

    struct stat statbuf1, statbuf2;

    //Controllo errori prima di passare i percorsi alla funzione
    assert (argc==3);
    if (lstat(argv[1], &statbuf1)<0)
    {
        fprintf(stderr, "Errore nel primo statbuf\n");
        return (-1);
    }
    if (lstat(argv[2], &statbuf2)<0)
    {
        fprintf(stderr, "Errore nel secondo statbuf\n");
        return (-2);
    }
    //Controllo che sia una directory
    if (S_ISDIR(statbuf1.st_mode)==0)
    {
        fprintf(stderr, "Il primo percorso non è una directory\n");
        return (-3);
    }
    if (S_ISDIR(statbuf2.st_mode)==0)
    {
        fprintf(stderr, "Il secondo percorso non è una directory\n");
        return (-4);
    }

    copia(argv[1], argv[2]);

    return 0;
}

void copia (char *percorso1, char *percorso2)
{
    struct dirent *dirp;
    int i=0, f1, f2, nr, nw, c;
    DIR *dp1, *dp2;
    struct stat statbuf;
    char fullName1[N], fullName2[N], vet[N];
    //Di ogni variabile ne serve una per ogni directory

    if ((dp1=opendir(percorso1))==NULL)
    {
        fprintf(stderr, "Errore nell'apertura directory 1\n");
        return (-5);
    }
    if ((dp2=opendir(percorso2))==NULL)
    {
        fprintf(stderr, "Errore nell'apertura directory 2\n");
        return (-6);
    }

    while ( (dirp = readdir(dp1)) != NULL)
    {
        //dirp->d_name è il nome del file nella cartella
        if(strcmp(dirp->d_name, ".")!=0 && strcmp(dirp->d_name, "..")!=0)
        {
            sprintf (fullName1, "%s/%s", percorso1, dirp->d_name);
            sprintf (fullName2, "%s/%s", percorso2, dirp->d_name);
            if (lstat(fullName1, &statbuf) < 0 )
            {
                fprintf (stderr, "Error.\n"); exit (1);
            }
            //Copia di file
            if (S_ISDIR(statbuf.st_mode) == 0)
            {
               f1=open(fullName1, O_RDONLY);
               f2=open(fullName2, O_WRONLY | O_CREAT);
               if(f1==(-1) || f2==(-1))
               {
                    fprintf(stderr, "Errore apertura file!");
                    exit (2);
               }
               while((nr=read(f1, vet, N))>0)
               {
                    nw=write(f2, vet, nr);
                    if(nr!=nw)
                    {
                        fprintf(stderr, "Errore nella copia del file!");
                        exit(3);
                    }

                    close(f1);
                    close(f2);
               }
            }
            //Copia cartella e ricorri
            else
            {
                c=mkdir(fullName2, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
                if(c==-1)
                {
                    fprintf(stderr, "Errore creazione directory!");
                    exit(4);
                }
                copia(fullName1, fullName2);
            }
            i++;
        }
    }

    if (closedir(dp1) < 0)
    {
        fprintf (stderr, "Error.\n");
        exit (5);
    }
    return;
}
