
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
