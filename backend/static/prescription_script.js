// prescription_script.js

// Function to set the current date for the prescriptionDate input
function setCurrentDate() {
    var currentDate = new Date();
    var year = currentDate.getFullYear();
    var month = ('0' + (currentDate.getMonth() + 1)).slice(-2); // Adding 1 because months are zero-indexed
    var day = ('0' + currentDate.getDate()).slice(-2);

    var formattedDate = year + '-' + month + '-' + day;

    document.getElementById("prescriptionDate").value = formattedDate;
}

// Set the current date when the page loads
window.onload = function() {
    setCurrentDate();
};

let isMedicineSectionValidated = false;

function validateForm() {
    clearErrorMessages();

    var isValid = true;

    // Patient Information Validation
    isValid = validateField("patientName", "Please enter the patient's name.") && isValid;
    isValid = validateField("patientAge", "Please enter the patient's age.") && isValid;
    // Add similar lines for other fields...

    // Medicine Section Validation (only validate if not already validated)
    if (!isMedicineSectionValidated) {
        isValid = validateField("composition", "Please enter the medicine composition.") && isValid;
        isValid = validateCheckbox("dosage", "Please select at least one dosage option.") && isValid;
        isValid = validateRadio("frequency", "Please select a frequency option.") && isValid;
        isValid = validateField("duration", "Please enter the duration.") && isValid;
        isValid = validateField("instructions", "Please enter the instructions.") && isValid;

        // Set the flag to true after successful validation
        if (isValid) {
            isMedicineSectionValidated = true;
        }
    }

    return isValid;
}

function validateField(fieldName, errorMessage) {
    var field = document.getElementById(fieldName);
    var fieldValue = field.value.trim();

    if (!fieldValue) {
        displayError(field, errorMessage);
        return false;
    }

    return true;
}

function validateCheckbox(checkboxName, errorMessage) {
    var checkboxes = document.getElementsByName(checkboxName);
    var isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

    if (!isChecked) {
        displayError(checkboxes[0], errorMessage);
        return false;
    }

    return true;
}

function validateRadio(radioName, errorMessage) {
    var radios = document.getElementsByName(radioName);
    var isChecked = Array.from(radios).some(radio => radio.checked);

    if (!isChecked) {
        displayError(radios[0], errorMessage);
        return false;
    }

    return true;
}
function displayError(element, errorMessage) {
    var errorSpan = document.createElement("span");
    errorSpan.className = "error-message";
    errorSpan.innerHTML = errorMessage;

    element.parentNode.appendChild(errorSpan);
}

function clearErrorMessages() {
    var errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach(function (errorMessage) {
        errorMessage.parentNode.removeChild(errorMessage);
    });
}

function getPrescriptionData() {
    var prescriptionData = [];
    var tableRows = document.getElementById('prescriptionTableBody').getElementsByTagName('tr');

    for (var i = 0; i < tableRows.length; i++) {
        var cells = tableRows[i].getElementsByTagName('td');

        var medicine = cells[0].innerText;
        var dosage = cells[1].innerText;
        var frequency = cells[2].innerText;
        var duration = cells[3].innerText;
        var instructions = cells[4].innerText;

        prescriptionData.push({
            medicine: medicine,
            dosage: dosage,
            frequency: frequency,
            duration: duration,
            instructions: instructions
        });
    }

    return prescriptionData;
}

function addPrescription() {
    if (!validateForm()) {
        return;
    }

    var composition = document.getElementById("composition").value;
    var dosage = getCheckboxValues("dosage");
    var frequency = getRadioValue("frequency");
    var duration = document.getElementById("duration").value;
    var instructions = document.getElementById("instructions").value;

    var table = document.getElementById("prescriptionTableBody");
    var row = table.insertRow(-1);

    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);
    var cell6 = row.insertCell(5);

    cell1.innerHTML = composition;
    cell2.innerHTML = dosage.join(', ');
    cell3.innerHTML = frequency;
    cell4.innerHTML = duration;
    cell5.innerHTML = instructions;
    cell6.innerHTML = '<button onclick="deleteRow(this)">Delete</button>';

    clearPrescriptionForm();
}

function getCheckboxValues(checkboxName) {
    var checkboxes = document.getElementsByName(checkboxName);
    var values = [];

    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            values.push(checkbox.value);
        }
    });

    return values;
}

