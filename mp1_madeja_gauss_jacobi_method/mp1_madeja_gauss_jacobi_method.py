import re

def gauss_jacobi_main():
    def collect_equations():
        equations = []
        print("Enter three equations in the format ax+by+cz=d:")
        for _ in range(3):
            equation = input().strip()
            equations.append(equation)
        return equations

    def extract_coefficients(eq):
        # Match any combination of digits (including optional sign) followed by a variable (x, y, z)
        matches = re.findall(r'([+-]?\d+)[xyz]', eq)
        coefficients = [int(match) if match else 1 for match in matches]

        # Extract the constant term
        constant_match = re.search(r'=([+-]?\d+)$', eq)
        constant = int(constant_match.group(1)) if constant_match else 0

        return coefficients, constant

    def arrange_equations(equations, x_coefficients, y_coefficients, z_coefficients):
        arranged_equations = []

        # Find the dominant variable for each coefficient list
        dominant_x = max(x_coefficients, key=abs)
        dominant_y = max(y_coefficients, key=abs)
        dominant_z = max(z_coefficients, key=abs)

        # Find the index of the dominant variable in each list
        idx_x = x_coefficients.index(dominant_x)
        idx_y = y_coefficients.index(dominant_y)
        idx_z = z_coefficients.index(dominant_z)

        # Assign equations based on the dominant variables
        arranged_equations.append(equations[idx_x])
        arranged_equations.append(equations[idx_y])
        arranged_equations.append(equations[idx_z])

        # Remove selected equations from the original list
        remaining_equations = [eq for eq in equations if eq not in arranged_equations]

        return tuple(arranged_equations), remaining_equations

    def iterative_formulas(arranged_equations):
        (a, b, c), d = extract_coefficients(arranged_equations[0])
        (e, f, g), h = extract_coefficients(arranged_equations[1])
        (i, j, k), l = extract_coefficients(arranged_equations[2])

        ea = float(input("\nEnter the absolute error: "))
        dp = int(input("Enter the number of decimal places for rounding: "))

        print("\nIterative Formulas:")
        print(f"x_new = [({d})-({b})y-({c})z]/({a})]")
        print(f"y_new = [({h})-({e})x-({g})z]/({f})]")
        print(f"z_new = [({l})-({i})x-({j})y]/({k})]")
        return a, b, c, d, e, f, g, h, i, j, k, l, ea, dp

    def gauss_jacobi(a, b, c, d, e, f, g, h, i, j, k, l, x, y, z):
        x_new = (d - b*y - c*z) / a
        y_new = (h - e*x - g*z) / f
        z_new = (l - i*x - j*y) / k
        return x_new, y_new, z_new

    def absolute_errors(x_new, y_new, z_new, x, y, z):
        eax = abs(x_new - x)
        eay = abs(y_new - y)
        eaz = abs(z_new - z)
        return eax, eay, eaz

    equations = collect_equations()

    # Extract coefficients for x, y, z, and the constant from all equations
    all_coefficients = [extract_coefficients(eq) for eq in equations]

    # Unpack coefficients for x, y, z, and constants
    x_coefficients, y_coefficients, z_coefficients = zip(*[coefficients for coefficients, _ in all_coefficients])
    constants = [constant for _, constant in all_coefficients]

    # Arrange equations based on the dominant variables
    arranged_equations, remaining_equations = arrange_equations(equations, x_coefficients, y_coefficients, z_coefficients)

    # Display arranged equations
    print("\nArranged equations:")
    print("Equation 1:", arranged_equations[0])
    print("Equation 2:", arranged_equations[1])
    print("Equation 3:", arranged_equations[2])

    # Unpack coefficients and constants for a to l from arranged equations
    a, b, c, d, e, f, g, h, i, j, k, l, ea, dp = iterative_formulas(arranged_equations)

    # Initial guesses for x, y, z
    x, y, z = 0, 0, 0

    # Table headers
    print("\nTabulated Results:")
    print(f"{'Iter':<8} | {'x':<8} | {'y':<8} | {'z':<8} | {'x_new':<8} | {'y_new':<8} | {'z_new':<8} | {'Eax':<8} | {'Eay':<8} | {'Eaz':<8}")
    print("-" * 110)

    iteration = 1
    while True:
        x_new, y_new, z_new = gauss_jacobi(a, b, c, d, e, f, g, h, i, j, k, l, x, y, z)
        eax, eay, eaz = absolute_errors(x_new, y_new, z_new, x, y, z)

        # Display values in tabular form
        row_data = [iteration, round(x, dp), round(y, dp), round(z, dp),
                    round(x_new, dp), round(y_new, dp), round(z_new, dp),
                    round(eax, dp), round(eay, dp), round(eaz, dp)]

        row_str = "| ".join(f"{val:<9.{dp}f}" if isinstance(val, float) else f"{val:<9}" for val in row_data)

        print(row_str)

        # Check for convergence
        if all(error <= ea for error in [eax, eay, eaz]):
            break

        # Update values for the next iteration
        x, y, z = x_new, y_new, z_new
        iteration += 1

    print("\nRoots:")
    print(f"x = {x_new:.{dp}f}")
    print(f"y = {y_new:.{dp}f}")
    print(f"z = {z_new:.{dp}f}")
    print(f"\nIterations: {iteration}")
    print("\n")

if __name__ == "__main__":
    gauss_jacobi_main()
