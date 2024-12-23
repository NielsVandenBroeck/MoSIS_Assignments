#include <math.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include "lsolve.h"

double getelm(double* matrix, const unsigned int i, const unsigned int j, const unsigned int m) {
    const unsigned n = m + 1;
    return *((matrix + i * n) + j);
}

void setelm(double* matrix, const unsigned i, const unsigned int j, const unsigned int m, double val) {
    const unsigned n = m + 1;
    *((matrix + i * n) + j) = val;
}

unsigned int argmax_abs(const unsigned int low, const unsigned int high, const unsigned int column, double* A) {
    unsigned int i_max = 0;
    double max_value = -1.0;  // computes the abs argmax, so always larger than -1
    for(unsigned int i = low; i < high; ++i) {
        double a = fabs(getelm(A, i, column, high));
        if(a > max_value) {
            max_value = a;
            i_max = i;
        }
    }
    return i_max;
}

void swrows(double* matrix, const unsigned int r1, const unsigned int r2, const unsigned int cols) {
    if(r1 == r2) { return; }
    double tmp;
    for(unsigned int i = 0; i < cols; ++i) {
        tmp = getelm(matrix, r2, i, cols - 1);
        setelm(matrix, r2, i, cols - 1, getelm(matrix, r1, i, cols - 1));
        setelm(matrix, r1, i, cols - 1, tmp);
    }
}

void lsolve(double* matrix, const unsigned int size) {
    const double eps = 1e-4;
    const unsigned int m = size;        // rows
    const unsigned int n = size + 1;    // columns
    unsigned int h = 0;                 // pivot row
    unsigned int k = 0;                 // pivot column

    unsigned int* swaps = malloc(2 * sizeof(unsigned int));
    int swaps_done = 0;

    while(h < m && k < n) {
        unsigned int i_max = argmax_abs(h, m, k, matrix);
        double elm = getelm(matrix, i_max, k, m);
        if(fabs(elm) <= eps) {
            // Go to the next column
            k += 1;
        } else {
            swrows(matrix, h, i_max, n);
            for(unsigned int i = k; i < n; ++i) {
                setelm(matrix, h, i, m, getelm(matrix, h, i, m) / elm);
            }

            for(unsigned int i = 0; i < m; ++i) {
                if(i == h) { continue; }
                double f = getelm(matrix, i, k, m) / getelm(matrix, h, k, m);
                setelm(matrix, i, k, m, 0.0);
                for(unsigned int j = k + 1; j < n; ++j) {
                    setelm(matrix, i, j, m, getelm(matrix, i, j, m) - getelm(matrix, h, j, m) * f);
                }
            }

            ++swaps_done;
            swaps = realloc(swaps, (2 * swaps_done) * sizeof(unsigned int));
            swaps[2 * (swaps_done - 1)] = h;
            swaps[2 * (swaps_done - 1) + 1] = i_max;

            h += 1;
            k += 1;
        }
    }

    for(int i = swaps_done - 1; i >= 0; --i) {
        swrows(matrix, swaps[i * 2], swaps[i * 2 + 1], n);
    }
    free(swaps);
}

double det(double* matrix, const unsigned int size) {
    unsigned int height = size - 1;

    if(size == 2) {
        double a00 = getelm(matrix, 0, 0, size);
        double a01 = getelm(matrix, 0, 1, size);
        double a10 = getelm(matrix, 1, 0, size);
        double a11 = getelm(matrix, 1, 1, size);
        return (a00 * a11) - (a01 * a10);
    }

    double total = 0.0;
    for(unsigned int fc = 0; fc < size; ++fc) {
        double** As = (double**)malloc(height * sizeof(double*));
        for(unsigned int i = 0; i < height; ++i) {
            As[i] = (double*)malloc(height * sizeof(double));
        }
        for(unsigned int r = 0; r < height; ++r) {
            for(unsigned int c = 0; c < fc; ++c) {
                As[r][c] = getelm(matrix, r + 1, c, height);
            }
            for(unsigned int c = fc; c < height; ++c) {
                As[r][c] = getelm(matrix, r + 1, c + 1, height);
            }
        }
        double sign = -1.0;
        if(fc % 2 == 1) {
            sign = 1.0;
        }
        double sub_det = det(*As, height);
        total += sign * getelm(matrix, 0, fc, height) * sub_det;

        for(unsigned int i = 0; i < height; ++i) {
            free(As[i]);
        }
        free(As);
    }
    return total;
}

void agloop(double* A, const unsigned int size, ...) {
    double D = det(A, size);
    if(fabs(D) < 1e-5) {
        printf("ERROR: SINGULAR MATRIX!\n");
        exit(1);
    }
    lsolve(A, size);

    // Read the arguments
    va_list list;
    va_start(list, size);
    for(unsigned int j = 0; j < size; ++j) {
        *va_arg(list, double*) = getelm(A, j, size, size);
    }
    va_end(list);
}
