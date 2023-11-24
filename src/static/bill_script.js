// Function to fetch composition suggestions based on user input
function getSuggestions(searchTerm) {
    // Make an AJAX request to the server
    fetch(`/composition-suggest?term=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            // Update the datalist with the received suggestions
            updateDatalist(data);

            // Disable the medicine dropdown until a composition is selected
            const medicineDropdown = document.getElementById('medicineDropdown');
            medicineDropdown.disabled = true;
        })
        .catch(error => {
            console.error('Error fetching composition suggestions:', error);
        });
}

// Function to handle the selection of a composition
function onCompositionSelected() {
    const selectedComposition = document.getElementById('medicineSearch').value;

    // Enable the medicine dropdown and fetch medicines based on the selected composition
    const medicineDropdown = document.getElementById('medicineDropdown');
    medicineDropdown.disabled = false;

    // Enable the quantity input
    const quantityInput = document.getElementById('quantityInput');
    quantityInput.disabled = false;

    // Call getMedicines only if a composition is selected
    if (selectedComposition.trim() !== '') {
        getMedicines(selectedComposition);
    }
}

// Function to update the datalist with new suggestions
function updateDatalist(suggestions) {
    const compositionList = document.getElementById('compositionList');
    
    // Clear existing options
    compositionList.innerHTML = '';

    // Add new options based on suggestions
    suggestions.forEach(suggestion => {
        const option = document.createElement('option');
        option.value = suggestion;
        compositionList.appendChild(option);
    });
}

// Function to fetch medicines based on selected composition
function getMedicines(selectedComposition) {
    console.log('Selected Composition:', selectedComposition);

    // Make an AJAX request to the server
    const encodedComposition = encodeURIComponent(selectedComposition);
    fetch(`/medicines?composition=${encodedComposition}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received Medicines:', data);
            // Update the medicine dropdown with the received medicines
            updateMedicineDropdown(data);
        })
        .catch(error => {
            console.error('Error fetching medicines:', error);
        });
}

// Function to update the medicine dropdown with new medicines
function updateMedicineDropdown(medicines) {
    const medicineDropdown = document.getElementById('medicineDropdown');
    
    // Clear existing options
    medicineDropdown.innerHTML = '';

    // Add a default option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.text = 'Select Medicine';
    medicineDropdown.appendChild(defaultOption);

    // Add new options based on medicines
    medicines.forEach(medicine => {
        const option = document.createElement('option');
        option.value = medicine;
        option.text = medicine;
        medicineDropdown.appendChild(option);
    });

    // Enable the medicine dropdown after updating it
    medicineDropdown.disabled = false;
}

// Function to handle the selection of a medicine
function onMedicineSelected(selectedMedicine) {
    // You can perform actions based on the selected medicine, if needed
    console.log('Selected Medicine:', selectedMedicine);
}

let rowIndex = 1; // Variable to keep track of the index
let basePrice = 1; // Placeholder for the actual price logic

// Function to add medicine to the table
function addMedicineToTable() {
    const selectedMedicine = document.getElementById('medicineDropdown').value;
    const quantity = document.getElementById('quantityInput').value;

    // Check if both medicine and quantity are selected
    if (selectedMedicine.trim() !== '' && quantity.trim() !== '' && parseInt(quantity) > 0) {
        // Create a new row
        const table = document.getElementById('medicineTable');
        const tbody = table.getElementsByTagName('tbody')[0];
        const newRow = tbody.insertRow();

        // Insert cells into the row
        const indexCell = newRow.insertCell(0);
        const medicineCell = newRow.insertCell(1);
        const priceCell = newRow.insertCell(2);
        const quantityCell = newRow.insertCell(3);
        const totalPriceCell = newRow.insertCell(4);
        const actionCell = newRow.insertCell(5);

        let myArray = selectedMedicine.split(':');
        medname = myArray[1];
        basePrice = parseFloat(myArray[2]).toFixed(2); // You can replace this with the actual price logic
        // Populate cells with data
        indexCell.innerHTML = rowIndex++;
        medicineCell.innerHTML = medname.split('|')[0];
        priceCell.innerHTML = basePrice; // You can replace this with the actual price logic
        quantityCell.innerHTML = quantity;

        // Calculate total price
        const totalPrice = parseInt(quantity) * basePrice;
        totalPriceCell.innerHTML = totalPrice;

        // Add delete button to the action cell
        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = 'Delete';
        deleteButton.onclick = function () {
            deleteRow(newRow);
        };
        actionCell.appendChild(deleteButton);

        // Clear the input fields
        document.getElementById('medicineSearch').value = '';
        document.getElementById('medicineDropdown').value = '';
        document.getElementById('quantityInput').value = '';
    }
    updateTotalPrice();

}

// Function to delete a row
function deleteRow(row) {
    const table = document.getElementById('medicineTable');
    const tbody = table.getElementsByTagName('tbody')[0];
    tbody.removeChild(row);
    updateTotalPrice();

}

function updateTotalPrice() {
    const table = document.getElementById('medicineTable');
    const tbody = table.getElementsByTagName('tbody')[0];

    let total = 0;

    // Iterate through each row in the table
    for (let i = 0; i < tbody.rows.length; i++) {
        // Get the price cell value from the row
        const priceCell = tbody.rows[i].cells[2];
        const price = parseFloat(priceCell.innerHTML);
        const quantityCell = tbody.rows[i].cells[3];
        const quantity = parseFloat(quantityCell.innerHTML);
        

        // Add the price to the total
        total += price*quantity;
    }

    // Update the <p> element with the total price
    const totalPriceElement = document.getElementById('totalPrice');
    totalPriceElement.innerHTML = 'Total Price: ' + total.toFixed(2);
}

