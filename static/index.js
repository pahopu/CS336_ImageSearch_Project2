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