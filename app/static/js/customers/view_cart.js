function confirmAction(itemName, action) {
    let message = "";
    if (action === "add") {
        message = "你確定要將 " + itemName + " 加入「1」份至購物車嗎？";
    } else if (action === "remove") {
        message = "你確定要將 " + itemName + " 從購物車中移除「1」份嗎？";
    } else if (action === "checkout") {
        message = "你確定要進行結帳嗎？";
    }

    if (confirm(message)) {
        if (action === "add") {
            alert(itemName + " 新增成功！");
        } else if (action === "remove") {
            alert(itemName + " 移除成功！");
        }
        return true; // 允許表單提交
    } else {
        return false; // 阻止表單提交
    }
}

// 開啟備註模態框
function openNoteModal(orderId, orderDetailId = null) {
    document.getElementById('noteOrderId').value = orderId;
    document.getElementById('noteDetailId').value = orderDetailId || '';
    document.getElementById('noteModal').style.display = 'block';
}

// 開啟整筆訂單備註模態框
function openOrderNoteModal(orderId) {
    openNoteModal(orderId);
}

// 關閉備註模態框
function closeNoteModal() {
    document.getElementById('noteModal').style.display = 'none';
}

// 提交備註
function submitNote() {
    const form = document.getElementById('noteForm');
    form.submit();
}

// 開啟付款方式模態框
function openPaymentModal(orderId, totalPrice, restaurantID, availableTimes) {
    // 將 availableTimes 解析為 JSON 格式，確保它變成 JavaScript 陣列
    availableTimes = JSON.parse(availableTimes);

    // 如果 availableTimes 為空，顯示警告訊息並關閉模態框
    if (availableTimes.length === 0) {
        alert("目前店家無營業或不收單，無法前往結帳。");
        closePaymentModal();
        return;
    }
    // 設定隱藏欄位的值
    document.getElementById('paymentOrderId').value = orderId;
    document.getElementById('totalPrice').value = totalPrice;
    document.getElementById('restaurantID').value = restaurantID;

    console.log('Available pickup times:', availableTimes);

    // 獲取取餐時間下拉選單元素
    const pickupTimeSelect = document.getElementById('pickup_time');

    // 清空下拉選單的內容
    pickupTimeSelect.innerHTML = '<option value="" disabled selected>選擇取餐時間</option>';

    // 將 availableTimes 內的選項添加到下拉選單中
    availableTimes.forEach(time => {
        const option = document.createElement('option');
        option.value = time;
        option.textContent = time;
        pickupTimeSelect.appendChild(option);
    });

    // 顯示模態框
    document.getElementById('paymentModal').style.display = 'block';
}

// 關閉付款方式模態框
function closePaymentModal() {
    document.getElementById('paymentModal').style.display = 'none';
}

// 提交付款
function submitPayment() {
    const paymentMethodSelect = document.getElementById('payment_method');
    const pickupTimeSelect = document.getElementById('pickup_time');

    const selectedPaymentMethod = paymentMethodSelect.value;
    const selectedPickupTime = pickupTimeSelect.value;

    if (selectedPaymentMethod === "" && selectedPickupTime === "") {
        alert("請選擇付款方式和取餐時間！");
        return;  // 阻止提交
    } else if  (selectedPaymentMethod === ""){
        alert("請選擇付款方式！");
        return;
    }else if (selectedPickupTime === ""){
        alert("請選擇取餐時間！");
        return;
    }
    const form = document.getElementById('paymentForm');
    form.submit();
    alert("訂單已成功送出！");
}

// 刪除整筆訂單的警告
function confirmDeleteOrder() {
    return confirm("你確定要刪除整筆嗎？此操作無法恢復！");
}

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
