document.addEventListener('DOMContentLoaded', (event) => {
    // Function to handle shipment creation
    async function fetchShipmentData() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error('Token not found. User not authenticated.');
                return;
            }

            const response = await fetch('http://127.0.0.1:8000/myshipment', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }

            const data = await response.json();
            const tableBody = document.querySelector('.table-body');

            // Clear existing rows
            tableBody.innerHTML = '';

            // Check if data is an array before iterating
            if (Array.isArray(data)) {
                // Iterate through the data and append rows to the table
                data.forEach((shipment, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${shipment['ShipmentNumber']}</td>
                        <td>${shipment['RouteDetails']}</td>
                        <td>${shipment['Device']}</td>
                        <td>${shipment['PoNumber']}</td>
                        <td>${shipment['NdcNumber']}</td>
                        <td>${shipment['SerialNumber']}</td>
                        <td>${shipment['ContainerNum']}</td>
                        <td>${shipment['GoodsType']}</td>
                        <td>${shipment['ExpectedDeliveryDate']}</td>
                        <td>${shipment['DeliveryNumber']}</td>
                        <td>${shipment['BatchId']}</td>
                        <td>${shipment['ShipmentDescription']}</td>
                    `;
            
                    tableBody.appendChild(row);
                });

                // Display username and email
                const userInfoContainer = document.querySelector('.user-info-container');
                userInfoContainer.innerHTML = `<p>Username: ${data[0].username}</p><p>Email: ${data[0].email}</p>`;
            } 
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    // functioncall when the page loads
    fetchShipmentData();
    
});


