from naginterfaces.library import mv
import numpy as np

matrix = 'Var-Covar'
std = 'Eigenvalue'
x = np.array([
    [7.0, 4.0, 3.0],
    [4.0, 1.0, 8.0],
    [6.0, 3.0, 5.0],
    [8.0, 6.0, 1.0],
    [8.0, 5.0, 7.0],
    [7.0, 2.0, 9.0],
    [5.0, 3.0, 3.0],
    [9.0, 5.0, 8.0],
    [7.0, 4.0, 5.0],
    [8.0, 2.0, 2.0],
])

x_clean = x[:,:2]
x_clean = np.ascontiguousarray(x[:, :2])

isx = [1, 1]

# Initialize s to 0.0, as matrix /= 'S'
s = [0.0, 0.0]

# Calculate NVAR
nvar = isx.count(1)

# The statistics of principal component analysis
e = mv.prin_comp(matrix, std, x_clean, isx, s, nvar)
e = np.matrix(e)

print(' Eigenvalues  Percentage  Cumulative       Chisq          DF'
      '         Sig'
     )
print('               variation   variation')
print('[')
for i in range(e.shape[0]):
    print(
        '  ' +
        ', '.join(['{:10.4f}']*e.shape[1]).format(*e[i, :])
    )
print(']')