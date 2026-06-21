const API = "https://functions-app01-b6gncbafdgfta9cs.italynorth-01.azurewebsites.net";

function showError(message) {
    const el = document.getElementById("error-msg");
    el.textContent = message;
    el.style.display = "block";
    setTimeout(() => { el.style.display = "none"; }, 5000);
}

function showSuccess(message) {
    const el = document.getElementById("success-msg");
    el.textContent = message;
    el.style.display = "block";
    setTimeout(() => { el.style.display = "none"; }, 4000);
}

function setLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (btn) btn.disabled = loading;
}

async function loadProducts() {
    setLoading("btn-load", true);
    try {
        const response = await fetch(`${API}/api/products`);
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();

        const tbody = document.getElementById("products");
        tbody.innerHTML = "";

        data.forEach(p => {
            const row = document.createElement("tr");
            const total = p.price * p.quantity;
            row.innerHTML = `
                <td>${p.name}</td>
                <td>${p.price.toFixed(2)} PLN</td>
                <td>${p.quantity}</td>
                <td>${total.toFixed(2)} PLN</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        showError("Failed to load products: " + err.message);
    } finally {
        setLoading("btn-load", false);
    }
}

async function loadTotal() {
    setLoading("btn-total", true);
    try {
        const response = await fetch(`${API}/api/total`);
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();
        document.getElementById("total").innerText = `Total Value: ${data.total.toFixed(2)} PLN`;
    } catch (err) {
        showError("Failed to load total: " + err.message);
    } finally {
        setLoading("btn-total", false);
    }
}

async function applyDiscount() {
    const input = document.getElementById("discount-input");
    const percent = parseFloat(input.value);

    if (isNaN(percent) || percent <= 0 || percent > 100) {
        showError("Please enter a valid discount between 1 and 100.");
        return;
    }

    setLoading("btn-discount", true);
    try {
        const response = await fetch(`${API}/api/discount`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ percent })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || `Server error: ${response.status}`);
        showSuccess(data.message);
        await loadProducts();
        await loadTotal();
    } catch (err) {
        showError("Failed to apply discount: " + err.message);
    } finally {
        setLoading("btn-discount", false);
    }
}

async function resetInventory() {
    setLoading("btn-reset", true);
    try {
        const response = await fetch(`${API}/api/reset`, { method: "POST" });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || `Server error: ${response.status}`);
        showSuccess(data.message);
        await loadProducts();
        await loadTotal();
    } catch (err) {
        showError("Failed to reset inventory: " + err.message);
    } finally {
        setLoading("btn-reset", false);
    }
}

// Load data on page start
loadProducts();
loadTotal();
