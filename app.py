from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from library_manager import LibraryManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
library = LibraryManager()

@app.route('/')
def index():
    return render_template('index.html', 
                         books=library.get_all_books(),
                         loans=library.get_all_loans())

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        quantity = int(request.form['quantity'])
        
        book_id = library.add_book(title, author, quantity)
        flash(f'Book "{title}" added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/view_books')
def view_books():
    search_query = request.args.get('search', '')
    if search_query:
        books = library.search_books(search_query)
    else:
        books = library.get_all_books().items()
    return render_template('view_books.html', books=books, search_query=search_query)

@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    book_id = int(request.form['book_id'])
    borrower_name = request.form['borrower_name']
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    loan_id = library.borrow_book(book_id, borrower_name, borrow_date, return_date)
    if loan_id != -1:
        flash(f'Book borrowed successfully by {borrower_name}!', 'success')
    else:
        flash('Error borrowing book. Book might not be available.', 'error')
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    loan_id = int(request.form['loan_id'])
    if library.return_book(loan_id):
        flash('Book returned successfully!', 'success')
    else:
        flash('Error returning book.', 'error')
    return redirect(url_for('index'))

@app.route('/manage_loans')
def manage_loans():
    return render_template('manage_loans.html', loans=library.get_all_loans())

if __name__ == '__main__':
    # Add some sample books
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 3)
    library.add_book("To Kill a Mockingbird", "Harper Lee", 2)
    library.add_book("1984", "George Orwell", 4)
    
    app.run(debug=True, port=8000)
