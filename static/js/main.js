let update_button = document.getElementsByClassName('update-card')

for (let i = 0; i < update_button.length; i++) {
    update_button[i].addEventListener("click", function () {
        let product_id = this.dataset.product
        let action = this.dataset.action
        console.log("product_id:", product_id, "action:", action)
        console.log("USER:", user)
        if (user === 'AnonymousUser') {
            add_cookie_item(product_id, action)
        } else {
            update_user_order(product_id, action)
        }
    })
}

function add_cookie_item(product_id, action) {
    console.log("User is not authenticated...")
    if (action === "add") {
        if (cart[product_id] === undefined) {
            cart[product_id] = {"quantity": 1}
        } else {
            cart[product_id]['quantity'] += 1
        }
    }
    if(action==="remove"){
        cart[product_id]['quantity']-=1
        if (cart[product_id]['quantity'] <=0) {
            console.log("Item was removed...")
            delete cart[product_id]
        }
    }
    console.log("CART:", cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}


function update_user_order(product_id, action) {
    console.log('User is authenticated, sending data...')

    let url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product_id': product_id, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(data)
            location.reload()
        });
}