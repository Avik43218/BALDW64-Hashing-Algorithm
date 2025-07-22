"""
This program uses a list of 12 variables, H, in the compression loop and a list of 88 other
constants, K, for high entropy.

The 12 variables are named from a to l, and they are randomly chosen points from two 
mathematical equations: x^2 + y^2 = 256 and 9x^2 - 4y^2 = 36, the first one being a circle 
and the second one being a hyperbola.

The values of the list K are calculated from the value of Permitivity of Free Space, 
ε₀ = 8.8541878128e-12, by scaling it first and then offsetting the scaled value with integers
within the range 1 to 88.

Here's a simple implementation of the constant value calculation procedure.

"""

scaled = int(8.8541878128e-12 * (2**64))
constants = [(scaled ^ (i * 0xA5A5A5A5A5A5A5A5)) & 0xFFFFFFFFFFFFFFFF for i in range(1, 89)]

hex_str = '[' + ', '.join([hex(val) for val in constants]) + ']'
print(hex_str)
