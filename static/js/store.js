document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".addToCart").forEach(button => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            let quantity = card.querySelector(".form-select").value;

            if (quantity === "Quantity") {
                alert("Please select a quantity.");
                return;
            }

            let bookData = JSON.parse(this.getAttribute("data-book"));
            bookData.quantity = parseInt(quantity, 10);  // Convert to integer

            console.log("Adding to cart:", bookData); // Debugging

            fetch("/add_to_cart", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(bookData),
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error("Error:", error));
        });
    });
});
