document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            const bookId = this.getAttribute("data-book-id");
            console.log("Removing book ID:", bookId); // Debugging log

            fetch("/remove_from_cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ book_id: bookId })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server response:", data); // Debugging log

                if (data.success) {
                    this.closest(".card").remove();
                    document.getElementById("grand-total").textContent = data.new_total;
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => console.error("Fetch error:", error));
        });
    });
});
