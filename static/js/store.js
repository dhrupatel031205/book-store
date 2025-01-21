document.querySelectorAll('.addCart').forEach(button => {
    button.addEventListener('click', function () {
        // Parse the book data from the data-book attribute
        const bookData = JSON.parse(this.getAttribute('data-book'));

        // Send the data to the backend
        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});