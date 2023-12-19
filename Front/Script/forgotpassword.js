function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function sendResetEmail() {
  // Validate email format
  const emailInput = document.getElementById("email");
  const email = emailInput.value;

  if (!validateEmail(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Make an asynchronous request to send reset email
  fetch("http://127.0.0.1:8000/forgotpassword", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
    }),
  })
    .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    // Handle the response from the server
    console.log(data);
    alert(data.message);

    // Assuming the server sends a success message, hide reset form and show OTP form
    document.getElementById("reset-form").style.display = "none";
    document.getElementById("otp-form").style.display = "block";
  })
  .catch(error => {
    console.error("Fetch error:", error);
    alert("Error: " + error.message);
  });
}



function updatePassword() {
  var newPassword = document.getElementById('new-password').value;
  var confirmPassword = document.getElementById('confirm-password').value;

  if (newPassword !== confirmPassword) {
      alert("Passwords do not match. Please try again.");
      return;
  }

  // Call the updatePassword function
  handleUpdatePasswordClick();
}


function handleUpdatePasswordClick() {
  // Store the new password in local storage
  var newPassword = document.getElementById('new-password').value;
  localStorage.setItem('newPassword', newPassword);

  // Get the token from wherever you store it
  var token = "create_access_token";  // Replace with your actual token

  // Make an asynchronous request to reset the password
  fetch("http://127.0.0.1:8000/resetpassword", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token,
    },
    body: JSON.stringify({
      new_password: newPassword,
      confirm_password: confirmPassword,
    }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    // Handle the response from the server
    console.log(data);
    alert(data.message);

    // You can redirect the user or perform other actions based on the response
  })
  .catch(error => {
    console.error("Fetch error:", error);
    alert("Error: " + error.message);
  });
}



function verifyOtp() {
  const otp = document.getElementById("otp").value;
  const apiUrl = "http://127.0.0.1:8000/verifyotp";
  const token = localStorage.getItem("access_token");

  const payload = {
      otp: otp,
  };

  if (!otp || !token) {
      alert("OTP or token is missing.");
      return;
  }

  fetch(apiUrl, {
      method: "POST",
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(payload),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      console.log(data);
      alert(data.message);

      if (data.success) {
          document.getElementById("otp-form").style.display = "none";
          document.getElementById("new-password-form").style.display = "block";
      }
  })
  .catch(error => {
      console.error("Fetch error:", error);
      alert("Error: " + error.message);
  });
}









