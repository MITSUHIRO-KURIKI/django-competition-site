/*@cc_on _d=document;eval('var document=_d')@*/

// Display filename
bsCustomFileInput.init();
// Clear File Selection
document.getElementById('inputFileReset').addEventListener('click', function (e) {
    var elem = document.getElementById('inputFile');
    elem.value = '';
    elem.dispatchEvent(new Event('change'));
    var fileset = $(this).val();
    if (fileset === '') {
        $("#preview_img").attr('src', "/static/templates/include/bs-custom-file-input/dummy.png");
    } else {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#preview_img").attr('src', e.target.result);
        }
        reader.readAsDataURL(e.target.files[0]);
    }
});

// File preview
$('#inputFile').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#preview_img").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});