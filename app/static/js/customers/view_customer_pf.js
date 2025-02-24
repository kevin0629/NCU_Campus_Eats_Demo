// 確認修改個人資料的函數
function confirmEditProfile() {
    return confirm("您確定要修改您的個人資料嗎？");
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