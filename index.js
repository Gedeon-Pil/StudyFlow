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
    var files = evt.target.files
    // reader.addEventListener('load', (event) => {
    //
    // })
    console.log(reader.readAsText(files[0]));
    console.log(files);
});

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object
    console.log(files)
    // files is a FileList of File objects. List some properties.
    // var output = [];
    // for (var i = 0, f; f = files[i]; i++) {
    //     output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
    //         f.size, ' bytes, last modified: ',
    //         f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
    //         '</li>');
    // }
    // document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

document.getElementById('files').addEventListener('change', handleFileSelect, false);