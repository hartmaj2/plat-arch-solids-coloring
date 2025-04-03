import re

# prepares polynomial for copy pasting into desmos
def poly_for_desmos(poly):
    poly = str(poly)
    print(poly)
    poly = poly.replace("*","") # replaces unnecessary multiplication symbols (desmos doesn't need them)
    poly = re.sub(r"\^(\d+)",r"^{\1}",poly) # groups the exponents so x^10 doesn't get parsed as x^1 * 0
    return poly

# converts polynomial sage object to a string and then replaces the necessary part with proper latex syntax and wraps in equation environment
def poly_to_latex(polynomial):
    str_with_wrong_superscripts =  str(polynomial).replace("*","") # replaces k*x^n by kx^n 
    str_with_maybe_bad_fractions =  re.sub(r'\^(\d+)',r"^{\1}",str_with_wrong_superscripts) # replaces x^123 by x^{123} for example
    str_with_good_fractions = re.sub(r'(\d+)/(\d+)',r"\\frac{\1}{\2}",str_with_maybe_bad_fractions) # replacs k/qx^n by \frac{k}{q}x^n
    return f"${str_with_good_fractions}$" # adds $...$ around and returns result