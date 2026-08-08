#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(void){
    int size=10000000;
    int reps=10;
    char *s=malloc(size+1);
    memset(s,'a',size);
    s[size]='\0';
    long long total=0;
    for (int r=0;r<reps;r++){
        // reverse in place
        for (int i=0,j=size-1;i<j;i++,j--){ char t=s[i]; s[i]=s[j]; s[j]=t; }
        total+=size;
    }
    printf("%lld\n", total);
    free(s);
    return 0;
}
