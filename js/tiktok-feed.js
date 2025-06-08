// TikTok Feed Configuration
const TIKTOK_USERNAME = 'treasurelandschoolijebuode'; // Your TikTok username
const TIKTOK_FEED_CONTAINER = document.getElementById('tiktok-feed');
const TIKTOK_VIDEO_IDS = [
    '7510968199823887621', // Replace with your TikTok video IDs
    '7510096997324475704',
    '7509737324020845830'
];

// Function to create TikTok embed using iframe
function createTikTokEmbed(videoId) {
    const col = document.createElement('div');
    col.className = 'col-md-4 ftco-animate mb-4';

    // Create iframe for the TikTok embed
    const iframe = document.createElement('iframe');
    iframe.setAttribute('src', `https://www.tiktok.com/embed/v2/${videoId}?lang=en-US`);
    iframe.setAttribute('allowfullscreen', 'true');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('height', '600');
    iframe.setAttribute('width', '325');
    iframe.style.maxWidth = '100%';
    iframe.style.borderRadius = '8px';

    // Create a wrapper div for better styling
    const wrapper = document.createElement('div');
    wrapper.style.position = 'relative';
    wrapper.style.paddingBottom = '175%';
    wrapper.style.overflow = 'hidden';
    wrapper.style.borderRadius = '8px';
    wrapper.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';

    // Style the iframe to be responsive
    iframe.style.position = 'absolute';
    iframe.style.top = '0';
    iframe.style.left = '0';
    iframe.style.width = '100%';
    iframe.style.height = '100%';

    wrapper.appendChild(iframe);
    col.appendChild(wrapper);

    return col;
}

// Function to load TikTok script
function loadTikTokScript() {
    return new Promise((resolve) => {
        console.log('Loading TikTok script...');
        if (window.tiktokEmbedLoaded) {
            console.log('TikTok script already loaded');
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://www.tiktok.com/embed.js';
        script.async = true;
        script.onload = () => {
            window.tiktokEmbedLoaded = true;
            resolve();
        };
        document.body.appendChild(script);
    });
}

// Main function to load and display TikTok embeds
async function loadTikTokEmbeds() {
    console.log('loadTikTokEmbeds called');
    const container = document.getElementById('tiktok-feed');
    if (!container) {
        console.error('TikTok feed container not found');
        return;
    }

    try {
        // Show loading state
        container.innerHTML = `
            <div class="col-12 text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
                <p class="mt-2">Loading TikTok posts...</p>
            </div>`;

        // Wait a moment for the TikTok script to load
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Clear loading state
        container.innerHTML = '';

        // Create embeds for each video
        console.log('Creating embeds for videos:', TIKTOK_VIDEO_IDS);
        TIKTOK_VIDEO_IDS.forEach((videoId, index) => {
            console.log(`Creating embed ${index + 1} for video ID:`, videoId);
            try {
                const embed = createTikTokEmbed(videoId);
                container.appendChild(embed);
                console.log(`Embed ${index + 1} created and appended`);

                // Add a fallback link for mobile devices
                const fallbackLink = document.createElement('a');
                fallbackLink.href = `https://www.tiktok.com/@${TIKTOK_USERNAME}/video/${videoId}`;
                fallbackLink.target = '_blank';
                fallbackLink.rel = 'noopener';
                fallbackLink.className = 'btn btn-sm btn-outline-primary mt-2';
                fallbackLink.textContent = 'Watch on TikTok';
                fallbackLink.style.display = 'block';
                fallbackLink.style.margin = '10px auto';
                fallbackLink.style.maxWidth = '200px';

                container.appendChild(fallbackLink);
            } catch (error) {
                console.error(`Error creating embed ${index + 1}:`, error);
            }
        });

        // Add a small delay before checking for TikTok script
        setTimeout(() => {
            if (window.tiktok && window.tiktok.parser) {
                console.log('Calling TikTok parser');
                window.tiktok.parser();
            } else {
                console.warn('TikTok parser not available, embeds may not load correctly');
            }
        }, 1000);

    } catch (error) {
        console.error('Error loading TikTok embeds:', error);
        container.innerHTML = `
            <div class="col-12 text-center">
                <p>Unable to load TikTok posts. Please try again later.</p>
                <p><a href="https://www.tiktok.com/@${TIKTOK_USERNAME}" target="_blank" class="btn btn-primary">View on TikTok</a></p>
            </div>`;
    }
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTikTokEmbeds);
} else {
    loadTikTokEmbeds();
}