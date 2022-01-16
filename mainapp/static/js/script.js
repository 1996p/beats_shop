(function (){
    function change_price() {
        let current_price = document.querySelectorAll('.product-price')
        for (let price of current_price) {
            let price_value = price.textContent
            price.textContent = price_value.replace(/(\d{1,3}(?=(?:\d\d\d)+(?!\d)))/g, "$1" + '.')
        }
    }
    addEventListener("DOMContentLoaded", function (){
        change_price()
    });
})();

