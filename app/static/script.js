function addProduct() {
    const container = document.getElementById("products");

    const div = document.createElement("div");
    div.classList.add("form-row");

    div.innerHTML = `
        <select name="product_ids">
            ${document.querySelector('select[name="product_ids"]').innerHTML}
        </select>

        <label>Quantity:</label>
        <input type="number" name="quantities" min="1" required>
    `;

    container.appendChild(div);
}