document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".addToCart").forEach((button) => {
    button.addEventListener("click", function () {
      let bookData = JSON.parse(this.dataset.book);
      let quantity = this.parentElement.querySelector(".book-quantity").value;

      fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: bookData.id, quantity: parseInt(quantity) }), // Sending quantity
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message); // Show success or error message
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
