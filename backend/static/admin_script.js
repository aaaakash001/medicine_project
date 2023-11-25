// Inside your existing script.js

const compositionInput = document.getElementById('composition');
const suggestionsUl = document.getElementById('suggestions');
const searchForm = document.getElementById('searchForm');
const resultContent = document.getElementById('search-results');

compositionInput.addEventListener('input', () => {
    const term = compositionInput.value.trim();
    if (term.length === 0) {
        suggestionsUl.innerHTML = '';
        suggestionsUl.style.display = 'none';
        return;
    }

    // Make an AJAX request to get suggestions
    fetch(`/suggest?term=${term}`)
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
    fetch('/search', {
        method: 'POST',
        body: new URLSearchParams({ composition }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(data => {
            // Update the content of the current page with the search results
            resultContent.innerHTML = ''; // Clear previous content
            if (data.length > 0) {
                data.forEach(item => {
                    // Create and append elements to display each result
                    const div = document.createElement('div');
                    div.textContent = `Name: ${item[0]}, Composition: ${item[1]}, Brand: ${item[2]}, Type: ${item[3]}, Price: ${item[4]}`;
                    // Add more content as needed
                    resultContent.appendChild(div);
                });
            } else {
                // Display a message if no results are found
                resultContent.textContent = 'No results found.';
            }
        })
        .catch(error => {
            console.error('Error fetching search result:', error);
        });
});
function validateForm() {
    // Get the user input
    const user = document.getElementById("user").value;
    const pass = document.getElementById("pass").value;

    // Replace this with actual authentication logic (e.g., AJAX request to a server)
    fetch('/admin-search', {
        method: 'POST',
        body: JSON.stringify({ username: user, password: pass }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to the dashboard page on successful login
            window.location.href = "admin-dashboard";
        } else {
            // Display an error message
            document.getElementById("error-message").textContent = "Invalid username or password. Please try again.";
        }
    })
    .catch(error => {
        console.error("An error occurred:", error);
    });

    return false; // Prevent form submission
}