function getRadioValue(radioName) {
    var radios = document.getElementsByName(radioName);

    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i].value;
        }
    }

    return null;
}

function deleteRow(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function clearPrescriptionForm() {
    document.getElementById("composition").value = "";
    document.getElementsByName("dosage").forEach(function (checkbox) {
        checkbox.checked = false;
    });
    document.getElementsByName("frequency").forEach(function (radio) {
        radio.checked = false;
    });
    document.getElementById("duration").value = "";
    document.getElementById("instructions").value = "";
}

function generatePrescription() {
    // Clear existing error messages
    clearErrorMessages();

    // Validate the form before generating the prescription
    if (!validateForm()) {
        return;
    }

    // Hospital Information (you can customize this)
    var hospital_name = document.getElementById('hospitalName').value;
    var hospital_address =document.getElementById('hospitalAddress').value;
    var hospital_phone = document.getElementById('hospitalPhone').value;

    console.log("Hospital Name:", hospital_name);
    console.log("Hospital Address:", hospital_address);
    console.log("Hospital Phone:", hospital_phone);


    // Get patient information
    var date = document.getElementById('prescriptionDate').value;
    var patientName = document.getElementById('patientName').value;
    var patientAge = document.getElementById('patientAge').value;
    var patientGender = document.getElementById('patientGender').value;
    var weight = document.getElementById('weight').value;
    var height = document.getElementById('height').value;
    var bloodPressure = document.getElementById('bloodPressure').value;

    // Get prescription data
    var prescriptionData = getPrescriptionData();

    // Additional Information
    var additionalNotes = document.getElementById('additionalNotes').value;

    // Create HTML content for the prescription
    var content = `
        <div style="font-family: 'Arial', sans-serif; max-width: 800px; margin: 20px auto; font-size: 12px;padding:20px">
         <div style="background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                <div style="color: #4caf50; text-align: center; font-size: 20px; margin-bottom: 15px;">Prescription Date</div>
                <div><strong>Date:</strong> ${date}</div>
            </div>  
            <br>  
        <div style="background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                <div style="color: #4caf50; text-align: center; font-size: 20px; margin-bottom: 15px;">Your Hospital Name</div>
                <div><strong>Hospital Name:</strong> ${hospital_name}</div>
                <div><strong>Hospital Address:</strong> ${hospital_address}</div>
                <div><strong>Hospital Phone:</strong> ${hospital_phone}</div>
            </div>
            <br>
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;margin-bottom: 20px;">
                <div style="flex: 1; background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                    <h2 style="color: #4caf50; margin-bottom: 15px; font-size: 20px;">Patient Information</h2>
                    <div><strong>Name:</strong> ${patientName}</div>
                    <div><strong>Age:</strong> ${patientAge}</div>
                    <div><strong>Gender:</strong> ${patientGender}</div>
                </div>

                <div style="flex: 1; margin-left: 20px; background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                    <h2 style="color: #4caf50; margin-bottom: 15px; font-size: 20px;">Vital Statistics</h2>
                    <div><strong>Weight:</strong> ${weight} Kg</div>
                    <div><strong>Height:</strong> ${height} feet</div>
                    <div><strong>Blood Pressure:</strong> ${bloodPressure}</div>
                </div>
            </div>

            <div style="background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); margin-bottom: 20px; padding: 20px;">
                <h2 style="color: #4caf50; margin-bottom: 15px; font-size: 20px;">Medicine Information</h2>
                <table style="width: 100%; border-collapse: collapse; text-align:left">
                    <thead style="margin-bottom:20px">
                        <tr>
                            <th>Medicine</th>
                            <th>Dosage</th>
                            <th>Frequency</th>
                            <th>Duration</th>
                            <th>Instructions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${prescriptionData.map(prescription => `
                            <tr>
                                <td>${prescription.medicine}</td>
                                <td>${prescription.dosage}</td>
                                <td>${prescription.frequency}</td>
                                <td>${prescription.duration}</td>
                                <td>${prescription.instructions}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>

            <div style="background-color: #f4f4f4; min-height:400px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                <h2 style="color: #4caf50; margin-bottom: 15px; font-size: 20px;">Additional Details</h2>
                <div>${additionalNotes}</div>
            </div>
        </div>
    `;

    // Convert HTML to PDF using html2pdf library
    html2pdf().from(content).save('prescription.pdf');
}
