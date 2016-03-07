+ function($) {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var uploadForm = document.getElementById('imagesubmit');

    var startUpload = function(files) {
        console.log(files)
    }

    uploadForm.addEventListener('submit', function(e) {
        var uploadFiles = document.getElementById('js-upload-files').files;
        e.preventDefault()

        startUpload(uploadFiles)
    })

}(jQuery);