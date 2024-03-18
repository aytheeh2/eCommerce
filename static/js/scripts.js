// Timer for alerts
setTimeout(function () {
    $(".alert").alert("close");
}, 5000);

console.log('scripts.js working');

$(document).ready(function () {
    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 15,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000, // Set autoplay speed in milliseconds (e.g., 3000ms = 3 seconds)
        dots: false,
        responsive: {
            0: {
                items: 1 // Display 1 item on screens smaller than 600px
            },
            576: {
                items: 2 // Display 2 items on screens between 576px and 767px
            },
            768: {
                items: 3 // Display 3 items on screens between 768px and 991px
            },
            992: {
                items: 4 // Display 4 items on screens between 992px and 1199px
            },
            1200: {
                items: 6 // Display 6 items on screens larger than or equal to 1200px
            }
        }
    });



    console.log('Checkbox ready');
    $(".filter-checkbox").on("click", function () {
        console.log('Checkbox clicked');
    });


});

// Product review AJAX
// Your AJAX code for submitting product reviews would go here
// Make sure it's structured properly and handles success and error cases


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



