/**
 * Read More Functionality
 * Automatically adds "Read more" to text blocks that exceed 3 lines
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize read more functionality for all elements with the class 'readmore-container'
    function initReadMore() {
        // Select all elements that should have read more functionality
        const containers = document.querySelectorAll('.media-body p, .text p, .services-2 .text p, .ftco-about .text p');

        containers.forEach(container => {
            // Skip if already initialized or empty
            if (container.classList.contains('readmore-initialized') || !container.textContent.trim()) {
                return;
            }

            // Get the computed line height or use default (1.5em)
            const lineHeight = parseInt(window.getComputedStyle(container).lineHeight) || 24;
            const maxHeight = lineHeight * 3; // 3 lines

            // Check if content exceeds 3 lines
            if (container.scrollHeight > maxHeight) {
                // Add readmore class to the paragraph
                container.classList.add('readmore-text');

                // Create and append the toggle button
                const toggleBtn = document.createElement('span');
                toggleBtn.className = 'readmore-toggle';
                toggleBtn.textContent = 'Read more';
                toggleBtn.setAttribute('aria-expanded', 'false');

                // Insert after the paragraph
                container.parentNode.insertBefore(toggleBtn, container.nextSibling);

                // Add click event
                toggleBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    const isExpanded = container.classList.toggle('expanded');
                    toggleBtn.textContent = isExpanded ? 'Read less' : 'Read more';
                    toggleBtn.setAttribute('aria-expanded', isExpanded);
                });

                // Mark as initialized
                container.classList.add('readmore-initialized');
            }
        });
    }

    // Initialize on load
    initReadMore();

    // Re-initialize when content is loaded dynamically
    const observer = new MutationObserver(function(mutations) {
        initReadMore();
    });

    // Start observing the document with the configured parameters
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Also re-initialize on window resize in case layout changes affect text wrapping
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(initReadMore, 250);
    });
});