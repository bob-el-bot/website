const originalTitle = document.title;

const titlesByRoute = {
    "/": ["We hope you're enjoying Bob!", "Come back to the homepage!", "We’re still here!"],
    "/commands": ["Bob's Docs are right here!", "Come read up!", "You really like the Docs, huh?"],
    "/premium": ["Enjoy premium!", "You won't regret upgrading!", "It's worth it!"],
    "/blog": ["Pick an article!", "Missing out on these blogs!"],
    "/community": ["Thanks for taking the time!", "Thanks for reading this!"],
    "/blogs": ["Read more!", "You should share this!", "Blog is ready when you are!"],
    "/colors": ["Discord colors right here!", "Rainbows!", "Bob's favorite color is purple!"],
    "/timestamps": ["Timestamps right here!", "Time is relative...", "What time is it?"],
};

let currentRoute = window.location.pathname;
currentRoute = currentRoute.replace(/\.html$/, ''); // Remove .html if it's present

// If the path starts with '/blogs', use the /blogs messages
const isBlogPage = currentRoute.startsWith("/blogs");

const awayTitles = isBlogPage ? titlesByRoute["/blogs"] : titlesByRoute[currentRoute] || ["Come back soon!"];

function getRandomTitle() {
    const randomIndex = Math.floor(Math.random() * awayTitles.length);
    return awayTitles[randomIndex];
}

// Detect when visibility changes
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        // Set a random title if the page is hidden
        document.title = getRandomTitle();
    } else {
        // Restore the original title when the page is visible again
        document.title = originalTitle;
    }
});