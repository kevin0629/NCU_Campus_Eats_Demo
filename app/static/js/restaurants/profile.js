function validateEditStoreForm() {
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
    return true;
}