/* JS */
$(document).ready(function(){
	// ADD TO CART
	// 	* class="add-to-cart"
	// 	* product-id="product.id"
	// 	* quantity
	// 	* client_id
	$(".add-to-cart").on("click", function(evt){
		var shop_url = $("article").attr("shop-url");
		var product_id = $(this).attr("product-id");
		var client_id = 9; // [TODO] Logged in client id must be here.
		var quantity = 1; // [TODO] Select custom quantity - option
		evt.preventDefault();

		$.ajax({
			type:'GET',
			url: shop_url,
			data: { 'add_to_cart': true,
					'product_id': product_id,
					'client_id': client_id,
					'quantity': quantity},
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			// DONE [TODO] Message?
		});
	});

	// REMOVE FROM CART
	// 	* class="remove-from-cart"
	// 	* product-id="product.id"
	// 	* quantity
	// 	* client_id
	$(".remove-from-cart").on("click", function(evt){
		var shop_url = $("article").attr("shop-url");
		var product_id = $(this).attr("product-id");
		var client_id = 9; // [TODO] Logged in client id must be here.
		var quantity = 1; // [TODO] Select custom quantity - option
		evt.preventDefault();

		$.ajax({
			type:'GET',
			url: shop_url,
			data: { 'remove_from_cart': true,
					'product_id': product_id,
					'client_id': client_id,
					'quantity': quantity},
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			// DONE [TODO] Message?
		});
	});

	// ADD TO WISHLIST
	// 	* class="add-to-wishlist"
	// 	* product-id="product.id"
	$(".add-to-wishlist").on("click", function(evt){
		var shop_url = $("article").attr("shop-url");
		var product_id = $(this).attr("product-id");
		var client_id = 9; // [TODO] Logged in client id must be here.
		evt.preventDefault();

		$.ajax({
			type:'GET',
			url: shop_url,
			data: { 'add_to_wishlist': true,
					'product_id': product_id,
					'client_id': client_id},
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			// DONE [TODO] Message?
		});
	});

	// REMOVE FROM WISHLIST
	// 	* class="remove-to-wishlist"
	// 	* product-id="product.id"
	$(".remove-from-wishlist").on("click", function(evt){
		alert("Clicked");
		var shop_url = $("article").attr("shop-url");
		var product_id = $(this).attr("product-id");
		var client_id = 9; // [TODO] Logged in client id must be here.
		evt.preventDefault();

		$.ajax({
			type:'GET',
			url: shop_url,
			data: { 'remove_from_wishlist': true,
					'product_id': product_id,
					'client_id': client_id},
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			// DONE [TODO] Message?
		});
	});
});
