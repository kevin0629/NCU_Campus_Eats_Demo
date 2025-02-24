document.addEventListener("DOMContentLoaded", function() {
    const orderDataElement = document.getElementById('orderData');
    const historyOrderData = JSON.parse(orderDataElement.getAttribute('data-history'));

    // 將函式掛到 window，使得 HTML onclick 可以存取
    window.openModal = function(orderId) {
        const order = historyOrderData[orderId];
        let modalDetails = '';

        modalDetails += `
            <p><strong>訂單編號：</strong>${orderId}</p>
            <p><strong>顧客ID：</strong>${order.customer_id}</p>
            <p><strong>下單時間：</strong>${order.order_time}</p>
            <p><strong>預定取餐時間：</strong>${order.order_pick_up_time}</p>
            <p><strong>訂單備註：</strong>${order.order_note}</p>
            <p><strong>總金額：</strong>${order.total_amount} 元</p>
            <hr>
            <table>
                <thead>
                    <tr>
                        <th>餐點名稱</th>
                        <th>數量</th>
                        <th>單價</th>
                        <th>小計</th>
                        <th>備註</th>
                    </tr>
                </thead>
                <tbody>
        `;

        Object.values(order.order_details).forEach(item => {
            modalDetails += `
                <tr>
                    <td>${item.item_name}</td>
                    <td>${item.quantity}</td>
                    <td>${item.price} 元</td>
                    <td>${item.price * item.quantity} 元</td>
                    <td>${item.item_note}</td>
                </tr>
            `;
        });

        modalDetails += `
                </tbody>
            </table>
        `;

        document.getElementById('modalDetails').innerHTML = modalDetails;
        document.getElementById('orderModal').style.display = "block";
    };

    window.closeModal = function() {
        document.getElementById('orderModal').style.display = "none";
    };

    window.onclick = function(event) {
        const modal = document.getElementById('orderModal');
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
