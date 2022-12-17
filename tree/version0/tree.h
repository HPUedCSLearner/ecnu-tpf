#ifndef __TREE__
#define __TREE__

#include <unistd.h>
#include <stdlib.h>

typedef int Val;
typedef struct node {
    struct node* l, *r;
    Val data;
} Node, *Pnode;

Pnode find(Pnode root, Val val) {

}
Pnode insert(Pnode root, Val val) {
    if (root == NULL) {
        root = (Pnode)malloc(sizeof(Node));
        root->data = val;
        root->l = NULL;
        root->r = NULL;
        return root;
    }

    if (val > root->data) {
        root->r = insert(root->r, val);
    // } else if (val == root->data) {
    //     root->data += val;
    } else {
        root->l = insert(root->l, val);
    }
    return root;

}
#endif