window.addEventListener('load', () => {
    // Function to handle sign-in
    async function signIn(event) {
        // Prevent default form submission
        event.preventDefault();

        const email = document.getElementById('signEmail').value;
        const password = document.getElementById('password').value;

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('EmailError').textContent = 'Invalid email address';
            return false;
        } else {
            document.getElementById('EmailError').textContent = '';
        }

        if (password.length < 8) {
            document.getElementById('userpassword').textContent = 'Passwords must contain at least 8 characters';
            return false;
        } else {
            document.getElementById('userpassword').textContent = '';
        }

        const signInData = {
            email: email,
            password: password
        };

        const formData = new URLSearchParams()
        formData.append('username', `${email}`);
        formData.append('password', `${password}`);

        try {
            const response = await fetch('http://127.0.0.1:8000/signin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                mode: 'cors',
                body: formData,
            });

            // Check if the sign-in was successful
            if (response.ok) {
                const signin = await response.json();

                // Store in local storage
                localStorage.setItem('token', signin.token);
                sessionStorage.setItem("email", signin.email);
                sessionStorage.setItem("username", signin.username);
                sessionStorage.setItem("role", signin.role);

                document.getElementById('success-message').innerText = `Success: ${signin.message}`;
                clearAfterDelay(3000);
                // Redirect to Dashboard 

            } else {
                document.getElementById('userpassword').innerText = ` ${errorData.detail}`;
                return false;
            }
        } catch (error) {
            console.error('Error during sign-in:', error);
        }

        function clearAfterDelay(delay) {
            setTimeout(() => {
                document.getElementById('success-message').innerText = '';
                window.location.href = 'Dashboard.html';
            }, delay);

        }
    }

    // Event listener for the sign-in form
    const signInForm = document.getElementById('sign_in');
    if (signInForm) {
        signInForm.addEventListener('submit', signIn);
    } else {
        console.error('Sign-in form not found');
    }

    myFunction();
});

//function for showpassword
function myfunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

