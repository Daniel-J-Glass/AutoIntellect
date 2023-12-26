class Library:
    """
    A simple library management system.
    """

    def __init__(self):
        """
    Initializes the library with an empty list of books.
    """
        self.books = []

    def add_book(self, title, author):
        """
    Adds a new book to the library.
    
    Args:
        title (str): The title of the book.
        author (str): The author of the book.
    """
        # Check if the book already exists in the library
        for book in self.books:
            if book['title'] == title and book['author'] == author:
                return # Book already exists
    
        # Add the new book
        self.books.append({'title': title, 'author': author})

    def is_book_available(self, title):
        """
    Checks if a book is available in the library.
    
    Args:
        title (str): The title of the book to check.
    
    Returns:
        bool: True if the book is available, False otherwise.
    """
        for book in self.books:
            if book['title'] == title:
                return True
        return False

    @classmethod
    def create_from_book_list(cls, book_list):
        """
    Creates a new Library instance from a list of books.
    
    Args:
        book_list (list of tuple): A list where each tuple contains the title and author of a book.
    
    Returns:
        Library: A new Library instance with the given books.
    """
        # Create a new Library instance
        library_instance = cls()
        # Add each book from the book_list to the library
        for title, author in book_list:
            library_instance.add_book(title, author)
        return library_instance

    def list_books(self):
        """
        Lists all the books in the library.

        Returns:
            list of tuple: A list where each tuple contains the title and author of a book.
        """

def calculate_sum(a, b):
    """Calculate the sum of two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The sum of the two numbers.
    """
    return a + b


def find_max(numbers):
    """Find the maximum number in a list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        int: The maximum number in the list.
    """
