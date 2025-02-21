document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            const bookId = this.getAttribute("data-book-id");

            if (!bookId) {
                console.error("Error: Invalid book ID."); // Use console.error for debugging
                alert("Error: Invalid book ID.");
                return;
            }

            fetch("/remove_from_cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ book_id: bookId })
            })
            .then(response => {
                if (!response.ok) { // Check for HTTP errors
                    return response.json().then(err => {throw new Error(err.error || response.statusText)}); //improved error handling
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const card = this.closest(".card");
                    if (card) {
                        card.remove();
                    }

                    const grandTotalElement = document.getElementById("grand-total");
                    if (grandTotalElement) {
                        grandTotalElement.textContent = data.new_total.toFixed(2);
                    }

                    // Check if cart is empty and show a message
                    if (data.new_total === 0) {
                        const cartContainer = document.getElementById("cart-container");
                        if (cartContainer) { //check if element exist
                            cartContainer.innerHTML = "<p>Your cart is empty.</p>";
                        }
                    }
                } else {
                    console.error("Server error:", data.error); // Log the server error for debugging
                    alert("Error: " + data.error);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error); // Log fetch errors
                alert("An error occurred: " + error.message); // Alert a user-friendly message
            });
        });
    });
});