const nodemailer = require('nodemailer');
const cron = require('node-cron');
const axios = require('axios');
const cheerio = require('cheerio');
require('dotenv').config();

// Scraper Function for Multiple Sites
async function scrapeInternships(userInterests) {
    const sites = [
        'https://www.intern-list.com', //for us internships
        'https://devpost.com/', //for hackathons
        'https://www.coursera.org/search?query=professional%20certificates&sortBy=NEW', //for courses
        'https://www.linkedin.com/jobs/search/?keywords=internship&f_TPR=r172800',   //for worldwide internships (past 48 hours)
        'https://topmate.io' //for networking profiles
    ];
    let opportunities = [];

    try {
        for (const site of sites) {
            const searchUrl = addSearchParams(site, userInterests);
            const { data } = await axios.get(searchUrl);
            const $ = cheerio.load(data);

            $('.job-listing').each((index, element) => {
                const title = $(element).find('.job-title').text().trim();
                const description = $(element).find('.job-description').text().trim();
                const link = $(element).find('a').attr('href');
                const postedDate = $(element).find('.posted-date').text().trim();
                
                if (isWithinLast48Hours(postedDate) && matchesUserInterests(title + ' ' + description, userInterests)) {
                    opportunities.push({ title, link });
                }
            });
        }
    } catch (error) {
        console.error("Error scraping internships:", error);
    }

    return opportunities;
}

// Helper Functions
function addSearchParams(url, interests) {
    const searchTerms = interests.join(' OR ');
    
    if (url.includes('linkedin.com')) {
        return `${url}&keywords=${encodeURIComponent(searchTerms)}`;
    } else if (url.includes('devpost.com')) {
        return `${url}search?query=${encodeURIComponent(searchTerms)}&sort=recent`;
    } else if (url.includes('coursera.org')) {
        return `${url}&query=${encodeURIComponent(searchTerms)}`;
    }
    return url;
}

function matchesUserInterests(text, interests) {
    text = text.toLowerCase();
    return interests.some(interest => text.includes(interest.toLowerCase()));
}

function isWithinLast48Hours(dateString) {
    if (!dateString) return false;
    const postDate = new Date(dateString);
    const now = new Date();
    const diffHours = (now - postDate) / (1000 * 60 * 60);
    return diffHours <= 48;
}

// Email Configuration
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

// Fetch Users
async function getUsers() {
    try {
        const response = await axios.get('http://localhost:5000/api/users');
        return response.data;
    } catch (error) {
        console.error('Error fetching users:', error);
        return [];
    }
}

// Send Emails
async function sendEmails() {
    try {
        const users = await getUsers();

        for (const user of users) {
            const interests = user.interests ? user.interests.split(',') : [];
            const opportunities = await scrapeInternships(interests);
            
            if (opportunities.length === 0) continue;

            const htmlContent = `
                <h3>Hi ${user.name},</h3>
                <p>Here are some new opportunities matching your interests:</p>
                <ul>${opportunities.map(op => `<li><a href="${op.link}">${op.title}</a></li>`).join('')}</ul>
                <p>Happy hunting!</p>`;

            await transporter.sendMail({
                from: process.env.EMAIL_USER,
                to: user.email,
                subject: 'New Career Opportunities',
                html: htmlContent
            });
            
            console.log(`Email sent to ${user.email}`);
        }
    } catch (error) {
        console.error("Error sending emails:", error);
    }
}

// Schedule Emails
cron.schedule('0 9 * * *', sendEmails);

// Export for testing
module.exports = { sendEmails, scrapeInternships };