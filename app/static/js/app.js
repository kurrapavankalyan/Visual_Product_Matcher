// Visual Product Matcher - Main JavaScript

// Tab switching
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            button.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
    
    // Similarity slider updates
    const slider = document.getElementById('similarity-slider');
    const sliderValue = document.getElementById('similarity-value');
    const sliderUrl = document.getElementById('similarity-slider-url');
    const sliderValueUrl = document.getElementById('similarity-value-url');
    
    if (slider && sliderValue) {
        slider.addEventListener('input', () => {
            sliderValue.textContent = slider.value;
        });
    }
    
    if (sliderUrl && sliderValueUrl) {
        sliderUrl.addEventListener('input', () => {
            sliderValueUrl.textContent = sliderUrl.value;
        });
    }
});

// Utility functions
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    alert(message);
}

function scrollToResults() {
    document.getElementById('results-section').scrollIntoView({ 
        behavior: 'smooth' 
    });
}