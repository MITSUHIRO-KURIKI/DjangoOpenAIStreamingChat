function CustomFileInputChangeHandler(e) {
	let files = e.target.files;
	for (var i = 0, f; f = files[i]; i++) {
		let reader = new FileReader();
		reader.onload = (function(theFile) {
			return function(e) {
				if (theFile.type.match('image.*')) {
					$("#CustomFileInputPreviewImage").attr('src', e.target.result);
				} else {
					$("#CustomFileInputPreviewImage").attr('src', "/static/templates/common/func/bs-custom-file-input/dummy.png");
				}
			};
		})(f);
		reader.readAsDataURL(f);
	};
};

document.getElementById('CustomFileInputReset').addEventListener('click', function(e){
    document.getElementById('CustomFileInput').value = '';
    let InitFileName = $('#CustomFileInitFile').text();
    $("#CustomFileInputPreviewImage").attr('src', InitFileName);
}, false);

// EventListener
document.getElementById('CustomFileInput').addEventListener('change', CustomFileInputChangeHandler, false);