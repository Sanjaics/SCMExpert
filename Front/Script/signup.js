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
            document.getElementById('mailError').textContent = ''; 
        }

        if (password.length < 8) {
            document.getElementById('passwordError').textContent = 'Passwords must contain at least 8 characters';
            return false;
        } else {
            document.getElementById('passwordError').textContent = ''; 
        }

        // Password validation
        if (password !== confirmPassword) {
            document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
            return false;
        } else {
            document.getElementById('confirmPasswordError').textContent = ''; 
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
                document.getElementById('success-message').innerText = ` ${data.message}`;
              

                // If sign-up is successful, store user data in local storage
                localStorage.setItem('userData', JSON.stringify({
                    username: username,
                    email: email,
                    status: 'registered'
                }));
                console.log('User data stored in local storage');
                redirect(3000);
                
            } else {
                const errorData = await response.json();
                document.getElementById('password-message').innerText = ` ${errorData.detail}`;
                redirect(3000);
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

    function redirect(delay) {
        setTimeout(() => {
            document.getElementById('success-message').innerText = '';
            document.getElementById('password-message').innerText = '';
            window.location.href = 'index.html';
        }, delay);

    }

    myFunction();
});

function myFunction() {
    var x = document.getElementById("upassword");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

