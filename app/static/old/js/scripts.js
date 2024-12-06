document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('role');
    const customerFields = document.getElementById('customerFields');
    const restaurantFields = document.getElementById('restaurantFields');

    // 角色CSS
    if (roleSelect) {
        roleSelect.addEventListener('change', function() {
            if (roleSelect.value == '1') {
                customerFields.style.display = 'block';
                restaurantFields.style.display = 'none';
            } else if (roleSelect.value == '2') {
                customerFields.style.display = 'none';
                restaurantFields.style.display = 'block';
            }
        });
    }

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());
            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.json())
              .then(data => alert(data.message));
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.json())
              .then(data => {
                  if (data.role == 1) {
                      window.location.href = data.redirect_url;
                    //   window.location.href = '/customer_dashboard';
                  } else if (data.role == 2) {
                      window.location.href = '/restaurant_dashboard';
                  }
              });
        });
    }

    const addMenuItemForm = document.getElementById('addMenuItemForm');
    if (addMenuItemForm) {
        addMenuItemForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(addMenuItemForm);
            const data = Object.fromEntries(formData.entries());
            fetch('/menu_item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.json())
              .then(data => alert(data.message));
        });
    }

    const checkoutButton = document.getElementById('checkoutButton');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function() {
            const items = []; // Collect items from the menu
            const total_price = 0; // Calculate total price
            const pickup_time = document.getElementById('pickup_time').value;
            const note = document.getElementById('note').value;
            const data = {
                customer_id: 1, // Replace with actual customer ID
                restaurant_id: 1, // Replace with actual restaurant ID
                items: items,
                total_price: total_price,
                pickup_time: pickup_time,
                note: note
            };
            fetch('/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => response.json())
              .then(data => alert(data.message));
        });
    }

    const submitOrderButton = document.getElementById('submitOrderButton');
    if (submitOrderButton) {
        submitOrderButton.addEventListener('click', function() {
            const order_id = 1; // Replace with actual order ID
            const status = 1; // Pending status
            fetch(`/order/${order_id}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: status })
            }).then(response => response.json())
              .then(data => alert(data.message));
        });
    }
});