window.addEventListener('load', async () => {
    try {
        // Retrieve the JWT token from local storage
        const accessToken = localStorage.getItem('token');

        if (!accessToken) {
            console.error('Access token not found. Make sure to set the token after login.');
            return;
        }

        console.log('Access token found:', accessToken);

        // Fetch user information from the /myaccount endpoint
        const response = await fetch('http://127.0.0.1:8000/myaccount', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.status === 401) {
            //Unauthorized, redirect to the login page or handle accordingly
            console.error('User not authenticated. Redirecting to the login page.');
            window.location.href = '/Front/index.html';
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const userData = await response.json();
        console.log(userData);

        // Display user information
        const userEmailElement = document.getElementById('emailDisplay');
        const userUsernameElement = document.getElementById('usernameDisplay');
        const userRoleElement = document.getElementById('roleDisplay');

        if (userEmailElement && userData.email) {
            userEmailElement.textContent = userData.email;
        }

        if (userUsernameElement && userData.username) {
            userUsernameElement.textContent = userData.username;
        }

        if (userRoleElement && userData.role) {
            userRoleElement.textContent = userData.role;
        }

    } catch (error) {
        console.error('Error fetching user account information:', error.message);
        // Handle error as needed, e.g., redirect to the login page
    }
});
