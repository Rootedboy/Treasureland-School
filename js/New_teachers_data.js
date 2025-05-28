// New_teachers_data.js
import config from './config.js';

const SHEETS_API_URL = `https://sheets.googleapis.com/v4/spreadsheets/${config.spreadsheetId}/values/${config.range}?key=${config.apiKey}`;

export const fetchTeachers = async () => {
    try {
        const response = await fetch(SHEETS_API_URL);
        const data = await response.json();

        if (!data.values) {
            console.error('No data received from Google Sheets:', data);
            return [];
        }

        const headers = data.values[0];
        const teachers = data.values.slice(1).map((row, index) => {
            const teacher = {};
            headers.forEach((header, idx) => {
                teacher[header] = row[idx];
            });

            // Add ID based on row number
            teacher.id = index + 1;

            // Ensure all required fields exist
            teacher.position = teacher.position || 'Class Teacher';
            teacher.class = teacher.class || teacher.grade || 'N/A';
            teacher.about = teacher.about || teacher['brief of themselves'] || 'No description provided';
            teacher.favouriteQuote = teacher['favourite quote'] || 'No quote provided';
            teacher.image = `images/teacher-${index + 1}.jpg`;

            return teacher;
        });

        return teachers;
    } catch (error) {
        console.error('Error fetching teachers data:', error);
        return [];
    }
};

export const renderTeachers = async (containerId = 'teachers-container') => {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error('Container not found:', containerId);
        return;
    }

    try {
        const teachers = await fetchTeachers();
        if (!teachers || teachers.length === 0) {
            container.innerHTML = '<p>No teachers data available</p>';
            return;
        }

        const teachersHTML = teachers.map(teacher => `
            <div class="col-md-6 col-lg-3 ftco-animate">
                <div class="staff">
                    <div class="img-wrap d-flex align-items-stretch">
                        <div class="img align-self-stretch" style="background-image: url(${teacher.image});"></div>
                    </div>
                    <div class="text pt-3 text-center">
                        <h3>${teacher.name}</h3>
                        <span class="position mb-2">${teacher.position}</span>
                        <div class="faded">
                            <p>${teacher.about}</p>
                            <p><strong>Class:</strong> ${teacher.class}</p>
                            <p><strong>Favourite Quote:</strong> ${teacher.favouriteQuote}</p>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = teachersHTML;
    } catch (error) {
        console.error('Error rendering teachers:', error);
        container.innerHTML = '<p>Error loading teachers data</p>';
    }
};

// Initialize teachers when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await renderTeachers();
    } catch (error) {
        console.error('Error initializing teachers:', error);
    }
});