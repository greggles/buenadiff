from bs4 import BeautifulSoup
import csv
from lxml import html

def html_distill_and_save(directory_path, filename, xpath_expression):
    """
    Opens an HTML file, converts it to plain text using BeautifulSoup,
    and returns the plain text.

    Args:
        directory_path: The folder to work in (open and save files).
        filename: The path to the HTML file.
        xpath_expression: The XPath expression to select the content element(s).

    Returns:
        The plain text version of the HTML, or None if an error occurs.
    """
    full_filename = directory_path + filename + '.html'
    try:
        with open(full_filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Source HTML file not found: {full_filename}")
        return None
    except Exception as e:
        print(f"Error: problem reading file: {e}")
        return None

    try:
        tree = html.fromstring(html_content)
        elements = tree.xpath(xpath_expression)

        if not elements:
            print(f"Error: No elements found matching XPath: {xpath_expression}")
            return None

        # Handle multiple elements returned by XPath.
        extracted_text = ""
        extracted_html = ""
        for element in elements:
            # Convert lxml element to string for BeautifulSoup and focused diff.
            element_string = html.tostring(element, encoding='unicode')

            extracted_html += element_string + "\n"
            soup = BeautifulSoup(element_string, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            # Add a newline between multiple matches.
            extracted_text += text + "\n"

        # Remove trailing newline while writing it out.
        write_text_to_file(extracted_text.strip(), directory_path + filename + ".txt")
        write_text_to_file(extracted_html.strip(), directory_path + filename + "-distilled.html")

    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None

def get_files_from_csv(file_path):
    """
    Opens a CSV file and prints each row.

    Args:
        file_path: The path to the CSV file.
    """
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            data = []

            for line in csv.DictReader(csvfile):
                data.append(line)
            return data
    except FileNotFoundError:
        print(f"Error: CSV file not found: {file_path}")
    except csv.Error as e:
        print(f"CSV Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_text_to_file(text, file_path):
    """
    Writes text to a file.

    Args:
        text: the text to write out.
        file_path: file path and name to write out.

    Returns:

    """
    try:
        with open(file_path, 'w') as writer:
            writer.write(text)
    except FileNotFoundError:
        print(f"Error: Path to write file not found: {file_path}")
    except csv.Error as e:
        print(f"CSV Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    csvpath = 'url_data.csv'
    paths = ['reference/', 'working-copy/']

    for folder_path in paths:

        # CSV with 3 columns: URL, FILENAME to save it as, XPATH to contents to compare.
        url_data = get_files_from_csv(csvpath)

        # Example xpath to get both the main element and the jumbotron div element as they are siblings.
        # .//*[self::main or @class='jumbotron']

        for row in url_data:
            print(f"Processing files in {folder_path} for {row['URL']}")
            html_distill_and_save(folder_path, row['FILENAME'], row['XPATH'])
