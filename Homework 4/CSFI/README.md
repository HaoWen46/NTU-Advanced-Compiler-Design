# LLVM Optimization Pass README

## Environment Setup

## Build Instructions

## Running the Pass

## Testing Instructions
```bash
clang -O0 -emit-llvm -S ./test/testcases.c -o test.ll
opt -inline -S test.ll -o output.ll