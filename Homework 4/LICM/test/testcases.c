#include <stdio.h>

void basicTest(int n, int a, int b) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        int x = a + b;  // Invariant
        sum += x * i;
    }
    printf("Basic Test Sum: %d\n", sum);
}

void nestedTest(int n, int m, int a) {
    int product = 1;
    for (int i = 0; i < n; i++) {
        int constant = a + i;  // Outer loop invariant
        for (int j = 0; j < m; j++) {
            product *= constant * j;  // Inner loop depends on j
        }
    }
    printf("Nested Test Product: %d\n", product);
}

void conditionalTest(int n, int c) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (c > 0) {
            int temp = c * 2;  // Invariant when c > 0
            count += temp;
        }
    }
    printf("Conditional Test Count: %d\n", count);
}

void nonInvariantTest(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        int x = rand();  // Not invariant due to randomness
        sum += x;
    }
    printf("Non-Invariant Test Sum: %d\n", sum);
}

void multiThreadTest(int n, int *arr) {
    int fixedValue = arr[0];  // Invariant unless threads modify arr[0]
    for (int i = 0; i < n; i++) {
        arr[i] = fixedValue + i;
    }
    printf("Multi-thread Test: Array Updated\n");
}

int main() {
    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    basicTest(10, 5, 3);
    nestedTest(5, 3, 2);
    conditionalTest(10, 4);
    nonInvariantTest(10);
    multiThreadTest(10, arr);
    return 0;
}
