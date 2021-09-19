// function onLoad() {
//     document.getElementById('customFile')
// }
let fileLoaded;
let fileText;
let fileName;
let customName;
let queryType;

function loadFile() {
    customName = document.getElementById('userCustomFileName').value;
    console.log(customName)
    if(customName == ''){
        customName = fileName;
    }
    let reader = new FileReader();
    reader.addEventListener('load', (event) => {
        fileText = event.target.result;
        document.getElementById('text-box').innerHTML = fileText;
        addEditBtn();
    })
    reader.readAsText(fileLoaded);
}


// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function(evt) {
    fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    console.log($(this).val());
    fileLoaded = evt.target.files[0];
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
            sendData(queryType, selection, "span.popup-tag");
        }else{
            $("span.popup-tag").css("display","none");
        }
    });
});

/* Gedeon's Stuff */
/*Send post request*/
function sendData(key, value, id) {
    var data = new FormData();
    data.append(key, value);
    console.log(data);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:5000/query', true);
    xhr.onload = function () {
        let response = JSON.parse(this.responseText)
        console.log(this.responseText);
        console.log(response)
        console.log(response['output'])

        $(id).text(response['output']);
    };
    xhr.send(data);
}

/*Add file*/ 
var addBtn = document.getElementById('add-btn');
var fileContentsDict = {};
 
function addEditBtn() {
    var table = document.getElementById("myTable");
    var row = table.insertRow(-1);
    var cellInstruction = row.insertCell(-1);
    var button = document.createElement('button');
    var remove = document.createElement('button');
    button.setAttribute('class', 'btn btn-secondary');
    button.setAttribute('type', 'button');
    button.innerHTML = customName; // Make the custom name the button name
    button.setAttribute('name', customName);

    // Add filename: filecontents to dictionary
    fileContentsDict[customName] = fileText;
    console.log(fileContentsDict);

    // Add event listener that changes contents in view
    button.addEventListener('click', (event) => {
        document.getElementById('text-box').innerHTML = fileContentsDict[event.target.name];
    });

    remove.setAttribute('style', 'background-color: red');
    remove.addEventListener('click', function(e) {
        //Remove filename:filecontents from dictionary
        delete fileContentsDict[e.currentTarget.parentNode.name];
        e.currentTarget.parentNode.remove();
        document.getElementById('text-box').innerHTML = "";
    }, false);
    remove.innerHTML = "X";
    button.appendChild(remove);
    cellInstruction.appendChild(button);
}

function submitCustomQuery() {
    let selection = document.getElementById("userCustomQuery").innerHTML
    console.log(selection)
    sendData(queryType, selection, "span.resultCustomQuery")
}

var option1Button = document.getElementById('option1');
var option1Button = document.getElementById('option2');
var option1Button = document.getElementById('option3');
var option1Button = document.getElementById('option4');

option1.addEventListener('click', 
    queryType = "summarize"
);
option2.addEventListener('click', 
    queryType = "define"
);
option1.addEventListener('click', 
    queryType = "elaborate"
);
option1.addEventListener('click', 
    queryType = "custom"
);