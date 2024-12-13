document.addEventListener("DOMContentLoaded", function() {
    // 從 HTML 中的 data-attribute 取得訂單資料
    const orderDataElement = document.getElementById('orderData');
    const orderData = JSON.parse(orderDataElement.getAttribute('data-order'));

    // 定義函式並掛載到 window，供 HTML onclick 使用
    window.openModal = function(orderId) {
        const order = orderData[orderId];
        let modalDetails = `
            <p><strong>訂單編號：</strong>${orderId}</p>
            <p><strong>顧客ID：</strong>${order.customer_id}</p>
            <p><strong>下單時間：</strong>${order.order_time}</p>
            <p><strong>預定取餐時間：</strong>${order.order_pick_up_time}</p>
            <p><strong>訂單備註：</strong>${order.order_note}</p>
            <p><strong>總金額：</strong>${order.total_amount} 元</p>
            <p><strong>付款狀態：</strong>${order.payment_status}</p>
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
        document.getElementById('orderModal').style.display = 'block';
    };

    window.closeModal = function() {
        document.getElementById('orderModal').style.display = 'none';
    };

    window.openStatusModal = function(orderId, orderStatus) {
        document.getElementById('order_id').value = orderId;
        document.getElementById('statusModal').style.display = 'block';

        // 設定目前訂單狀態為選取狀態
        const orderStatusSelect = document.getElementById('order_status');
        orderStatusSelect.value = orderStatus;
    };

    window.closeStatusModal = function() {
        document.getElementById('statusModal').style.display = 'none';
    };

    window.submitStatus = function() {
        const form = document.getElementById('statusForm');
        form.submit();
    };

    window.openPaymentModal = function(orderId, paymentStatus) {
        document.getElementById('payment_order_id').value = orderId;
        document.getElementById('paymentModal').style.display = 'block';

        // 設定目前支付狀態為選取狀態
        const payStatusSelect = document.getElementById('payment_status');
        payStatusSelect.value = paymentStatus;
    };

    window.closePaymentModal = function() {
        document.getElementById('paymentModal').style.display = 'none';
    };

    window.submitPaymentStatus = function() {
        const form = document.getElementById('paymentForm');
        form.submit();
    };

    window.onclick = function(event) {
        const orderModal = document.getElementById('orderModal');
        if (event.target === orderModal) {
            orderModal.style.display = 'none';
        }

        const statusModal = document.getElementById('statusModal');
        if (event.target === statusModal) {
            statusModal.style.display = 'none';
        }

        const paymentModal = document.getElementById('paymentModal');
        if (event.target === paymentModal) {
            paymentModal.style.display = 'none';
        }
    };

    window.manageOrders = function() {
        // 若有需要再此定義您的 manageOrders 邏輯
        // 目前僅作為範例保留
    };
});
