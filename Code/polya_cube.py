# necessary to use conda environment with sympy installed
# to run: ./cenv/bin/python ./Code/polya_cube.py 

import sympy

x = sympy.Symbol('x')
y = sympy.Symbol('y')

res = sympy.expand( ((x+y)**8  +  6 * (x+y)**4 * (x**2 + y**2)**2 + 8 * (x+y)**2 * (x**3 + y**3)**2 + 13 * (x**2 + y**2)**4 + 8 * (x**2 + y**2) * (x**6 + y**6) + 12 * (x**4 + y**4)**2) / 48 )
print(res)