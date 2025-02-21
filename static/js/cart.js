document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-item").forEach((button) => {
        button.addEventListener("click", function () {
            let bookId = this.getAttribute("data-book-id");

            console.log("Extracted Book ID:", bookId);

            // Ensure bookId is being sent in correct JSON format
            var payload = JSON.stringify({ book_id: parseInt(bookId) ,"hi" :123,});
            console.log("Sending payload:", payload);

            fetch("/remove_from_cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: payload,
            })
            .then(async (response) => {
                console.log("Raw response:", response);
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || response.statusText);
                }
                return response.json();
            })
            .then((data) => {
                console.log("Server Response:", data);
                if (data.success) {
                    this.closest(".card").remove();

                    const grandTotalElement = document.getElementById("grand-total");
                    if (grandTotalElement) {
                        grandTotalElement.textContent = data.new_total.toFixed(2);
                    }

                    if (data.new_total === 0) {
                        const cartContainer = document.getElementById("cart-container");
                        if (cartContainer) {
                            cartContainer.innerHTML = "<p>Your cart is empty.</p>";
                        }
                    }
                } else {
                    console.error("Server error:", data.error);
                    alert("Error: " + data.error);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("An error occurred: " + error.message);
            });
        });
    });
});
