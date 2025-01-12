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
            // Modify URL to include search terms from user interests
            const searchUrl = addSearchParams(site, userInterests);
            const { data } = await axios.get(searchUrl);
            const $ = cheerio.load(data);

            $('.job-listing').each((index, element) => {
                const title = $(element).find('.job-title').text().trim();
                const description = $(element).find('.job-description').text().trim();
                const link = $(element).find('a').attr('href');
                const postedDate = $(element).find('.posted-date').text().trim();
                
                // Check if opportunity is from last 48 hours
                const isRecent = isWithinLast48Hours(postedDate);
                
                // Only add if the opportunity matches user interests and is recent
                if (isRecent && matchesUserInterests(title + ' ' + description, userInterests)) {
                    opportunities.push({ title, link });
                }
            });
        }
    } catch (error) {
        console.error("Error scraping internships:", error);
    }

    return opportunities;
}

// Helper function to add search parameters to URLs
function addSearchParams(url, interests) {
    const searchTerms = interests.join(' OR ');
    
    if (url.includes('linkedin.com')) {
        return `${url}&keywords=${encodeURIComponent(searchTerms)}`;
    } else if (url.includes('devpost.com')) {
        return `${url}search?query=${encodeURIComponent(searchTerms)}&sort=recent`;
    } else if (url.includes('coursera.org')) {
        return `${url}&query=${encodeURIComponent(searchTerms)}`;
    }
    // Add more site-specific URL modifications as needed
    return url;
}

// Helper function to check if text matches any user interests
function matchesUserInterests(text, interests) {
    text = text.toLowerCase();
    return interests.some(interest => 
        text.includes(interest.toLowerCase())
    );
}

// Helper function to check if posting is within last 48 hours
function isWithinLast48Hours(dateString) {
    if (!dateString) return false;
    const postDate = new Date(dateString);
    const now = new Date();
    const diffHours = (now - postDate) / (1000 * 60 * 60);
    return diffHours <= 48;
}

//  Email Sender Function
async function sendEmails() {
    try {
        const result = await pool.query('SELECT * FROM users');
        const users = result.rows;

        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });

        // Send personalized emails to each user
        for (const user of users) {
            // Get opportunities specific to this user's interests
            const opportunities = await scrapeInternships(user.interests);
            
            if (opportunities.length === 0) continue;

            const htmlContent = `<h3>Hi ${user.name},</h3>
                <p>Here are some new internship opportunities from the last 48 hours matching your interests (${user.interests.join(', ')}):</p>
                <ul>${opportunities.map(op => `<li><a href="${op.link}">${op.title}</a></li>`).join('')}</ul>
                <p>Happy hunting!</p>`;

            await transporter.sendMail({
                from: process.env.EMAIL_USER,
                to: user.email,
                subject: 'New Internship Opportunities',
                html: htmlContent
            });
        }

        console.log("Emails sent successfully.");
    } catch (error) {
        console.error("Error sending emails:", error);
    }
}

// Schedule Emails Every Other Day
cron.schedule('0 9 * * *', sendEmails); // Runs at 9 AM every day

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));