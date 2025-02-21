document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".remove-item").addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-item")) {
            let bookId = event.target.getAttribute("data-book-id");

            if (!bookId) {
                console.error("Book ID not found!");
                return;
            }

            console.log("Extracted Book ID:", bookId);

            let payload = JSON.stringify({ book_id: Number(bookId) });
            console.log("Sending payload:", payload);

            fetch("/remove_fr", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: payload
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
                    event.target.closest(".card").remove();

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
        }
    });
});
