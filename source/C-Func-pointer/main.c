#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define dim 10
typedef void* tf;

void show(void *b){
    int *v, i = 0;
    v=(int *)b;
    for(printf("Start\n");i<dim;printf("\nv[%d] = %d", i, v[i++]));
    return;
}

void inc(int a, void *b){
    int *v, i = 0;
    v=(int *)b;
    for(;i<dim;v[i++]+=a);
    return;
}

void *init(){
    int *v, i = 0;
    v=malloc(sizeof(int)*dim);
    for(;i<dim;v[i++]=0);
    return((void*)v);
}



void sub(int a, void *b){
    int *v, i = 0;
    v=(int *)b;
    for(;i<dim;v[i++]-=a);
    return;
}



int main()
{
    int *v;
    tf add, dec;
    add = &inc;
    dec = &sub;
    v=(int*)init();
    inc(2,v);
    sub(1,v);
    show(v);
    return 0;
}
