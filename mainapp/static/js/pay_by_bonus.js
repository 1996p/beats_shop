(function (){

    addEventListener("DOMContentLoaded", function (){
    let input = document.getElementById('id_bonus_count')
    let finalPrice = document.getElementById('final-price');
    let finalPriceValue = parseFloat(finalPrice.innerText.slice(16).replace('.', ''))
    input.oninput = function () {
        if (input.value > finalPriceValue) {
            input.value = finalPriceValue
            finalPrice.innerText = 'Итого к оплате: 0 ₽'
        } else {
            console.log((parseFloat(finalPriceValue) - input.value))
            finalPrice.innerText = 'Итого к оплате: ' + (parseFloat(finalPriceValue) - input.value).toString().replace(/(\d{1,3}(?=(?:\d\d\d)+(?!\d)))/g, "$1" + '.')+ ',00 ₽'
        }
    }
    });


})();
