// Get Stripe publishable key

fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  console.log("stripe config")
  const stripe = Stripe(data.publicKey);

// new
// Event handler
document.querySelector("#creditCard").addEventListener("click", () => {
  // Get Checkout Session ID
  // pass input values to backend
  console.log("clicked")
  let num = Number(document.getElementById("NFT").value);
  
  fetch(`/create-checkout-session?` + new URLSearchParams({number: `${num}`}))
  .then((result) => { return result.json(); })
  .then((data) => {
    console.log(data);
    /// Redirect to Stripe Checkout
    return stripe.redirectToCheckout({sessionId: data.sessionId})
  })
  .then((res) => {
      console.log(res);
    });
  });
});
