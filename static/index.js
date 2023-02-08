var image = document.getElementById('uploaded');

document.getElementById("img_file").addEventListener("change", (e) => {
	uploaded_file = e.target.files[0]
	image.src = URL.createObjectURL(uploaded_file);
	type = e.target.files[0].type.slice(0, 5)
	if (type != 'image') {
		alert("Invalid file")
		e.target.form.reset()
	}
})
var numImage = document.getElementById("range")
numImage.innerHTML = document.getElementById("customRange").value
document.getElementById("customRange").addEventListener("change", (e) => {
	value = e.target.value
	numImage.innerHTML = value
})





