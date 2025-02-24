function validateAddItemForm() {
    const price = document.querySelector('[name="price"]').value;
    const status = document.querySelector('[name="status"]').value;

    if (price < 0) {
        alert('請妥善設置餐點價格 (不可為負數)');
        return false;
    }

    if (status > 1 || status < 0) {
        alert('請妥善設置餐點狀態 (0停售、1販售中)');
        return false;
    }

    return confirm('確定要新增這個餐點嗎？');
}