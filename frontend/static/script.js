var fileTypes = ['pdf'];  //acceptable file types
function readURL(input) {
    if (input.files && input.files[0]) {
        console.log(input.files[0]);
        var extension = input.files[0].name.split('.').pop().toLowerCase(),  //file extension from input file
            isSuccess = fileTypes.indexOf(extension) > -1;  //is extension in acceptable types
        console.log(fileTypes.indexOf(extension));
        console.log(isSuccess);
        if (isSuccess) { //yes
            var reader = new FileReader();
            reader.onload = function (e) {
                if (extension == 'pdf'){
                    $(input).closest('.fileUpload').find(".icon").attr('src','https://image.flaticon.com/icons/svg/179/179483.svg');
                
                    var files = $("input").val();
                    // alert(files);
                    if(files.length > 0 ){
                        var form_data = new FormData();
                        form_data.append('file', $('#up').prop('files')[0]);
                        
                        $(function() {
                            $.ajax({
                                type: 'POST',
                                url:  '/uploadFile',
                                data: form_data,
                                contentType: false,
                                cache: false,
                                processData: false,
                                success: function(data) {
                                    // alert(data);
                                    const fileInput = document.querySelector('input[type=file]');
                                    const path = fileInput.value;
                                    const fileName = path.split(/(\\|\/)/g).pop();
                                    // console.log('File name:', fileName);
                                    var viewfile = $(".fileviewer");
                                    viewfile.attr("href", "viewUploaded/" + fileName);
                                    viewfile.css("display", "inline-block");
                                    $.toast({
                                        text: 'Successfully uploaded',
                                        heading: 'Yaay!',
                                        showHideTransition: 'slide',
                                        hideAfter: 3000,
                                        stack: false,
                                        position: {
                                           right: 5,
                                            top: 120
                                        },
                                        icon: 'success',
                                        loader: false,
                                        bgColor: '00FF35',
                                    });

                                    var dwn = $(".btn-dwn");
                                    // dwn.css("display", "none");
                                    dwn.fadeOut();

                                    var submitButton = document.getElementsByClassName("btn-next")[0];
                                    submitButton.classList.remove("disabled"); 
                                },
                                fail: function(xhr, textStatus, errorThrown){
                                    alert("Oops! Something went wrong. Please try again");
                                }
                            })
                        });
                        // alert("Upload successful");
                    }
                    else{
                        $.toast({
                            text: 'Please upload a document',
                            heading: 'Uh-oh',
                            showHideTransition: 'fade',
                            hideAfter: 3000,
                            stack: false,
                            position: {
                               right: 5,
                                top: 120
                            },
                            icon: 'error',
                            loader: false,
                            bgColor: '#ff0033',
                        })
                    }
                }
                else {
                    //console.log('here=>'+$(input).closest('.uploadDoc').length);
                    $.toast({
                        text: 'Only PDF files supported',
                        heading: 'Err!',
                        showHideTransition: 'fade',
                        hideAfter: 3000,
                        stack: false,
                        position: {
                           right: 5,
                            top: 120
                        },
                        icon: 'warning',
                        loader: false,
                        bgColor: '#FF9E00',
                    })
                    var files = $("input").val(null);

                    var viewfile = $(".fileviewer");
                    viewfile.css("display", "none");
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
                //console.log('here=>'+$(input).closest('.uploadDoc').find(".docErr").length);
                $.toast({
                    text: 'Only PDF files supported',
                    heading: 'Err!',
                    showHideTransition: 'fade',
                    hideAfter: 3000,
                    stack: false,
                    position: {
                       right: 5,
                        top: 120
                    },
                    icon: 'warning',
                    loader: false,
                    bgColor: '#D91212',
                })  
            var files = $("input").val(null);
            var viewfile = $(".fileviewer");
            viewfile.css("display", "none");
        }
    }
}

$(document).ready(function(){
    // alert("Doing");
    // $('.toast').toast('show');

    $(document).on("click", "a.btn-next" , function() {
        // alert($('.toast'));
        var files = $("input").val();
        if(files.length < 1){
            // alert("Please upload a document");
            $.toast({
                text: 'Please upload a document',
                heading: 'Uh-oh',
                showHideTransition: 'fade',
                hideAfter: 3000,
                stack: false,
                position: {
                   right: 5,
                    top: 120
                },
                icon: 'error',
                loader: false,
                bgColor: '#D91212',
            })
        }
        else{
            // alert("Doing something");
            var ele = document.getElementsByName('os');
            for(i = 0; i < ele.length; i++) {
                if(ele[i].checked)
                    var os = ele[i].value;
            }
            var form_data = new FormData();
            form_data.append('file', $('#up').prop('files')[0]);
            // form_data.append("os", os);
            console.log(form_data);
            var submitButton = document.getElementsByClassName("btn-next")[0];
            submitButton.classList.add("disabled"); 

            var wait_text = $("#wait_text");
            wait_text.fadeIn(500).css("display","block");
            $.ajax({
                type: 'POST',
                url:  '/submitFile/' + os,
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    var dwn = $(".btn-dwn");
                    dwn.attr("href", "download/" + "package.zip");
                    wait_text.fadeOut(100).css("display","none");

                    dwn.fadeIn(500).css("display","inline-block");

                    var submitButton = document.getElementsByClassName("btn-next")[0];
                    submitButton.classList.add("disabled"); 

                },
                fail: function(xhr, textStatus, errorThrown){
                    alert("Oops! Something went wrong. Please try again");
                }
            })
        }
    });

    $(document).on('change','.up', function(){
        var id = $(this).attr('id'); /* gets the filepath and filename from the input */
        var profilePicValue = $(this).val();
        var fileNameStart = profilePicValue.lastIndexOf('\\'); /* finds the end of the filepath */
        profilePicValue = profilePicValue.substr(fileNameStart + 1).substring(0,20); /* isolates the filename */
        //var profilePicLabelText = $(".upl"); /* finds the label text */
        if (profilePicValue != '') {
            //console.log($(this).closest('.fileUpload').find('.upl').length);
            $(this).closest('.fileUpload').find('.upl').html(profilePicValue); /* changes the label text */
        }
    });
});
