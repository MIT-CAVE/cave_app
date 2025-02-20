function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        const [key, value] = cookie.split("=");
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

function refreshAfterCookieTimeout(cookieName) {
    cookieValue = getCookie(cookieName);
    // Only refresh if cookie exists and is valid
    if (!cookieValue) return;
    const timeInSeconds = parseInt(cookieValue, 10);
    if (!isNaN(timeInSeconds) && timeInSeconds > 0) {
        // console.log(`Auth will timeout in ${timeInSeconds} seconds.`);
        setTimeout(() => {
            location.reload(); // Refresh page
        }, (timeInSeconds+1) * 1000); // Convert seconds to milliseconds and 
    }
}

// Refresh after "refresh_timer" cookie value (in seconds)
refreshAfterCookieTimeout("session-timeout");