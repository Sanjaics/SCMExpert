window.addEventListener('load', (event) => {
    // Function to handle sign-up
    async function signUp() {
        const username = document.getElementById('username').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('upassword').value;
        const confirmPassword = document.getElementById('confirmpassword').value;

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            document.getElementById('mailError').textContent = 'Invalid email address';
            return false;
        } else {
            document.getElementById('mailError').textContent = ''; // Clear error message
        }

        if (password.length < 8) {
            document.getElementById('passwordError').textContent = 'Passwords must contain at least 8 characters';
            return false;
        } else {
            document.getElementById('passwordError').textContent = ''; // Clear error message
        }

        // Password validation
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
            return false;
        } else {
            document.getElementById('confirmPasswordError').textContent = ''; // Clear error message
        }

        const signUpData = {
            username: username,
            email: email,
            password: password,
            confirm_password: confirmPassword
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(signUpData),
            });

            // Check if the response status is OK (status code 2xx)
            if (response.ok) {
                const data = await response.json();
                console.log(data);
                // If sign-up is successful, store user data in local storage
                localStorage.setItem('userData', JSON.stringify({
                    username: username,
                    email: email,
                    status: 'registered'
                }));
                console.log('User data stored in local storage');
                window.location.href = 'index.html'
            } else {
                const errorData = await response.json();
                console.error('Error:', errorData.detail);
            }

        } catch (error) {
            console.error('Error occurred while user sign-up:', error);
        }
    }

    // Event listener for the sign-up form
    const signUpForm = document.getElementById('sign_up');
    if (signUpForm) {
        signUpForm.addEventListener('submit', function (event) {
            event.preventDefault();
            signUp();
        });
    } else {
        console.error('Sign-up form not found');
    }

   
});


function myFunction() {
    var x = document.getElementById("upassword");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

