class LibraryManager:
    def __init__(self):
        # Initialize empty dictionaries for books and loans
        self.books = {}
        self.loans = {}
        self.book_id_counter = 1
        self.loan_id_counter = 1

    def add_book(self, title: str, author: str, quantity: int) -> int:
        """Add a new book to the library"""
        book_data = (title, author, quantity, quantity)  # (title, author, total_quantity, available)
        self.books[self.book_id_counter] = book_data
        self.book_id_counter += 1
        return self.book_id_counter - 1

    def get_book(self, book_id: int) -> tuple:
        """Get book information by ID"""
        return self.books.get(book_id)

    def get_all_books(self) -> dict:
        """Get all books in the library"""
        return self.books

    def remove_book(self, book_id: int) -> bool:
        """Remove a book from the library"""
        if book_id in self.books:
            del self.books[book_id]
            return True
        return False

    def borrow_book(self, book_id: int, borrower_name: str, borrow_date: str, return_date: str) -> int:
        """Borrow a book from the library"""
        if book_id in self.books:
            title, author, quantity, available = self.books[book_id]
            if available > 0:
                # Update book availability
                self.books[book_id] = (title, author, quantity, available - 1)
                # Create loan record
                loan_data = (book_id, borrower_name, borrow_date, return_date)
                self.loans[self.loan_id_counter] = loan_data
                self.loan_id_counter += 1
                return self.loan_id_counter - 1
        return -1

    def return_book(self, loan_id: int) -> bool:
        """Return a borrowed book"""
        if loan_id in self.loans:
            book_id = self.loans[loan_id][0]
            title, author, quantity, available = self.books[book_id]
            # Update book availability
            self.books[book_id] = (title, author, quantity, available + 1)
            # Remove loan record
            del self.loans[loan_id]
            return True
        return False

    def get_all_loans(self) -> dict:
        """Get all active loans"""
        return self.loans

    def search_books(self, query: str) -> list:
        """Search books by title or author"""
        results = []
        query = query.lower()
        for book_id, (title, author, quantity, available) in self.books.items():
            if query in title.lower() or query in author.lower():
                results.append((book_id, (title, author, quantity, available)))
        return results
