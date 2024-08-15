
        function Hesab() {
        var totalPardakht = 0; // متغیر برای جمع کل پرداخت
        var totalBeforeDiscount = 0; // متغیر برای جمع کل قبل از تخفیف

        $('.product').each(function() {
            // دریافت مقادیر از تگ HTML
            var Gheimat = parseFloat($(this).data('price'));
            var sale = parseFloat($(this).data('discount')) / 100;
            var qty = parseInt($(this).find('.qty').html());

            // محاسبه مقدار پرداخت
            var pardakht = (Gheimat - (Gheimat * sale)) * qty;

            // اضافه کردن مبلغ کل قبل از تخفیف
            totalBeforeDiscount += Gheimat * qty;

            // نمایش مقدار پرداخت
            var pardakht2 = pardakht.toLocaleString();
            $(this).find('.Pardakht').html(pardakht2);

            totalPardakht += pardakht;

            // محاسبه سود
            var sood = totalBeforeDiscount - totalPardakht; // محاسبه سود که برابر است با قیمت قبل از تخفیف کم میشود از قیمت بعد از تخفیف
            var sood2 = sood.toLocaleString();
            $('.sood').html(sood2);
        });

    // نمایش مجموع قیمت کل محصولات
    var totalPardakhtFormatted = totalPardakht.toLocaleString();
    $('.Col-Pardakht').html(totalPardakhtFormatted);

    // نمایش مجموع قیمت کل قبل از تخفیف
    var totalBeforeDiscountFormatted = totalBeforeDiscount.toLocaleString();
    $('.total').html(totalBeforeDiscountFormatted);
}

// فراخوانی تابع
Hesab();
//




































//
// $(document).on('click', '.bx-plus', function() {
//     if (qty < 10) {
//         qty++;
//         $('.Quantity-Number').html(qty);
//         totalPrice = qty * price;
//         $('.total-price').html(totalPrice);
//     }
// });
//
// $(document).on('click', '.bx-minus', function() {
//     if (qty > 0) {
//         qty--;
//         $('.Quantity-Number').html(qty);
//         totalPrice = qty * price;
//         $('.total-price').html(totalPrice);
//     }
// });