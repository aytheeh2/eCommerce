// Timer for alerts
setTimeout(function () {
    $(".alert").alert("close");
}, 5000);

// Product review AJAX
// Your AJAX code for submitting product reviews would go here
// Make sure it's structured properly and handles success and error cases
console.log('working');

const MonthNames = [
    'Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

$("#review_Form").submit(function (e) {
    e.preventDefault();

    // Perform AJAX call
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log('Ajax success: data saved to database');

            if (response.bool == true) {
                // Hide the review form
                $("#review_div").hide();

                // Extract review data from response
                var user = response.context.user;
                var review = response.context.review;
                var rating = response.context.rating;
                var date = response.context.date;

                // Construct HTML for the review card
                var reviewCardHtml = `
                        <div class="card border m-3 p-3">
                            <div class="card-body">
                                <div class="row align-items-center">
                                    <div class="col-md-8">
                                        <h5 class="card-title">${user}</h5>
                                        <p class="card-text mb-1">${date}</p>
                                    </div>
                                    <div class="col-md-4 text-md-end">
                                        <span class="badge bg-primary">${rating}/5 <i class="bi bi-star-fill"></i></span>
                                    </div>
                                </div>
                                <p class="card-text">${review}</p>
                            </div>
                        </div>
                    `;

                // Append the review card HTML to the designated element
                $("#display_after_review_posted").append(reviewCardHtml);
            } else {
                console.log('Review not saved to database');
            }
        },
        error: function (xhr, status, error) {
            console.error('Ajax error:', error);
        }
    });
});
