$(document).ready(function() {
    $('#prediction-form').on('submit', function(e) {
        e.preventDefault();
        
        // Hide any existing error messages and results
        $('#error-message').addClass('hidden');
        $('#result').addClass('hidden');
        
        // Show loading state
        $('.predict-button').prop('disabled', true).text('Predicting...');
        
        // Collect form data
        const formData = new FormData(this);
        
        // Make prediction request
        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    // Display the prediction
                    $('#prediction-value').text(response.prediction.toFixed(2) + ' MPa');
                    $('#result').removeClass('hidden');
                } else {
                    // Show error message
                    $('#error-message')
                        .text(response.error || 'An error occurred while making the prediction.')
                        .removeClass('hidden');
                }
            },
            error: function(xhr, status, error) {
                // Show error message
                $('#error-message')
                    .text('Failed to get prediction. Please try again.')
                    .removeClass('hidden');
            },
            complete: function() {
                // Reset button state
                $('.predict-button').prop('disabled', false).text('Predict Strength');
            }
        });
    });

    // Input validation
    $('input[type="number"]').on('input', function() {
        const value = parseFloat($(this).val());
        const min = parseFloat($(this).attr('min'));
        
        if (value < min) {
            $(this).addClass('invalid');
        } else {
            $(this).removeClass('invalid');
        }
    });
});