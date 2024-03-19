// Timer for alerts
setTimeout(function () {
  $(".alert").alert("close");
}, 5000);

console.log("scripts.js working");

$(document).ready(function () {
  $(".owl-carousel").owlCarousel({
    loop: true,
    margin: 15,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000, // Set autoplay speed in milliseconds (e.g., 3000ms = 3 seconds)
    dots: false,
    responsive: {
      0: {
        items: 1, // Display 1 item on screens smaller than 600px
      },
      576: {
        items: 2, // Display 2 items on screens between 576px and 767px
      },
      768: {
        items: 3, // Display 3 items on screens between 768px and 991px
      },
      992: {
        items: 4, // Display 4 items on screens between 992px and 1199px
      },
      1200: {
        items: 6, // Display 6 items on screens larger than or equal to 1200px
      },
    },
  });

  console.log("Checkbox ready");
  $(".filter-checkbox,#price-filter-btn").on("click", function () {
    console.log("Checkbox clicked");
    let filter_object = {};

    // for price filtering
    let min_price = $("#max_price").attr("min");
    let max_price = $("#max_price").val();

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function () {
      let filter_value = $(this).val();
      let filter_key = $(this).data("filter");

      // console.log(filter_key, 'filter_key');
      // console.log(filter_value, 'filter_value');

      filter_object[filter_key] = Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filter_key + "]:checked"
        )
      ).map(function (element) {
        return element.value;
      });
    });
    console.log("filter_object", filter_object);
    $.ajax({
      url: "/filter-products",
      data: filter_object,
      dataType: "json",
      beforeSend: function () {
        console.log("trying to filter product");
      },
      success: function (response) {
        console.log(response, "ajax filter success");
        $("#filtered-product").html(response.data);
      },
    });
  });

  //checking for input range slider exceeds value
  $("#max_price").on("blur", function () {
    let min_price = $(this).attr("min");
    let max_price = $(this).attr("max");
    let current_price = $(this).val();

    console.log("current_price", current_price);
    console.log("max_price", max_price);
    console.log("min_price", min_price);

    if (
      current_price < parseInt(min_price) ||
      current_price > parseInt(max_price)
    ) {
      console.log("invalid price");
      min_PRICE = Math.round(min_price * 100) / 100;
      max_PRICE = Math.round(max_price * 100) / 100;

      console.log(min_PRICE);
      console.log(max_PRICE);

      alert(
        " Price must be between $" + min_PRICE + " and $" + max_PRICE + "!"
      );
      // resetting the slider and inputs
      $(this).val(min_PRICE);
      $("#range").val(min_PRICE);
      $(this).focus();

      return false;
    }
  });
});

$("#review_Form").submit(function (e) {
  e.preventDefault();

  // Perform AJAX call
  $.ajax({
    data: $(this).serialize(),
    method: $(this).attr("method"),
    url: $(this).attr("action"),
    dataType: "json",
    success: function (response) {
      console.log("Ajax success: data saved to database");

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
        console.log("Review not saved to database");
      }
    },
    error: function (xhr, status, error) {
      console.error("Ajax error:", error);
    },
  });
});

// add to cart
$(".add-to-cart-btn").on("click", function () {
  console.log("add to cart clicked");

  let this_val = $(this);
  let index = this_val.attr("data-index");

  let quantity = $(".product-quantity-" + index).val();
  let product_title = $(".product-title-" + index).val();
  let product_id = $(".product-id-" + index).val();
  let product_price = $(".current-product-price-" + index).text();
  let product_pid = $(".product-pid-" + index).text();
  let product_image = $(".product-image-" + index);

  console.log(
    quantity,
    "quantity",
    product_title,
    "product_title"
    // product_id,
    // "product_id",
    // product_price,
    // "product_price",
    // product_pid,
    // "product_pid",
    // product_image,
    // "product_image",
    // index,
    // "index"
  );

  //   $.ajax({
  //     url: "/add-to-cart",
  //     data: {
  //       id: product_id,
  //       title: product_title,
  //       price: product_price,
  //       quantity: quantity,
  //     },
  //     dataType: "json",

  //     beforeSend: function () {
  //       console.log("trying to add to cart");
  //     },

  //     success: function (response) {
  //       // $(this).html("Added To Cart");
  //       // this_val.html("Added To Cart");
  //       $("#add-to-cart-btn").html("Added To Cart");
  //       console.log("add to cart success");
  //     },
  //   });
});

// // add to cart
// $(".add-to-cart-btn").on("click", function () {
//     console.log("add to cart clicked");
//     let quantity = $("#product-quantity").val();
//     let product_title = $(".product-title").val();
//     let product_id = $(".product-id").val();
//     let product_price = $(".product-price").text();

//     console.log(quantity, product_title, product_id, product_price);

//     $.ajax({
//         url: "/add-to-cart",
//         data: {
//             id: product_id,
//             title: product_title,
//             price: product_price,
//             quantity: quantity,
//         },
//         dataType: "json",

//         beforeSend: function () {
//             console.log("trying to add to cart");
//         },

//         success: function (response) {
//             // $(this).html("Added To Cart");
//             // this_val.html("Added To Cart");
//             $("#add-to-cart-btn").html("Added To Cart");
//             console.log("add to cart success");
//         },
//     });
// });
