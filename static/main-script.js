var actionButton = document.querySelectorAll('.action-button')[0]
var image_workspaceSpan = document.querySelector('.image-workspace span')
var preview_containerSpan = document.querySelector('.preview-container span')
var aspectRatio = document.querySelectorAll('.side-control-page-2 button')
var form_x = document.getElementById("x_coor")
var form_y = document.getElementById("y_coor")
var form_width = document.getElementById("img_width")
var form_height = document.getElementById("img_height")

var cropped_image = $(".cropped-image")[0]

$("#img_file")[0].onchange = (e) => {
    $(".im-wrapper")[0].innerHTML =  `<img id="image">`
    $("#modaltriger")[0].click()
    var image = document.querySelector('#image')
    var file = e.target.files[0]
    var url = window.URL.createObjectURL(new Blob([file], { type : 'image/jpg' }))
    image.src = url

    var options = {
        dragMode: 'move',
        preview: '.img-preview',
        viewMode: 3,
        ready: function(){
            // set aspect ratio
            aspectRatio[0].onclick = () => cropper.setAspectRatio(1.7777777777777777)
            aspectRatio[1].onclick = () => cropper.setAspectRatio(1.3333333333333333)
            aspectRatio[2].onclick = () => cropper.setAspectRatio(1)
            aspectRatio[3].onclick = () => cropper.setAspectRatio(0.6666666666666666)
            aspectRatio[4].onclick = () => cropper.setAspectRatio(0) // free

            // download cropped image
            actionButton.onclick = () => {
                cropper.getCroppedCanvas().toBlob((blob) => {
                    var downloadUrl = window.URL.createObjectURL(blob)
                    cropped_image.src = downloadUrl
                })

                img_data = cropper.getData(true)
                form_x.value = img_data.x
                form_y.value = img_data.y
                form_height.value = img_data.height
                form_width.value = img_data.width

                $(".dm-modal")[0].click()
            }
        }
    }

    var cropper = new Cropper(image, options)

}
