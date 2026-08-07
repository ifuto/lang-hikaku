#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define CAP (1u << 21)
#define NKEYS 1000000

typedef struct {
    char key[16];
    long long val;
    unsigned char used;
} Ent;

static Ent t[CAP];

static uint64_t fnv1a(const char *s) {
    uint64_t h = 14695981039346656037ULL;
    while (*s) {
        h ^= (unsigned char)*s++;
        h *= 1099511628211ULL;
    }
    return h;
}

int main(void) {
    for (int i = 0; i < NKEYS; i++) {
        char k[16];
        snprintf(k, sizeof k, "k%07d", i);
        size_t p = fnv1a(k) & (CAP - 1);
        while (t[p].used) p = (p + 1) & (CAP - 1);
        t[p].used = 1;
        strcpy(t[p].key, k);
        t[p].val = i;
    }
    printf("%d\n", NKEYS);
    return 0;
}
