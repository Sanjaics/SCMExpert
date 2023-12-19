// Function to check user authentication
async function checkAuthentication() {
    try {
        const response = await fetch('http://127.0.0.1:8000/check_authentication', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
        });

        if (response.ok) {
            // User is authenticated
            return true;
        } else {
            // User is not authenticated
            return false;
        }
    } catch (error) {
        console.error('Error checking authentication:', error);
        return false;
    }
}

// Function to redirect to the sign-in page if not authenticated
async function redirectToSignIn() {
    let isAuthenticated = await checkAuthentication();

    if (!isAuthenticated) {
        // Redirect to the sign-in page
        window.location.href = 'index.html';
    }
}

// Execute the authentication check on page load
window.addEventListener("load", async () => {
    // Redirect to sign-in page if not authenticated
    await redirectToSignIn();

    // If authenticated, redirect to the dashboard
    
    if (isAuthenticated) {
        window.location.href = 'dashboard.html';
    }
});
