// Function to update navbar in all HTML files
const fs = require('fs');
const path = require('path');

// Define the new navbar HTML
const newNavbar = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
        <div class="container">
            <a class="navbar-brand" href="index.html">
                <img src="images/TES-Logo512-nobg.png" alt="Logo" style="height: 40px; margin-right: 10px;">
                <span>Treasureland Elementary School</span>
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#ftco-nav" aria-controls="ftco-nav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="oi oi-menu"></span> Menu
            </button>
            <div class="collapse navbar-collapse" id="ftco-nav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item"><a href="index.html" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="about.html" class="nav-link">About</a></li>
                    <li class="nav-item"><a href="teacher.html" class="nav-link">Teacher</a></li>
                    <li class="nav-item"><a href="courses.html" class="nav-link">Courses</a></li>
                    <li class="nav-item"><a href="blog.html" class="nav-link">Blog</a></li>
                    <li class="nav-item"><a href="contact.html" class="nav-link">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>`;

// Files to update
const filesToUpdate = [
    'about.html',
    'teacher.html',
    'courses.html',
    'blog.html',
    'contact.html',
    'pricing.html',
    'blog-single.html'
];

// Function to update a single file
function updateFile(fileName) {
    const filePath = path.join(__dirname, fileName);
    
    if (!fs.existsSync(filePath)) {
        console.log(`Skipping ${fileName} - file not found`);
        return;
    }

    try {
        // Read the file
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Add custom.css if not present
        if (!content.includes('custom.css')) {
            content = content.replace(
                '<link rel="stylesheet" href="css/style.css">',
                '<link rel="stylesheet" href="css/style.css">\n    <link rel="stylesheet" href="css/custom.css">'
            );
        }
        
        // Add custom.js if not present
        if (!content.includes('custom.js') && content.includes('bootstrap.min.js')) {
            content = content.replace(
                '<script src="js/bootstrap.min.js"></script>',
                '<script src="js/bootstrap.min.js"></script>\n    <script src="js/custom.js"></script>'
            );
        }
        
        // Update navbar
        const navbarRegex = /<nav[\s\S]*?<\/nav>/i;
        if (navbarRegex.test(content)) {
            content = content.replace(navbarRegex, newNavbar);
            // Write the updated content back to the file
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`Updated navbar in ${fileName}`);
        } else {
            console.log(`No navbar found in ${fileName}`);
        }
    } catch (error) {
        console.error(`Error updating ${fileName}:`, error.message);
    }
}

// Update all files
filesToUpdate.forEach(updateFile);
console.log('Navbar update process completed!');
