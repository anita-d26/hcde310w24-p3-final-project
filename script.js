document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let searchTerm = document.getElementById('search-input').value.trim();
    if (searchTerm !== '') {
        searchGenius(searchTerm);
    }
});

function searchGenius(searchTerm) {
    let url = `https://api.genius.com/search?q=${encodeURIComponent(searchTerm)}`;
    fetch(url, {
        headers: {
            'Authorization': 'Bearer V4XqGk84jlrCSdAW9VI3iIvEFQ7fDYA6GmnFJ5ruymIFF3Px-p7dLLHemRCwCIdg'
        }
    })
    .then(response => response.json())
    .then(data => displaySearchResults(data.response.hits))
    .catch(error => console.error('Error:', error));
}

function displaySearchResults(results) {
    let searchResultsContainer = document.getElementById('search-results');
    searchResultsContainer.innerHTML = '';

    if (results.length > 0) {
        let resultList = document.createElement('ul');
        results.forEach(result => {
            let listItem = document.createElement('li');
            listItem.textContent = result.result.full_title;
            resultList.appendChild(listItem);
        });
        searchResultsContainer.appendChild(resultList);
    } else {
        searchResultsContainer.textContent = 'No results found.';
    }
}