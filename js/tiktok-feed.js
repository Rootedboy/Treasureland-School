// TikTok Feed Configuration
const TIKTOK_USERNAME = 'treasurelandschools'; // Your TikTok username
const TIKTOK_FEED_CONTAINER = document.getElementById('tiktok-feed');
const TIKTOK_POSTS_COUNT = 3;

// Function to create TikTok embed
function createTikTokEmbed(videoId) {
    console.log('Creating embed for video ID:', videoId);
    const col = document.createElement('div');
    col.className = 'col-md-4 ftco-animate mb-4';

    const block = document.createElement('blockquote');
    block.className = 'tiktok-embed';
    block.setAttribute('cite', `https://www.tiktok.com/@${TIKTOK_USERNAME}/video/${videoId}`);
    block.setAttribute('data-video-id', videoId);
    block.setAttribute('style', 'max-width: 605px; min-width: 325px;');

    const section = document.createElement('section');
    block.appendChild(section);

    col.appendChild(block);
    return col;
}

// Function to load TikTok script
function loadTikTokScript() {
    return new Promise((resolve) => {
        console.log('Loading TikTok embed script...');
        const script = document.createElement('script');
        script.src = 'https://www.tiktok.com/embed.js';
        script.async = true;
        script.onload = () => {
            console.log('TikTok script loaded');
            resolve();
        };
        script.onerror = (error) => {
            console.error('Error loading TikTok script:', error);
            resolve(); // Still resolve to continue execution
        };
        document.body.appendChild(script);
    });
}

// TikTok oEmbed API Implementation
async function loadTikTokEmbeds() {
    const container = document.getElementById('tiktok-feed');
    if (!container) return;

    const videoIds = [
        '7509737324020845830',
        '7509175490910129414',
        '7485703302315773192'
    ];

    for (const videoId of videoIds) {
        try {
            const response = await fetch(`https://www.tiktok.com/oembed?url=https://www.tiktok.com/@treasurelandschools/video/${videoId}`);
            const data = await response.json();

            const col = document.createElement('div');
            col.className = 'col-md-4 ftco-animate mb-4';
            col.style.padding = '10px';
            col.innerHTML = data.html;

            container.appendChild(col);
        } catch (error) {
            console.error(`Error loading TikTok ${videoId}:`, error);
        }
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTikTokEmbeds);
} else {
    loadTikTokEmbeds();
}