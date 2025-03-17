import random
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch  # Import inch for margins

def generate_equation(max_number):
    """
    Generates a simple addition or subtraction equation with numbers between 0 and max_number,
    formatted to three digits.

    Args:
        max_number: The maximum number that can be used in the equation.

    Returns:
        A string representing the equation.
    """
    num1 = random.randint(0, max_number)
    num2 = random.randint(0, max_number)
    operator = random.choice(['+', '-'])

    if operator == '-' and num1 < num2:
        num1, num2 = num2, num1  # Ensure the result is not negative

    return f"{num1:3d} {operator} {num2:3d} =       "

def generate_equations(num_equations, max_number):
    """
    Generates a specified number of equations.

    Args:
        num_equations: The number of equations to generate.
        max_number: The maximum number that can be used in the equations.

    Returns:
        A list of strings representing the equations.
    """
    return [generate_equation(max_number) for _ in range(num_equations)]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <number_of_equations>")
        sys.exit(1)

    try:
        num_equations = int(sys.argv[1])
        if num_equations < 1:
            raise ValueError
    except ValueError:
        print("Error: Number of equations must be a positive integer.")
        sys.exit(1)

    max_number = 100  # You can change this if needed

    equations = generate_equations(num_equations, max_number)

    # Create PDF
    doc = SimpleDocTemplate(
        "equations.pdf",
        pagesize=letter,
        leftMargin=0.5 * inch,  # Smaller left margin
        rightMargin=0.5 * inch,  # Smaller right margin
        topMargin=0.5 * inch,    # Smaller top margin
        bottomMargin=0.5 * inch, # Smaller bottom margin
    )
    styles = getSampleStyleSheet()
    Story = []

    # Prepare data for table
    data = []
    for i in range(0, len(equations), 2):
        row = [equations[i], equations[i + 1] if i + 1 < len(equations) else ""]
        data.append(row)

    # Create table
    table = Table(data, colWidths=[250, 250])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 14),  # Increased font size
    ]))

    Story.append(table)

    # Build PDF
    doc.build(Story)

    print("Equations written to equations.pdf")