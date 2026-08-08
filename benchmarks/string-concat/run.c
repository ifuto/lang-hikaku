#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main(void){
    int N=100000;
    size_t total=0;
    char *s = malloc(1);
    s[0]='\0';
    size_t cap=1;
    size_t len=0;
    for (int i=0;i<N;i++){
        if (len+2>cap){ cap*=2; s=realloc(s,cap); }
        s[len]='a';
        s[len+1]='\0';
        len++;
    }
    printf("%zu\n", len);
    free(s);
    return 0;
}
