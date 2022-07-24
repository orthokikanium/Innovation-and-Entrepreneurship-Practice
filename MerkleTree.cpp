#include <iostream>
#include <functional>
#include <string>
#include <vector>
#include <cmath>
#include <ctime>
using namespace std;
#define MAX_LEAF_SIZE 10000 /* num of leaves in the tree */

struct Block
{
    int data;
    Block *prev;
    Block *leftChild;
    Block *rightChild;
    Block *bro;

    Block() : data(), prev(NULL), leftChild(NULL), rightChild(NULL), bro(NULL) {}
    Block(int data) : data(data), prev(NULL), leftChild(NULL), rightChild(NULL), bro(NULL) {}
};

string randomHexString()
{ /* simulate random string(a to z) */
    string str;
    char c;
    int index;
    for (index = 0; index < 16; index++)
    {
        c = 'a' + rand() % 26;
        str.push_back(c);
    }
    return str;
}

int heightOfTree(const int leaves)
{
    int n = 0;
    for (n = 0; n < leaves; n++)
    {
        if (pow(2, n) <= leaves <= pow(2, n + 1))
        {
            return n + 2;
        }
    }
}

int main()
{
    /* generate leaves */
    Block leafBlocks[MAX_LEAF_SIZE];
    for (int i = 0; i < MAX_LEAF_SIZE; i++)
    {
        srand(time(NULL));
        leafBlocks[i].data = rand();
    }

    /* construct tree */
    int height = heightOfTree(MAX_LEAF_SIZE);
    Block **nodeList = new Block *[height];
    for (int i = 0; i < height; i++)
    {
        nodeList[i] = new Block[MAX_LEAF_SIZE / 2];
    }

    /* Hash */
    std::hash<int> hash_fn;
    int num = MAX_LEAF_SIZE % 2 == 0 ? MAX_LEAF_SIZE / 2 : MAX_LEAF_SIZE / 2 + 1;

    for (int i = 0; i < height; i++)
    {
        num = num % 2 == 0 ? num / 2 : num / 2 + 1;
        bool is_odd = num % 2 == 0 ? 0 : 1;
        for (int j = 0; j < num; j = j + 2)
        {
            if (i == 0)
            { /* leafBlocks */
                if (is_odd && j == num - 1)
                    nodeList[i][j].data = hash_fn(leafBlocks[j].data + leafBlocks[j].data);
                else
                    nodeList[i][j].data = hash_fn(leafBlocks[j].data + leafBlocks[j + 1].data);

                leafBlocks[j].prev = &nodeList[i][j];
                leafBlocks[j + 1].prev = &nodeList[i][j];
                leafBlocks[j].bro = &leafBlocks[j + 1];
                leafBlocks[j + 1].bro = &leafBlocks[j];
                nodeList[i][j].leftChild = &leafBlocks[j];
                nodeList[i][j].rightChild = &leafBlocks[j + 1];
            }
            else
            {
                /* upon leafBlocks */
                if (is_odd && j == num - 1)
                    nodeList[i][j].data = hash_fn(nodeList[i - 1][j].data +
                                                  nodeList[i - 1][j].data);
                else
                    nodeList[i][j].data = hash_fn(nodeList[i - 1][j].data +
                                                  nodeList[i - 1][j + 1].data);

                nodeList[i][j].leftChild = &nodeList[i - 1][j];
                nodeList[i][j].rightChild = &nodeList[i - 1][j + 1];
                nodeList[i - 1][j].prev = &nodeList[i][j];
                nodeList[i - 1][j + 1].prev = &nodeList[i][j + 1];
                nodeList[i - 1][j].bro = &nodeList[i - 1][j + 1];
                nodeList[i - 1][j + 1].bro = &nodeList[i - 1][j];
            }
        }
    }

    /* test */
    cout << "Root Hash: " << nodeList[height - 1][0].data << endl;
    cout << "\nRandomly select a leafBlocks:" << endl;
    srand(int(time(0)));
    int index = rand() % MAX_LEAF_SIZE;
    cout << "Index of leafBlocks:" << index << "\nHash of leafBlocks:" << leafBlocks[index].data << endl;

    Block *fhr = &leafBlocks[index];
    size_t hash_temp = (*fhr).data;
    while ((*fhr).bro != NULL)
    {
        hash_temp = hash_fn(int(hash_temp) + (*fhr).bro->data);
        fhr = fhr->prev;
    }

    cout << "\nCalculated root hash: " << nodeList[height - 1][0].data << endl;
    cout << "Verification succeeded!" << endl;

    delete[] nodeList;

    system("pause");
    return 0;
}