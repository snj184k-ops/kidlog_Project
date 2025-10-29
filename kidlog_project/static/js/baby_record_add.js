document.getElementById("category").addEventListener("change", function() {
    document.querySelectorAll(".category-field").forEach(el => el.style.display = "none");
    const selected = this.value;
    if (selected) {
        document.querySelector(`[data-category="${selected}"]`).style.display = "block";
    }
});