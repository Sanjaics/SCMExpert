document.addEventListener('DOMContentLoaded', function () {

    const updateButton = document.getElementById('updateButton');
    updateButton.addEventListener('click', function (event) {
        event.preventDefault();
        document.getElementById('error-message').innerText = '';
        updatePassword();
    });

    async function updatePassword() {
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (!newPassword || !confirmPassword) {
            document.getElementById('err-message').innerText = 'please enter the password';
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/forgotpassword', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    new_password: newPassword,
                    confirm_password: confirmPassword,
                }),
            });

            if (response.ok) {
                const data = await response.json();

                document.getElementById('message').innerText = ` ${data.message}`;
                clearAfterDelay(3000); // 3000 milliseconds (3 seconds)


            } else {
                const errorData = await response.json();
                console.error('Error updating password:', errorData);
                displayError(errorData);
            }
        } catch (error) {
            console.error('Error updating password:', error);
            displayError({ detail: ['An unexpected error occurred.'] });
        }
    }

    function displayError(errorData) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.innerText = `Error: ${errorData.detail.join(', ')}`;
    }

    function clearAfterDelay(delay) {
        setTimeout(() => {
            document.getElementById('message').innerText = '';
            window.location.href = 'index.html';
        }, delay);

    }
});

function myFunction() {
    var x = document.getElementById("new-password");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
