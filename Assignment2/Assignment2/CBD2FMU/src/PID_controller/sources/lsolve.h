#ifndef LSOLVE
#define LSOLVE

/**
 *  Obtains an element from a 2D array matrix, using pointers.
 *  This is mainly a helper function.
 *
 *  @param  matrix  An address to an (NxN+1) matrix, which is
 *                  to be constructed as a 2D array.
 *  @param  i       The row index of the element to obtain.
 *  @param  j       The column index of the element to obtain.
 *  @param  m       The amount of rows for the input matrix.
 **/
double getelm(double* matrix, const unsigned int i, const unsigned int j, const unsigned int m);

/**
 *  Sets an element in a 2D array matrix, using pointers.
 *  This is mainly a helper function.
 *
 *  @param  matrix  An address to an (NxN+1) matrix, which is
 *                  to be constructed as a 2D array.
 *  @param  i       The row index of the element to set.
 *  @param  j       The column index of the element to set.
 *  @param  m       The amount of rows for the input matrix.
 *  @param  val     The new value for the element.
 **/
void setelm(double* matrix, const unsigned int i, const unsigned int j, const unsigned int m, double val);

/**
 *  Computes the row index that yields the highest absolute value.
 *  This is mainly a helper function.
 *
 *  @param  low     The minimal row index to return.
 *  @param  high    The maximal row index to return.
 *  @param  A       An address to an (NxN+1) matrix, which is
 *                  to be constructed as a 2D array.
 **/
unsigned int argmax_abs(const unsigned int low, const unsigned int high, const unsigned int column, double* A);

/**
 *  Solves a system of equations linearly, by using matrices
 *  and Gauss-Jordan Elimination. Only works for N equations
 *  and N unknowns.
 *
 *  @param  matrix  An address to an (NxN+1) matrix, which is
 *                  to be constructed as a 2D array.
 *  @param  size    The amount of rows for the input matrix N.
 **/
void lsolve(double* matrix, const unsigned int size);

/**
 *  Computes the determinant of the matrix.
 *
 *  @param  matrix  An address to an (NxN) matrix, which is
 *                  to be constructed as a 2D array.
 *  @param  size    The amount of rows for the input matrix N.
 **/
double det(double* matrix, const unsigned int size);

/**
 *  Helper function to linearly solve algebraic loops.
 *  This first checks if the block matrix is not singular,
 *  after which it solves the equations w.r.t. Gauss-Jordan.
 *  Finally, the resulting matrix is automatically stored in
 *  the corresponding variables.
 *
 *  @param  A       An address to an (NxN+1) matrix, which is
 *                  to be constructed as a 2D array.
 *  @param  size    The amount of rows for the input matrix N.
 *  @param  ...     An undefined amount of arguments that refer
 *                  to the variables in which the data must be
 *                  stored in the end.
 **/
void agloop(double* A, const unsigned int size, ...);

#endif
