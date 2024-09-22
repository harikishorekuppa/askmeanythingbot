import PyPDF2
import csv

def capitalize_first_letter(string):
    words = string.split()
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)

def remove_numbers(string):
    return ''.join([char for char in string if not char.isdigit()])

def parse_array(arr):
    item = capitalize_first_letter(remove_numbers(arr[0].split()[0]))
    description = capitalize_first_letter(" ".join(arr[1:3]))
    quantity = float(arr[3].replace(",", ""))  # Convert to float to handle decimal quantities
    price_unit = float(arr[5].replace(",", ""))  # Remove commas before converting to float
    if len(arr) == 8:
        price_total = float(arr[7].replace(",", ""))  # Remove commas before converting to float
    else:
        price_total = 0.0  # Default to 0.0 if price_total is not provided
    # Return the item name and values as a tuple
    return (f"{item} {description}", quantity, price_unit, price_total)

def sum_values_without_price_unit(parsed_lines):
    result = {}
    for item_name, quantity, price_unit, price_total in parsed_lines:
        if item_name not in result:
            result[item_name] = [0, price_unit, 0.0]  # Initialize [quantity, price_unit, price_total]
        result[item_name][0] += quantity  # Sum the quantity
        result[item_name][2] += price_total  # Sum the total price
    return result

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def write_to_csv(summed_values, csv_filename):
    # Write the CSV file with rounded values
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["item_name", "quantity", "price_unit", "price_total"])  # Write headers
        for item_name, values in summed_values.items():
            quantity, price_unit, price_total = values
            writer.writerow([item_name, f"{quantity:.2f}", f"{price_unit:.2f}", f"{price_total:.2f}"])

# Example usage:
pdf_path = "Aug17-Aug23.pdf"
csv_output = "SaleReport.csv"

extracted_text = extract_text_from_pdf(pdf_path)
split_lines = extracted_text.split("\n")

parsed_lines = []
for item in split_lines:
    if "Chicken" in item:
        if "bone" in item:
            item = item.replace(" bone ", " bone piece ")
        line = item.split(" ")
        parsed_lines.append(parse_array(line))

# Sum the values of each item (without adding up price_unit)
summed_values = sum_values_without_price_unit(parsed_lines)

# Write the result as a CSV file
write_to_csv(summed_values, csv_output)

print(f"CSV created: {csv_output}")
