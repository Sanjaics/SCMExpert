document.addEventListener('DOMContentLoaded', (event) => {
    function displayDeviceData(data) {
        const tableBody = document.querySelector('.table-body');

        // Clear existing rows
        tableBody.innerHTML = '';

        // Check if data is an array before iterating
        if (Array.isArray(data)) {
            // Iterate the data and append rows to the table
            data.forEach(device => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${device['Battery_Level']}</td>
                    <td class="Device_ID">${device['Device_ID']}</td>
                    <td>${device['First_Sensor_temperature']}</td>
                    <td>${device['Route_From']}</td>
                    <td>${device['Route_To']}</td>
                `;

                tableBody.appendChild(row);
            });
        } else {
            console.error('Data is not an array:', data);
        }
    }

    async function fetchAndDisplayData() {
        try {
            const response = await fetch('http://127.0.0.1:8000/devicedata', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!response.ok) {
                document.getElementById('error-message').innerText = `Error: ${data.detail}`;
                clearAfterDelay(3000);
            }
            const data = await response.json();
            displayDeviceData(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }

        function clearAfterDelay(delay) {
            setTimeout(() => {
                document.getElementById('message').innerText = '';
            }, delay);
    
        }

    }

    // Call the fetchAndDisplayData function when the page loads
    fetchAndDisplayData();

    let searchInput = document.getElementById('searchInput');

    searchInput.addEventListener('keyup', function (event) {
        let searchQuery = event.target.value.toLowerCase();

        let allDeviceIdCells = document.querySelectorAll('.Device_ID');
        allDeviceIdCells.forEach(cell => {
            const currentName = cell.textContent.toLowerCase();

            if (currentName.includes(searchQuery)) {
                cell.parentElement.style.display = 'table-row';
            } else {
                cell.parentElement.style.display = 'none';
            }
        });
    });
});

