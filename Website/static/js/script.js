function Hesab() {
    var totalPardakht = 0; // متغیر برای جمع کل پرداخت
    var totalBeforeDiscount = 0; // متغیر برای جمع کل قبل از تخفیف

    $('.product').each(function () {
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


$(document).on('click', '.bx-plus', function () {
    // پیدا کردن مقدار مربوط به `.Quantity-Number` در کنار دکمه‌ای که کلیک شده است
    var qtyElement = $(this).siblings('.Quantity-Number');
    var qty = parseInt(qtyElement.html());

    if (qty < 10) {
        qty = qty + 1;
        qtyElement.html(qty);
        updateTotal(this)
    }
});

$(document).on('click', '.bx-minus', function () {
    // پیدا کردن مقدار مربوط به `.Quantity-Number` در کنار دکمه‌ای که کلیک شده است
    var qtyElement = $(this).siblings('.Quantity-Number');
    var qty = parseInt(qtyElement.html());

    if (qty > 0) {
        qty = qty - 1;
        qtyElement.html(qty);
        updateTotal(this)
    }


});

function updateTotal(element) {
    var productDiv = $(element).closest('.product');
    var price = parseFloat(productDiv.data('price'));
    var discount = parseFloat(productDiv.data('discount'));
    var quantity = parseInt(productDiv.find('.Quantity-Number').text());

    // محاسبه مبلغ پرداختی با احتساب تخفیف
    var discountedPrice = price - (price * (discount / 100));
    var totalPrice = discountedPrice * quantity;

    productDiv.find('.Pardakht').html(totalPrice.toLocaleString());
}


$(document).on('click', '.close-tabliq', function () {
    $('.tabliq').fadeToggle();
})
