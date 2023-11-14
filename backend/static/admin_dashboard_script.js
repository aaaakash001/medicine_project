$(document).ready(function () {
    $('#add-medicine-form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add_medicine',
            data: $(this).serialize(),
            success: function (response) {
                if (response.success) {
                    $('#result-message').text(response.message).removeClass('error').addClass('success');
                } else {
                    $('#result-message').text(response.message).removeClass('success').addClass('error');
                }
            }
        });
    });
});
