/* JS */
$(document).ready(function(){
	// ADD TO CART
	// 	* class="add-to-cart"
	// 	* product-id="product.id"
	$(".add-to-cart").on("click", function(evt){
		var product_id = $(this).attr("product-id");
		alert("Added to cart. Product id: " + product_id);
		evt.preventDefault();
	});

	// ADD TO WISHLIST
	// 	* class="add-to-wishlist"
	// 	* product-id="product.id"
	$(".add-to-wishlist").on("click", function(evt){
		var product_id = $(this).attr("product-id");
		alert("Added to wishlist. Product id: " + product_id);
		evt.preventDefault();
	});
});