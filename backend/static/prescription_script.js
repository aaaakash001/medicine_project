// prescription_script.js

// ... (previous code) ...

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

// ... (remaining code) ...
// prescription_script.js
// prescription_script.js

function generatePrescription() {
    // Hospital Information (you can customize this)
    var hospitalInfo = "Your Hospital Name\nAddress: Hospital Address\nPhone: Hospital Phone";

    // Get patient information
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

    // Create HTML content
    var content = `
        <div style="font-family: 'Arial', sans-serif; max-width: 800px; margin: 20px auto; font-size: 12px;">
            <div style="background-color: #f4f4f4; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                <div style="color: #4caf50; text-align: center; font-size: 20px; margin-bottom: 15px;">Your Hospital Name</div>
                <div><strong>Address:</strong> Hospital Address</div>
                <div><strong>Phone:</strong> Hospital Phone</div>
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
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
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

            <div style="background-color: #f4f4f4; min-height:200px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">
                <h2 style="color: #4caf50; margin-bottom: 15px; font-size: 20px;">Additional Details</h2>
                <div>${additionalNotes}</div>
            </div>
        </div>
    `;

    // Convert HTML to PDF
    html2pdf().from(content).save('prescription.pdf');
}




