# Book Assignment

A Python script to assign books to people based on preferences using the [Hungarian algorithm](https://cp-algorithms.com/graph/hungarian-algorithm.html).

## Inspiration and Local Bookstores

This project was inspired by a real event that took place in Italy, where book lovers emptied the storefront of local bookstores in a revolutionary act to support independent booksellers. You can read more about this event in the original news article here: [El País - Una revolución de bibliófilos vacía los escaparates de las librerías italianas](https://elpais.com/cultura/2024-12-22/una-revolucion-de-bibliofilos-vacia-los-escaparates-de-las-librerias-italianas.html).

Motivated by this initiative, this project aims to replicate the movement by leveraging mathematics and programming to optimally allocate books to people who participate in similar actions to support local bookstores.

### Local Bookstores Supported

The following local bookstores have contributed to the adoption and spread of this project:

#### La Carbonera
- Address: Carrer de Blai, 40, Sants-Montjuïc, 08004 Barcelona ([Google Maps](https://maps.app.goo.gl/h3Bqrgr1UbBkXVB57))
- Website: [carbonera.cat](https://carbonera.cat/)
- Online bookstore: [botiga.carbonera.cat](https://botiga.carbonera.cat/)

On February 8, 2025, the members of La Carbonera, eager for new readings and passionate about supporting their local bookstore, bought the entire storefront. To fairly distribute the books among themselves, they turned to this Python script for optimal allocation.

They used this scropt as follows:
```bash
# Download the official logo archive from La Carbonera's website
wget https://carbonera.cat/wp-content/uploads/2019/11/drive-download-20191025T083544Z-001.zip -O /tmp/la_carbonera_logos.zip

# Extract the images from the downloaded ZIP archive
unzip /tmp/la_carbonera_logos.zip -d /tmp/

# Run the script
python3 assign_books.py --drive_id FILE_ID \
  --debug \
  --ascii \
  --ascii_banner "Moltes gràcies equip de La Carbonera! Atentament, El Ministeri d'Exteriors de Sidrals Canoners" \
  --ascii_image /tmp/LA_CARBONERA_LOGO_NEG_OK.jpg
```

## Installation
```bash
pip3 install -r requirements.txt
```

Optional: install `jp2a` ([GitHub](https://github.com/cslarsen/jp2a)) to use additional `--ascii_image` and `--evil_image` options (see [Options](#options) below).

On Ubuntu:
```bash
sudo apt install jp2a
```

## Options

The script accepts the following command-line arguments:

| Argument        | Description | Required / Optional |
|----------------|-------------|---------------------|
| `--csv_file`   | Path to local CSV file | Required (one of `--csv_file` or `--drive_id`) |
| `--drive_id`   | Google Drive file ID | Required (one of `--csv_file` or `--drive_id`) |
| `--ascii`      | Enable ASCII art for assignments display | Optional |
| `--ascii_banner` | Custom message to display as ASCII art when `--ascii` is enabled | Optional |
| `--ascii_image` | Path to local JPG image to display as ASCII art when `--ascii` is enabled. It requires to install `jp2a` (https://github.com/cslarsen/jp2a) | Optional |
| `--evil_mode`  | Enable evil mode (what could possibly go wrong?) | Optional |
| `--evil_name`  | Name of evil mode's author to display as ASCII art when `--ascii` and `--evil_mode` are enabled | Optional |
| `--evil_banner` | Custom message to display as ASCII art when `--ascii` and `--evil_mode` are enabled | Optional |
| `--evil_image` | Path to local JPG image to display as ASCII art when `--ascii` and `--evil_mode` are enabled. It requires to install `jp2a` (https://github.com/cslarsen/jp2a) | Optional |
| `--debug`      | Enable debug mode | Optional |

## Usage Examples

- Assign books using a local CSV file:
  ```bash
  python3 assign_books.py --csv_file path/to/file.csv

- Assign books using a Google Drive file:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID

- Assign books using a Google Drive file and show debug info:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID --debug

- Assign books using a Google Drive file and enable ASCII art to display books assignment:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID --ascii

- Assign books using a Google Drive file, enable ASCII art to display books assignment with a custom banner at the end:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID --ascii --ascii_banner "Book Club Assignments"

- Assign books using a Google Drive file, enable ASCII art to display books assignment with a custom image at the end:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID --ascii --ascii_image path/to/image.jpg

- Assign books using a Google Drive file, enable evil mode, enable ASCII art to display books assignment with a custom banner at the end:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID \
    --evil_mode \
    --ascii \
    --ascii_banner "Book Club Assignments"

- Assign books using a Google Drive file, enable evil mode, enable ASCII art to display books assignment with a custom evil author and banner at the end:
  ```bash
  python3 assign_books.py --drive_id YOUR_FILE_ID \
    --evil_mode \
    --ascii \
    --evil_name "Chaos Demon" \
    --evil_banner "Chaos Mode Activated"

- Show help:
  ```bash
  python3 assign_books.py -h

- If neither `--csv_file` nor `--drive_id` is provided, the script will display an error message:
  ```bash
  python3 assign_books.py
  usage: assign_books.py [-h] [--csv_file CSV_FILE] [--drive_id DRIVE_ID] [--ascii] [--ascii_banner ASCII_BANNER]
                         [--ascii_image ASCII_IMAGE] [--evil_mode] [--evil_name EVIL_NAME] [--evil_banner EVIL_BANNER]
                         [--evil_image EVIL_IMAGE] [--debug]
  assign_books.py: error: You must provide either --csv_file or --drive_id.

## Conditions of Use
1. Each person must rate the books based on their preferences, with a score of 10 being the highest (strongly desires the book), and a score of 0 or an empty cell meaning they do not want the book.
2. The number of people cannot exceed the number of books.
3. Each person receives exactly one book.
4. When evil mode (`--evil_mode`) is enabled:
   * Preference scores are randomized and not processed from the provided CSV data.
   * Preference scores are not converted scores into costs (Hungarian algorithm minimizes cost).

## Algorithm
The Hungarian algorithm is applied through the function `linear_sum_assignment()` ([documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html())) from the `scipy.optimize` module.

## CSV File Format
The CSV file should contain preference scores for book assignments. The script processes the file as follows:
- The first two columns are ignored (they contain book prices without and with discount).
- The last column is ignored (it contains the total number of people).
- The last two rows are ignored (they display summary information about books and their costs).

### Example CSV Format
| Books      | Original Price | Discounted Price | Person1 | Person2 | Person3 | Person4 | Person5 | Person6 | Person7 | Person8 | Person9 | Person10 | 10 |
|------------|----------------|------------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----|
| Book1      | 20.00          | 19.00            | 7       | 3       | 8       | 2       | 9       | 6       | 4       | 1       | 10      | 5        |    |
| Book2      | 25.00          | 23.75            | 5       | 9       | 3       | 8       | 2       | 7       | 6       | 10      | 4       | 1        |    |
| Book3      | 18.00          | 17.10            | 1       | 6       | 7       | 9       | 5       | 8       | 3       | 4       | 2       | 10       |    |
| Book4      | 22.00          | 20.90            | 4       | 8       | 1       | 10      | 6       | 2       | 9       | 7       | 3       | 5        |    |
| Book5      | 30.00          | 28.50            | 10      | 2       | 5       | 3       | 7       | 9       | 8       | 6       | 1       | 4        |    |
| Book6      | 27.00          | 25.65            | 3       | 7       | 10      | 6       | 4       | 5       | 1       | 2       | 8       | 9        |    |
| Book7      | 15.00          | 14.25            | 9       | 5       | 2       | 7       | 8       | 3       | 6       | 4       | 10      | 1        |    |
| Book8      | 24.00          | 22.80            | 6       | 10      | 4       | 5       | 1       | 7       | 2       | 3       | 9       | 8        |    |
| Book9      | 21.00          | 19.95            | 2       | 1       | 9       | 4       | 10      | 6       | 5       | 8       | 7       | 3        |    |
| Book10     | 19.00          | 18.05            | 8       | 4       | 6       | 1       | 3       | 10      | 7       | 9       | 5       | 2        |    |
| **Summary**    |                |                  |         |         |         |         |         |         |         |         |         |          |    |
| **Total Cost** | **221.00**         | **209.95**           |         |         |         |         |         |         |         |         |         |          |    |

### Example CSV file
```bash
Books,Original Price,Discounted Price,Person1,Person2,Person3,Person4,Person5,Person6,Person7,Person8,Person9,Person10,10
Book1,20.00,19.00,7,3,8,2,9,6,4,1,10,5,10
Book2,25.00,23.75,5,9,3,8,2,7,6,10,4,1,10
Book3,18.00,17.10,1,6,7,9,5,8,3,4,2,10,10
Book4,22.00,20.90,4,8,1,10,6,2,9,7,3,5,10
Book5,30.00,28.50,10,2,5,3,7,9,8,6,1,4,10
Book6,27.00,25.65,3,7,10,6,4,5,1,2,8,9,10
Book7,15.00,14.25,9,5,2,7,8,3,6,4,10,1,10
Book8,24.00,22.80,6,10,4,5,1,7,2,3,9,8,10
Book9,21.00,19.95,2,1,9,4,10,6,5,8,7,3,10
Book10,19.00,18.05,8,4,6,1,3,10,7,9,5,2,10
Summary,,,,,,,,,,,,,
Total Cost,221.00,209.95,,,,,,,,,,,
```

## Running Tests

To run the test suite, use the following command:

```bash
pytest-3 tests/
```

## License
This project is licensed under the MIT License.
