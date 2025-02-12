import unittest
import pandas as pd
import numpy as np
from book_assignment.assign_books import assign_books, process_data, load_data
import os

class TestAssignBooks(unittest.TestCase):
    def test_assign_books(self):
        books = ['Book1', 'Book2', 'Book3', 'Book4', 'Book5', 'Book6', 'Book7', 'Book8', 'Book9', 'Book10']
        people = ["Person1", "Person2", "Person3", "Person4", "Person5", "Person6", "Person7", "Person8", "Person9", "Person10"]
        preferences = np.random.randint(0, 11, size=(len(books), len(people)))
        assignments = assign_books(books, people, preferences, args=type('', (), {'debug': False, 'evil_mode': False})())

        # Verify that each person receives exactly one book
        self.assertEqual(len(assignments), len(people))
        self.assertTrue(all(person in assignments for person in people))

class TestAssignBooksFromCSV(unittest.TestCase):
    def setUp(self):
        data = [
            ["Books", "Original Price", "Discounted Price", "Person1", "Person2", "Person3", "Person4", "Person5", "Person6", "Person7", "Person8", "Person9", "Person10", "10"],
            ["Book1", 20.00, 19.00, 7, 3, 8, 2, 9, 6, 4, 1, 10, 5, 10],
            ["Book2", 25.00, 23.75, 5, 9, 3, 8, 2, 7, 6, 10, 4, 1, 10],
            ["Book3", 18.00, 17.10, 1, 6, 7, 9, 5, 8, 3, 4, 2, 10, 10],
            ["Book4", 22.00, 20.90, 4, 8, 1, 10, 6, 2, 9, 7, 3, 5, 10],
            ["Book5", 30.00, 28.50, 10, 2, 5, 3, 7, 9, 8, 6, 1, 4, 10],
            ["Book6", 27.00, 25.65, 3, 7, 10, 6, 4, 5, 1, 2, 8, 9, 10],
            ["Book7", 15.00, 14.25, 9, 5, 2, 7, 8, 3, 6, 4, 10, 1, 10],
            ["Book8", 24.00, 22.80, 6, 10, 4, 5, 1, 7, 2, 3, 9, 8, 10],
            ["Book9", 21.00, 19.95, 2, 1, 9, 4, 10, 6, 5, 8, 7, 3, 10],
            ["Book10", 19.00, 18.05, 8, 4, 6, 1, 3, 10, 7, 9, 5, 2, 10],
            ["Summary", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["Total Cost", 221.00, 209.95, "", "", "", "", "", "", "", "", "", "", ""]
        ]

        df = pd.DataFrame(data)
        self.test_csv_path = "tests/test_data.csv"
        df.to_csv(self.test_csv_path, index=False, header=False)

    def test_assign_books_from_csv(self):
        df = load_data(type('', (), {'csv_file': self.test_csv_path, 'drive_id': None})())
        books, people, preferences = process_data(df, type('', (), {'debug': False, 'evil_mode': False})())
        assignments = assign_books(books, people, preferences, type('', (), {'debug': False, 'evil_mode': False})())

        # Verify that each person receives exactly one book
        self.assertEqual(len(assignments), len(people))
        self.assertTrue(all(person in assignments for person in people))

    def tearDown(self):
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

if __name__ == "__main__":
    unittest.main()

