# Calculus Essentials

## Derivatives

The derivative of a function $f(x)$ is defined as:

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

Some common derivatives:
- $\frac{d}{dx}(x^n) = nx^{n-1}$
- $\frac{d}{dx}(\sin x) = \cos x$
- $\frac{d}{dx}(e^x) = e^x$

## Integration

The fundamental theorem of calculus states:

$$
\int_{a}^{b} f(x) dx = F(b) - F(a)
$$

where $F'(x) = f(x)$.

## Taylor Series

Any function $f(x)$ can be expanded around $x = a$:

$$
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n
$$

For example, $e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}$.

## Partial Derivatives

For multivariable functions, we have $\frac{\partial f}{\partial x}$ and $\frac{\partial f}{\partial y}$.
