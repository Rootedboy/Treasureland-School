// Navbar scroll effect
window.addEventListener('DOMContentLoaded', function() {
    // Add shadow and background when scrolling
    const navbar = document.getElementById('mainNav');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Close mobile menu when clicking a nav link
    const navLinks = document.querySelectorAll('.nav-link');
    const menuToggle = document.getElementById('ftco-nav');
    const bsCollapse = new bootstrap.Collapse(menuToggle, {toggle: false});
    
    navLinks.forEach(function(l) {
        l.addEventListener('click', function() {
            if (window.innerWidth < 992) { // Only for mobile view
                bsCollapse.hide();
            }
        });
    });
});
