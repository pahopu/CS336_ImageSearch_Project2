<<<<<<< HEAD
<<<<<<< HEAD
var inputImage = document.getElementsByClassName('cropped-image')[0]

inputImage.addEventListener("change", () => {
    if (inputImage.src !== ""){
        inputImage.style.marginTop = "10px";
        alert("hehehehheh")
    }
})
=======
var dismissBtn = $('.dm-modal');


var numImage = document.getElementById("range")
numImage.innerHTML = document.getElementById("customRange").value
document.getElementById("customRange").addEventListener("change", (e) => {
	value = e.target.value
	numImage.innerHTML = value
})

//for (let i = 0; i < dismissBtn.length; i++) {
//    dismissBtn[i].addEventListener("click", () => {
//        $("form")[0].reset()
//    })
//}
>>>>>>> 980a0eea797939db785415859ede40acbc451f7c
=======
var dismissBtn = $('.dm-modal');


var numImage = document.getElementById("range")
numImage.innerHTML = document.getElementById("customRange").value
document.getElementById("customRange").addEventListener("change", (e) => {
	value = e.target.value
	numImage.innerHTML = value
})

//for (let i = 0; i < dismissBtn.length; i++) {
//    dismissBtn[i].addEventListener("click", () => {
//        $("form")[0].reset()
//    })
//}
>>>>>>> ff67239562e1965db44a89e3fedd424cc2c12461
