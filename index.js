// function onLoad() {
//     document.getElementById('customFile')
// }

function loadFile() {
    console.log("Loaded file");
}


// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function(evt) {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    console.log($(this).val());
    var reader = new FileReader();
    reader.addEventListener('load', (event) => {
        document.getElementById('text-box').innerHTML = event.target.result;
    })
    reader.readAsText(evt.target.files[0]);
});

function getSelected() {
    if(window.getSelection) { return window.getSelection(); }
    else if(document.getSelection) { return document.getSelection(); }
    else {
        var selection = document.selection && document.selection.createRange();
        if(selection.text) { return selection.text; }
        return false;
    }
    return false;
}
/* create sniffer */
$(document).ready(function() {
    $('#text-box').mouseup(function(event) {
        console.log($(document.getElementById('text-box')).height())
        console.log($('text-box').height())

        var selection = getSelected();
        selection = $.trim(selection);
        if(selection != ''){
            $("span.popup-tag").css("display","block");
            $("span.popup-tag").css("top",event.clientY/2);
            $("span.popup-tag").css("left",event.clientX/2);
            $("span.popup-tag").css("max-width", $(document.getElementById('text-box')).width()/2);
            $("span.popup-tag").css("max-height", $(document.getElementById('text-box')).height()/2);
            console.log(sendData(selection))
            $("span.popup-tag").text(selection);
        }else{
            $("span.popup-tag").css("display","none");
        }
    });
});


function sendData(string) {
    var data = new FormData();
    data.append('text', string);
    console.log(data);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/summarization', true);
    xhr.onload = function () {
        console.log(this.responseText);
    };
    xhr.send(data);
}