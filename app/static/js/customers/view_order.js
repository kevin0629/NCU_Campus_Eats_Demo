document.addEventListener("DOMContentLoaded", () => {
    const flashContainer = document.getElementById("flash-container");
    if (flashContainer) {
        const messages = JSON.parse(flashContainer.dataset.messages);
        displayFlashMessages(messages);
    }
});

// Flash 訊息處理函數
function displayFlashMessages(messages) {
    messages.forEach(([category, message]) => {
        alert(message); // 你可以替換為更好的通知方式
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const orderDataElement = document.getElementById('order-data');
    const orderData = JSON.parse(orderDataElement.dataset.orders);

    function openModal(orderId) {
        const order = orderData[orderId];
        let modalDetails = '';

        for (const [restaurantId, restaurantData] of Object.entries(order.restaurants)) {
            modalDetails += `<p><strong>店家：</strong>${restaurantData.restaurant_name}</p>`;
        }

        modalDetails += `
            <p><strong>下單時間：</strong>${order.order_time}</p>
            <p><strong>訂單狀態：</strong>${
                order.order_status === 1 ? '待處理' :
                order.order_status === 2 ? '店家確認' :
                order.order_status === 3 ? '處理中' : '已完成'
            }</p>
            <p><strong>總金額：</strong>${order.total_amount} 元</p>
            <p><strong>付款方式：</strong>${order.payment_method}</p>
            <p><strong>付款狀態：</strong>${order.payment_status}</p>
            <hr>
        `;

        for (const [restaurantId, restaurantData] of Object.entries(order.restaurants)) {
            modalDetails += `
                <table>
                    <thead>
                        <tr>
                            <th>餐點名稱</th>
                            <th>價格</th>
                            <th>數量</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            restaurantData.items.forEach(item => {
                modalDetails += `
                    <tr>
                        <td>${item.item_name}</td>
                        <td>${item.price} 元</td>
                        <td>${item.quantity}</td>
                    </tr>
                `;
            });
            modalDetails += `</tbody></table>`;
        }

        document.getElementById('modalDetails').innerHTML = modalDetails;
        document.getElementById('orderModal').style.display = "block";
    }

    function closeModal() {
        document.getElementById('orderModal').style.display = "none";
    }

    window.openModal = openModal;
    window.closeModal = closeModal;
});
