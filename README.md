<img src = "https://github.com/mike006322/PolynomialCalculator/blob/master/logo.svg" height = 200>

# Polynomial Calculator
*A lightweight Computer Algebra System for polynomial computations over finite fields*


### Features

- Polynomial operations: +, -, *, /, %, gcd
- Supports polynomials over field of characteristic > 0 (A field of characteristic $$p > 0$$ is one where arithmetic behaves like modulo $$p$$, meaning $$p$$ copies of 1 add up to 0).
- Supports multi-variable polynomials
- Numerical solutions for single-variable polynomials
- Numerical solutions for systems of polynomials
- Support for constructing finite fields with polynomials
- Can find Gröbner basis for polynomial Ideals

### Usage

```Python
from core.polynomial import Polynomial
f = Polynomial('x+1')
g = Polynomial('x-1')
print('f = ', f)
print('g = ', g)
print('f*g = ', f*g)
print('solutions = ', (f*g).solve())
print('f*g/g = ', f*g/g)
print(division_string(f*g, f))
```
```
f = x + 1.0
g = x - 1.0
f*g = x^2 - 1.0
solutions = (1.0, -1.0)
f*g/g = x + 1.0
x^2 - 1.0 = (x - 1.0)*(x + 1.0) + (remainder:) 0
```
```Python
from core.polynomial import Polynomial 
from core.ideal import Ideal 
f = Polynomial("x^2y - 1") 
g = Polynomial("xy^2 - x") 
I = Ideal(f, g) 
g_b = I.groebner_basis() 
print("groebner basis =", *g_b)
```
```
groebner basis = -x^2 + y^2 - 10  
```
```Python
s = Polynomial("-x^2 + 10y")  
t = Polynomial("-y^2 + 10")  
J = Ideal(s, t)  
print("groebner basis =", *J.groebner_basis())  
print("J == I", J == I)
```
```
groebner basis = -y^2 + 10 - x^2 + y  
J == I True 
```

### Near-term goals:
- implement faster gcd algorithm
- implement lookup tables for primitive field elements
- implement 'factor' algorithm to factor over polynomials over finite fields
- option to plot single-variable polynomials
- create a GUI with Python

### Longer-term goals
- web GUI
- Mobile app

### Installation

```bash
git clone https://github.com/mike006322/PolynomialCalculator.git
cd PolynomialCalculator
pip install -r requirements.txt
```

### Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

Please make sure to update tests as appropriate.


### Similar projects:
- [SAGE](http://doc.sagemath.org/)

- [Sympy](https://github.com/sympy/sympy)


- [CoCa](http://cocoa.dima.unige.it/) written in C++ and CoCa language

- jasymchat - Computer Algebra System written in Java (won't run on phone, seems defunct)
