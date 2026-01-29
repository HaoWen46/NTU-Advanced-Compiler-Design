#include <stdio.h>

// Test Case 1: Simple Inlining
int multiply(int a, int b) {
    return a * b;
}

void test_simple_inlining() {
    int result = multiply(2, 3);
    printf("Simple Inlining Result: %d\n", result);
}

// Test Case 2: Recursive Function (No Inlining)
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

void test_recursive_function() {
    int result = factorial(5);
    printf("Recursive Function Result: %d\n", result);
}

// Test Case 3: Context-Sensitive Decisions
int compute_offset(int base, int offset) {
    return base + offset;
}

void test_context_sensitive() {
    int x = compute_offset(10, 5);
    int y = compute_offset(20, 7);
    printf("Context-Sensitive Results: %d, %d\n", x, y);
}

// Test Case 4: Mixed Function Calls
int add(int x, int y) {
    return x + y;
}

int subtract(int x, int y) {
    return x - y;
}

void test_mixed_calls() {
    int sum = add(15, 5);
    int diff = subtract(20, 10);
    printf("Mixed Calls Results: Sum=%d, Difference=%d\n", sum, diff);
}

// Test Case 5: Edge Case - Large Loop
int increment(int x) {
    return x + 1;
}

void test_large_loop() {
    int sum = 0;
    for (int i = 0; i < 10000; i++) {
        sum += increment(i);
    }
    printf("Large Loop Result: %d\n", sum);
}

int main() {
    test_simple_inlining();
    test_recursive_function();
    test_context_sensitive();
    test_mixed_calls();
    test_large_loop();
    return 0;
}