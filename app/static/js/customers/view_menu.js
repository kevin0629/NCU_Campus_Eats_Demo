function confirmAddToCart(itemname) {
    if (confirm("你確定要將"+itemname+"加入「1」份至購物車嗎？")) {
        return true; // 允許表單提交
    } else {
        return false; // 阻止表單提交
    }
}