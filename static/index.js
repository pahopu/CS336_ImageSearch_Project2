var inputImage = document.getElementsByClassName('cropped-image')[0]

inputImage.addEventListener("change", () => {
    if (inputImage.src !== ""){
        inputImage.style.marginTop = "10px";
        alert("hehehehheh")
    }
})