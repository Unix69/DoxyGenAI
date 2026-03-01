#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>
#define N 100

void funzione (char *);

int main (int argc, char **argv)
{

    struct stat statbuf;
    char fullName[N];

    //Controllo errori prima di passare il percorso alla funzione
    if (lstat(argv[1], &statbuf)<0)
    {
        fprintf(stderr, "Errore nel primo if\n");
        return (-1);
    }
    //Controllo che sia una directory
    if (S_ISDIR(statbuf.st_mode)==0)
    {
        fprintf(stderr, "Errore nel secondo if\n");
        return (-2);
    }

    funzione(argv[1]);

    return 0;
}

void funzione(char *percorso)
{
    struct dirent *dirp;
    int i=0;
    DIR *dp;
    struct stat statbuf;
    char fullName[N];
    //Di ogni variabile ne serve una per ogni directory

    if ((dp=opendir(percorso))==NULL)
    {
        fprintf(stderr, "Errore nell'apertura if\n");
        return (-3);
    }

    while ( (dirp = readdir(dp)) != NULL)
    {
        //dirp->d_name è il nome del file nella cartella
        if(strcmp(dirp->d_name, ".")!=0 && strcmp(dirp->d_name, "..")!=0)
        {
            sprintf (fullName, "%s/%s", percorso, dirp->d_name);
            if (lstat(fullName, &statbuf) < 0 )
            {
                fprintf (stderr, "Error.\n"); exit (1);
            }
            //Stampa nome file se non è una cartella
            if (S_ISDIR(statbuf.st_mode) == 0)
            {
                fprintf (stdout, "File %d: %s\n", i, fullName);
            }
            //Stampa nome cartella e ricorri
            else
            {
                fprintf (stdout, "Dir %d: %s\n", i, fullName);
                funzione(fullName);
            }
            i++;
        }
    }

    if (closedir(dp) < 0)
    {
        fprintf (stderr, "Error.\n"); exit (1);
    }
    return;
}
