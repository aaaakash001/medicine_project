const generateBillPdfButton = document.getElementById('generateBillPdfButton');

// Add an event listener to the button
generateBillPdfButton.addEventListener('click', function () {
    // Check if the cart has at least one item
    if (myCart.hasItems()) {
        // Generate the PDF
        myCart.updateTable();
        myCart.generatePDF();
    } else {
        // Handle the case where the cart is empty
        alert('Cart is empty. Add at least one item before generating PDF.');
    }
});

class Cart {
    constructor() {
        this.medicines = {}; // Use an object to store medicines
        this.table = document.getElementById('medicineTable');
        this.rowIndex = 1;
    }

    hasItems() {
        return Object.keys(this.medicines).length > 0;
    }

    addMedicineToCart(selectedMedicine, quantity) {
        if (quantity > 0) {
            const medArray = selectedMedicine.split(':');
            const medName = medArray[1].split('|')[0];
            const basePrice = parseFloat(medArray[2]).toFixed(2);

            if (this.medicines[medName]) {
                // Medicine already in the cart, update quantity
                this.medicines[medName].quantity += quantity;
            } else {
                // Add a new medicine to the cart
                this.medicines[medName] = { name: medName, price: parseFloat(basePrice), quantity: quantity };
            }

            this.updateTable();
        }
    }

    updateQuantity(medName, change) {
        let currentQuantity = this.medicines[medName].quantity + change;

        if (currentQuantity > 0) {
            this.medicines[medName].quantity = currentQuantity;
            this.updateTable();
        } else {
            // If quantity becomes 0, remove the medicine from the cart
            delete this.medicines[medName];
            this.updateTable();
        }
    }

    removeMedicine(medName) {
        delete this.medicines[medName];
        this.updateTable();
    }
    updateTable() {
        // Clear existing rows
        while (this.table.rows.length > 1) {
            this.table.deleteRow(1);
        }
    
        // Reset the index for each update
        this.rowIndex = 1;
    
        // Add new rows based on cart data
        for (const medName in this.medicines) {
            const medicine = this.medicines[medName];
            const quantity = medicine.quantity;
    
            // Create a new row
            const newRow = this.table.insertRow();
    
            // Insert cells into the row
            const indexCell = newRow.insertCell(0);
            const medicineCell = newRow.insertCell(1);
            const priceCell = newRow.insertCell(2);
            const quantityCell = newRow.insertCell(3);
            const totalPriceCell = newRow.insertCell(4);
            const actionCell = newRow.insertCell(5);
    
            // Populate cells with data
            indexCell.innerHTML = this.rowIndex++;
            medicineCell.innerHTML = medicine.name;
            priceCell.innerHTML = medicine.price.toFixed(2);
    
            // Update the quantity cell with the current quantity
            const spanQuantity = document.createElement('span');
            spanQuantity.className = 'quantity-text';
            spanQuantity.innerHTML = quantity.toString();
    
            // Add buttons
            const addButton = document.createElement('button');
            addButton.className = 'quantity-button add';
            addButton.innerHTML = '+';
            addButton.onclick = () => this.updateQuantity(medName, 1);
    
            const subtractButton = document.createElement('button');
            subtractButton.className = 'quantity-button subtract';
            subtractButton.innerHTML = '-';
            subtractButton.onclick = () => this.updateQuantity(medName, -1);
    
            const deleteButton = document.createElement('button');
            deleteButton.innerHTML = 'Delete';
            deleteButton.onclick = () => this.removeMedicine(medName);
    
            quantityCell.className = 'quantity-container';
            quantityCell.appendChild(subtractButton);
            quantityCell.appendChild(spanQuantity);
            quantityCell.appendChild(addButton);
    
            // Calculate total price
            const totalPrice = quantity * medicine.price;
            totalPriceCell.innerHTML = totalPrice.toFixed(2);
    
            actionCell.appendChild(deleteButton);
        }
    
        // Update the total price
        this.updateTotalPrice();
    }
    
    updateTotalPrice() {
        let total = 0;

        for (const medName in this.medicines) {
            const medicine = this.medicines[medName];
            total += medicine.price * medicine.quantity;
        }

        const totalPriceElement = document.getElementById('totalPrice');
        totalPriceElement.innerHTML = 'Total Price: ' + total.toFixed(2);
    }

    generatePDF() {
        if (this.hasItems()) {
            // Format the date for the filename and header
            const date = new Date();
            let dateTimeString = date.toLocaleDateString().replace(/[TZ/]/g, '-');
            dateTimeString += '-' + date.toLocaleTimeString().replace(/[TZ:]/g, '-');

            // HTML content for the header
            const headerHtml = `<header><p style="text-align: right;">Generated on: ${date.toISOString().replace(/[TZ]/g, ' ')}</p></header>`;

            // HTML content for the table (body)
            const tableHtml = this.generateTableHtml();

            // HTML content for the footer
            const footerHtml = '<footer style="position: fixed; bottom: 10px; width: 100%; "><p style="text-align: right;">Generated from DocAssist Portal</p></footer>';

            // Combine HTML content
            const combinedHtml = `${headerHtml}${tableHtml}${footerHtml}`;

            // Convert HTML content to PDF
            html2pdf(combinedHtml, {
                margin: 10,
                filename: `bill_${dateTimeString}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
                pagebreak: { before: '.page-break' },
            });
        } else {
            alert('Cart is empty. Cannot generate PDF.');
        }
    }

    generateTableHtml() {
        // Generate HTML content for the table based on the medicines in the cart
        let tableHtml = '<table style="width:100%;"><thead><tr><th>Index</th><th>Medicine Name</th><th>Price</th><th>Quantity</th><th>Total Price</th></tr></thead><tbody>';
        let index = 1;
        for (const medName in this.medicines) {
            const medicine = this.medicines[medName];
            tableHtml += `<tr><td>${index++}</td><td>${medicine.name}</td><td>${medicine.price.toFixed(2)}</td><td>${medicine.quantity}</td><td>${(medicine.price * medicine.quantity).toFixed(2)}</td></tr>`;
        }

        tableHtml += `<tr><td></td><td></td><td></td><td>Total:</td><td>${this.calculateTotalPrice().toFixed(2)}</td></tr>`;
        tableHtml += '</tbody></table>';

        return tableHtml;
    }

    calculateTotalPrice() {
        let total = 0;

        for (const medName in this.medicines) {
            const medicine = this.medicines[medName];
            total += medicine.price * medicine.quantity;
        }

        return total;
    }

    // Convert medicines object to an array for jsPDF
    medicinesArray() {
        const result = [];

        for (const medName in this.medicines) {
            const medicine = this.medicines[medName];
            result.push([
                this.rowIndex++,
                medicine.name,
                medicine.price.toFixed(2),
                medicine.quantity,
                (medicine.price * medicine.quantity).toFixed(2),
            ]);
        }

        return result;
    }
}

// Usage example:

const myCart = new Cart();

function addMedicineToTable() {
    const selectedMedicine = document.getElementById('medicineDropdown').value;
    const quantity = document.getElementById('quantityInput').value;

    myCart.addMedicineToCart(selectedMedicine, parseInt(quantity));

    // Clear the input fields
    document.getElementById('medicineSearch').value = '';
    document.getElementById('medicineDropdown').value = '';
    document.getElementById('quantityInput').value = '';
}
