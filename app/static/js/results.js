// Results display functionality

function displayResults(data) {
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const resultsCount = document.getElementById('results-count');
    const uploadedImage = document.getElementById('uploaded-image');
    
    // Clear previous results
    resultsGrid.innerHTML = '';
    
    // Display uploaded image
    if (data.uploaded_image) {
        if (data.uploaded_image.startsWith('http')) {
            uploadedImage.src = data.uploaded_image;
        } else {
            uploadedImage.src = `/static/uploads/${data.uploaded_image}`;
        }
    }
    
    // Display result count
    resultsCount.textContent = `(${data.count} products found)`;
    
    // Display results
    if (data.results && data.results.length > 0) {
        data.results.forEach((product, index) => {
            const card = createProductCard(product, index);
            resultsGrid.appendChild(card);
        });
        
        resultsSection.style.display = 'block';
        scrollToResults();
    } else {
        resultsSection.style.display = 'block';
        resultsGrid.innerHTML = '<p class="no-results">No similar products found. Try adjusting the similarity threshold.</p>';
        scrollToResults();
    }
}

function createProductCard(product, index) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Determine image source
    let imageSrc = product.image_path || '/static/images/placeholder.png';
    
    card.innerHTML = `
        <img src="${imageSrc}" alt="${product.name}" 
             onerror="this.src='/static/images/placeholder.png'">
        <div class="product-info">
            <div class="product-name">${product.name}</div>
            <div class="product-category">${product.category || 'General'}</div>
            ${product.price ? `<div class="product-price">$${product.price.toFixed(2)}</div>` : ''}
            <div class="similarity-score">
                ${(product.similarity_score * 100).toFixed(0)}% Match
            </div>
        </div>
    `;
    
    // Add click handler for details
    card.addEventListener('click', () => {
        showProductDetails(product);
    });
    
    return card;
}

function showProductDetails(product) {
    // Create modal or navigate to product page
    alert(`Product: ${product.name}\nCategory: ${product.category}\nSimilarity: ${(product.similarity_score * 100).toFixed(0)}%`);
}

// Add animation CSS
const style = document.createElement('style');
style.textContent = `
    .product-card {
        animation: fadeInUp 0.5s ease forwards;
        opacity: 0;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .no-results {
        text-align: center;
        padding: 3rem;
        color: var(--text-light);
        font-size: 1.2rem;
    }
    
    .product-price {
        font-weight: 700;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
`;
document.head.appendChild(style);