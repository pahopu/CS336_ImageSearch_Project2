var cropBtn = $(".crop-btn")[0]
var cropImg = $(".cropped-image")[0]
var inputStatusP = $(".input-status")[0]
var searchBtn = $("#search-btn")[0]
var alertPopup = $("#alert-section")[0]

cropBtn.addEventListener("click", () => {
    cropImg.style.marginTop = "50px";
    inputStatusP.hidden = true;
})

alertNoFile = $("#alert-no-file")[0].value;

if (alertNoFile == 1){
    alertPopup.innerHTML = "<div class='alert alert-warning alert-dismissible fade show' role='alert'>Please choose image for searching!<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>";
}

