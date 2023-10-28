// Inside your existing script.js

const compositionInput = document.getElementById('composition');
const suggestionsUl = document.getElementById('suggestions');
const searchForm = document.getElementById('searchForm');
const resultContent = document.getElementById('search-results');
const searchcomposition = document.getElementById('search-composition');


compositionInput.addEventListener('input', () => {
    const term = compositionInput.value.trim();
    if (term.length === 0) {
        suggestionsUl.innerHTML = '';
        suggestionsUl.style.display = 'none';
        return;
    }

    // Make an AJAX request to get suggestions
    fetch(`/analysis-suggest?term=${term}`)
        .then(response => response.json())
        .then(data => {
            suggestionsUl.innerHTML = '';
            if (data.length > 0) {
                data.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    li.addEventListener('click', () => {
                        compositionInput.value = suggestion;
                        suggestionsUl.style.display = 'none';
                    });
                    suggestionsUl.appendChild(li);
                });
                suggestionsUl.style.display = 'block';
            } else {
                suggestionsUl.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching suggestions:', error);
        });
});

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const composition = compositionInput.value;
    // Make an AJAX request to get the search result
    fetch('/analysis-search', {
        method: 'POST',
        body: new URLSearchParams({ composition }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(data => {
            searchcomposition.innerHTML="Search Result for Composition "+composition;
            // Update the content of the current page with the search results
            resultContent.innerHTML = ''; // Clear previous content
            if (data.length > 0) {
                // Create a table element
                const table = document.createElement('table');
                table.border = "1"; // Add a border to the table (optional)
            
                // Create a table row for the table header
                const headerRow = table.insertRow();
                const headers = ["Name", "Composition", "Brand", "Type", "Price"];
            
                headers.forEach(headerText => {
                    const headerCell = document.createElement("th");
                    headerCell.textContent = headerText;
                    headerRow.appendChild(headerCell);
                });
            
                // Iterate through the data and create table rows for each item
                data.forEach(item => {
                    const row = table.insertRow();
                    item.forEach(cellData => {
                        const cell = row.insertCell();
                        cell.textContent = cellData;
                    });
                });
            
                // Append the table to the resultContent (assuming resultContent is a div or other container)
                resultContent.appendChild(table);
                
            }
             else {
                // Display a message if no results are found
                resultContent.textContent = 'No results found.';
            }
        })
        .catch(error => {
            console.error('Error fetching search result:', error);
        });
});
