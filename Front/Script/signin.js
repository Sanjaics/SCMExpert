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
                console.log(signin);

                // Store in local storage
                localStorage.setItem('token', signin.token);
                
                localStorage.setItem('user_email', signInData.email);

                // Redirect to Dashboard 
                window.location.href = 'Dashboard.html';
            } else {
                document.getElementById('userpassword').textContent = 'Password or email is invalid';
                return false;
            }
        } catch (error) {
            console.error('Error during sign-in:', error);
        }
    }

    // Event listener for the sign-in form
    const signInForm = document.getElementById('sign_in');
    if (signInForm) {
        signInForm.addEventListener('submit', signIn);
    } else {
        console.error('Sign-in form not found');
    }

    //  myFunction();
    
  
    
});
function myfunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

