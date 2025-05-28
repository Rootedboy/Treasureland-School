// Teacher profiles data
export const teachers = [{
        id: 1,
        name: "Kowe Bose",
        position: "Class Teacher",
        class: "Primary 1",
        about: "I am a creative and spontaneous educator with high sense of awareness.",
        image: "images/teacher-1.jpg",
        favouriteQuote: "Life is good.",
    },
    {
        id: 2,
        name: "Mgbeoji Ifeyinwa Martina",
        position: "Class Teacher",
        class: "Primary 1",
        about: "I am a passionate and dedicated teacher with a strong commitment to education. I believe in creating a supportive and engaging learning environment that helps students reach their full potential.",
        image: "images/teacher-2.jpg",
        favouriteQuote: "No success outside can compensate for the the failure for the failure at home .By David O McKay , an American leader in the Church of Jesus Christ of Latter-Day Saints."
    },
    {
        id: 3,
        name: "Mbgolu Mary Isioma",
        position: "Class Teacher",
        class: "Primary 1",
        about: "I’m an easygoing, loving, and kind-hearted person who values fairness and strongly dislikes favoritism.",
        favouriteQuote: "Since we didn’t inherit generational wealth, may we not inherit their generational curses either",
        image: "images/teacher-3.jpg"
    },
    {
        id: 4,
        name: "Oluremi Temitayo Temitope",
        position: "Class Teacher",
        class: "Primary 2",
        about: "I am hard working, am a disciplinary person , truthful and hate cheating and pretence. Fun to be with. I am ME.",
        image: "images/teacher-4.jpg",
        favouriteQuote: "The Lord replied, “My Presence will go with you, and I will give you rest.” Exodus 33: 14.",
    },
    {
        id: 5,
        name: "Bello Motunrayo Oluwadamilare",
        position: "ICT",
        class: "Primary 1-5",
        about: "My name is Bello Motunrayo Oluwadamilare. I'm a graduate of Olabisi Onabanjo University. I enjoy dancing, singing and teaching children. I'm passionate about children, I love working with children and helping them to grow.",
        image: "images/teacher-4.jpg",
        favouriteQuote: "Make hay while the sun shines.",
    },
    {
        id: 6,
        name: "Folasade Adegoke",
        position: "HOD",
        class: "Primary 4",
        about: "My name is Folashade Grace Adegoke, currently serving as the Head of Primary Four. I am a graduate of Tai Solarin University of Education with a decade of professional teaching experience. I have a deep interest in baking, singing, and nurturing young minds. My passion lies in supporting children from divorced homes as they navigate challenging seasons.",
        image: "images/teacher-4.jpg",
        favouriteQuote: "Don’t wait for the perfect moment. Take the moment and make it perfect.",
    },
    {
        id: 7,
        name: "Victoria Enos Francis",
        position: "Class Teacher",
        class: "Primary 5",
        about: "I'm Eno Francis, a native of Delta state. I am hard-working and driven individual who isn't afraid to face challenges. I am passionate about my job and knows how to get the job done.",
        image: "images/teacher-4.jpg",
        favouriteQuote: "Do onto others what you want them to do to you.",
    },
    {
        id: 8,
        name: "Bello Motunrayo Oluwadamilare",
        position: "ICT",
        class: "Primary 1-5",
        about: "My name is Bello Motunrayo Oluwadamilare. I'm a graduate of Olabisi Onabanjo University. I enjoy dancing, singing and teaching children. I'm passionate about children, I love working with children and helping them to grow.",
        image: "images/teacher-4.jpg",
        favouriteQuote: "Make hay while the sun shines.",
    },
];

// Function to get teacher by ID
export function getTeacherById(id) {
    return teachers.find(teacher => teacher.id === id);
}

// Function to render all teachers
export function renderTeachers(containerId = 'teachers-container') {
    const container = document.getElementById(containerId);
    if (!container) return;

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
}

// Initialize teachers when DOM is loaded
if (document.readyState !== 'loading') {
    renderTeachers();
} else {
    document.addEventListener('DOMContentLoaded', renderTeachers);
}