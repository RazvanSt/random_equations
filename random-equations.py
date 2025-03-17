import random
import sys
import argparse
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
    parser = argparse.ArgumentParser(description="Generate random math equations in a PDF.")
    parser.add_argument("num_equations", type=int, help="The number of equations to generate.")
    parser.add_argument("-m", "--max_number", type=int, default=100, help="The maximum number to use in the equations (default: 100).")

    args = parser.parse_args()

    if args.num_equations < 1:
        print("Error: Number of equations must be a positive integer.")
        sys.exit(1)
    
    if args.max_number < 0:
        print("Error: max_number must be a non-negative integer.")
        sys.exit(1)

    equations = generate_equations(args.num_equations, args.max_number)

    # Create a unique filename based on the current date and time
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")
    output_filename = f"equations_{timestamp}.pdf"

    # Create PDF
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        title="Random Math Equations",
        leftMargin=0.5 * inch,  # Smaller left margin
        rightMargin=0.5 * inch,  # Smaller right margin
        topMargin=0.5 * inch,    # Smaller top margin
        bottomMargin=0.5 * inch, # Smaller bottom margin
    )
    styles = getSampleStyleSheet()
    Story = []

    # Add the text "Please solve these equations:"
    header_text = "Please solve these equations:"
    header_style = styles["Heading2"]  # You can choose a different style if you prefer
    header = Paragraph(header_text, header_style)
    Story.append(header)
    Story.append(Spacer(1, 0.2 * inch))  # Add some space between the header and the table

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

    print(f"Equations written to {output_filename}")