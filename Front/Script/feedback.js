let selectedRating = 0;

function setRating(rating) {
    selectedRating = rating;

    // display the selected rating 
    for (let i = 1; i <= 5; i++) {
        const element = document.getElementById('rate' + i);
        if (i <= rating) {
            element.classList.add('selected');
        } else {
            element.classList.remove('selected');
        }
    }
}

async function submitFeedback() {
    try {
        const feedbackText = document.getElementById('feedbackText').value;

        if (selectedRating === 0) {
            alert('Please provide a rating before submitting.');
            return;
        }
        const feedbackData = {
            feedback_text: feedbackText,
            rating: selectedRating,
        };

        const accessToken = localStorage.getItem('token');

        const response = await fetch('http://127.0.0.1:8000/feedback', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(feedbackData),
        });

        if (response.status === 401) {
            console.error('User not authenticated. Redirecting to the login page.');
            // window.location.href = 'index.html';
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        alert(result.message);  // Display  message
        clearForm();

    } catch (error) {
        console.error('Error submitting feedback:', error.message);
        // Handle error as needed
    }
}

function clearForm() {
    // Clear values
    document.getElementById('feedbackText').value = '';

    // Reset ratings visually
    for (let i = 1; i <= 5; i++) {
        const element = document.getElementById('rate' + i);
        element.classList.remove('selected');
    }

    // Reset the selectedRating variable
    selectedRating = 0;
}



// Getting feedback element with the id "feedbackContainer"
const feedbackContainer = document.getElementById('ratingContainer');

async function fetchFeedback() {
    try {
        const accessToken = localStorage.getItem('token');

        const response = await fetch('http://127.0.0.1:8000/feedback', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.status === 401) {
            document.getElementById('error-message').innerText = "unauthorized admin can only access";
            return;
        }

        if (!response.ok) {
            // document.getElementById('success-message').innerText = `Success: ${signin.message}`;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const feedbackList = await response.json();

        // Update the DOM with the feedbackList, creating a card for each feedback
        feedbackContainer.innerHTML = ''; // Clear existing content

        feedbackList.forEach((feedback) => {
            const card = document.createElement('div');
            card.classList.add('card');

            // Add the user, rating, and comment information to the card
            card.innerHTML = `
                <div class="card-header">Feedback</div>
                <div class="card-body">
                    <div class="inner">
                        <div style="font-size: 18px;">
                            <h4>User: ${feedback.user_email}</h4>
                            <h4>Rating: ${feedback.rating}</h4>
                            <h4>Comment: ${feedback.feedback_text}</h4>
                        </div>
                    </div>
                </div>
            `;

            feedbackContainer.appendChild(card);
        });

    } catch (error) {
        console.error('Error fetching feedback:', error.message);
        // Handle error as needed
    }
}

// Call fetchFeedback when the page loads,refresh the feedback list
fetchFeedback();

