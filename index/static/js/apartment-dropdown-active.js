document.querySelectorAll('.search-apartment-dropdown-header').forEach(function(element) {
    element.addEventListener('click', function() {
        this.classList.toggle('active');
    });
});