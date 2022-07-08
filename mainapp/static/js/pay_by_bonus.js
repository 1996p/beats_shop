(function (){

    addEventListener("DOMContentLoaded", function (){
    let input = document.getElementById('id_bonus_count')
    let finalPrice = document.getElementById('final-price');
    let finalPriceValue = parseFloat(finalPrice.innerText.slice(16).replaceAll('.', ''))
    let bonusBalance = document.getElementById('bonus-balance')
    let bonusBalanceValue = parseInt(bonusBalance.innerText.replaceAll('.',''))


    input.oninput = function () {
        if (input.value > finalPriceValue) {
            input.value = finalPriceValue
            finalPrice.innerText = 'Итого к оплате: 0 ₽'
        } else if (input.value > bonusBalanceValue) {
            input.value = bonusBalanceValue
            finalPrice.innerText = 'Итого к оплате: ' + (parseFloat(finalPriceValue) - input.value).toString().replace(/(\d{1,3}(?=(?:\d\d\d)+(?!\d)))/g, "$1" + '.')+ ',00 ₽'
        } else {
            finalPrice.innerText = 'Итого к оплате: ' + (parseFloat(finalPriceValue) - input.value).toString().replace(/(\d{1,3}(?=(?:\d\d\d)+(?!\d)))/g, "$1" + '.')+ ',00 ₽'
        }
    }
    });


})();
