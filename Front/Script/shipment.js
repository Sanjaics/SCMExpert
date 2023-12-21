document.addEventListener('DOMContentLoaded', (event) => {
    // Function to handle shipment creation
    async function createShipment() {
        // Collect form data
        const shipmentNumber = document.getElementById('shipmentnum').value;
        const routeDetails = document.getElementById('routeDetails').value;
        const device = document.getElementById('devicedata').value;
        const phNumber = document.getElementById('PhNumber').value;
        const ndcNumber = document.getElementById('ndcNumber').value;
        const serialNumber = document.getElementById('serialnumber').value;
        const containerNum = document.getElementById('containerNum').value;
        const goodsType = document.getElementById('goodstype').value;
        const expectedDeliveryDate = document.getElementById('expecteddeliveryDate').value;
        const deliveryNumber = document.getElementById('delivertnumber').value;
        const batchId = document.getElementById('batchid').value;
        const shipmentDescription = document.getElementById('shipmentdescription').value;

        // Validate the form data
        if (!shipmentNumber || !routeDetails || !device || !phNumber || !ndcNumber || !serialNumber || !containerNum || !goodsType || !expectedDeliveryDate || !deliveryNumber || !batchId || !shipmentDescription) {
            console.error('All fields are required');
            return;
        }

        // Check if a token is available in the local storage
        const token = localStorage.getItem('token');
        if (!token) {
            console.error('Token not found. User not authenticated.');
            return;
        }

        // AJAX request to create a new shipment
        try {
            const response = await fetch('http://127.0.0.1:8000/Create_shipment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    ShipmentNumber: shipmentNumber,
                    RouteDetails: routeDetails,
                    Device: device,
                    PoNumber: phNumber,
                    NdcNumber: ndcNumber,
                    SerialNumber: serialNumber,
                    ContainerNum: containerNum,
                    GoodsType: goodsType,
                    ExpectedDeliveryDate: expectedDeliveryDate,
                    DeliveryNumber: deliveryNumber,
                    BatchId: batchId,
                    ShipmentDescription: shipmentDescription,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('success-message').innerText = ` ${data.message}`;
                
                // Display a success message on the page
                const successMessageElement = document.getElementById('success-message');
                document.getElementById('success-message').innerText = ` ${data.message}`;
                successMessageElement.classList.remove('hidden'); // Show the success message
                // Clear  after 3000 milliseconds
                setTimeout(() => {
                    successMessageElement.innerText = '';
                    successMessageElement.classList.add('hidden'); // Hide the success message
                    
                }, 3000);
                clear();
            } else {
                const errorData = await response.json();
                // Print the error detail
                console.error('Error:', errorData.detail);
                // Display the error message on the page
                const errorMessageElement = document.getElementById('error-message');
                errorMessageElement.innerText = `Error: ${errorData.detail}`;
                errorMessageElement.classList.remove('hidden'); // Show the error message
            }

        } catch (error) {
            console.error('Error creating shipment:', error);
        }
    }

    // Event listener for the shipment form
    const shipmentForm = document.getElementById('shipment-form');
    if (shipmentForm) {
        shipmentForm.addEventListener('submit', function (event) {
            event.preventDefault();
            createShipment();
           
        });
    } else {
        console.error('Shipment form not found');
    }

    function clear() {
        // clear values
        document.getElementById('shipment-form').reset();
    }
   
    
});
document.addEventListener('DOMContentLoaded', function () {
    // Get the current date in the format "YYYY-MM-DD"
    var currentDate = new Date().toISOString().split('T')[0];
   
    // Set date for the input field
    var dateInput = document.getElementById('expecteddeliveryDate');
    dateInput.value = currentDate;
    dateInput.min = currentDate;
  });
