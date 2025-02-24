function showForm(role) {
    // 隱藏所有表單
    document.getElementById('customer-form').classList.remove('active');
    document.getElementById('restaurant-form').classList.remove('active');

    // 顯示所選角色的表單，並添加 active 類
    if (role === 'customer') {
        document.getElementById('customer-form').classList.add('active');
    } else if (role === 'restaurant') {
        document.getElementById('restaurant-form').classList.add('active');
    }
}

function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

function getEmailFieldName(formId) {
    return formId === 'customer-form' ? 'email' : 'manager_email';
}

function validatePasswordForm(formId) {
    let password = document.querySelector(`#${formId} input[name="password"]`).value;
    let confirmPassword = document.querySelector(`#${formId} input[name="confirm_password"]`).value;
    let emailFieldName = getEmailFieldName(formId);
    let email = document.querySelector(`#${formId} input[name="${emailFieldName}"]`).value;

    if (password.length < 8) {
        alert("密碼長度至少8個字符！");
        return false;
    }

    if (password !== confirmPassword) {
        alert("密碼與確認密碼不一致！");
        return false;
    }

    if (!validateEmail(email)) {
        alert("無效的電子郵件格式！");
        return false;
    }

    if (formId === 'restaurant-form'){
        const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        const timePattern = /^\d{2}:\d{2}~\d{2}:\d{2}$/;

        for (const day of days) {
            const inputs = document.querySelectorAll(`[name="${day}[]"]`);
            
            for (const input of inputs) {
                const value = input.value.trim();

                console.log(`${day} 的時段: ${value}`);
                
                if (value) {
                    // 驗證時間格式
                    if (!timePattern.test(value)) {
                        alert(`${day} 的時間格式不正確 (應為 HH:MM~HH:MM)`);
                        return false;
                    }

                    const [start, end] = value.split("~");
                    if (start >= end) {
                        alert(`${day} 的時段開始時間必須早於結束時間`);
                        return false;
                    }
                }
            }
        }
    }
    return true;
}
