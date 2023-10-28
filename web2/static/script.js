const compositionInput = document.getElementById('composition');
const suggestionsUl = document.getElementById('suggestions');

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

// Close the suggestions dropdown when clicking outside of it
document.addEventListener('click', (event) => {
    if (event.target !== compositionInput) {
        suggestionsUl.style.display = 'none';
    }
});
