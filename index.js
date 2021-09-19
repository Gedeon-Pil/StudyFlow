let fileLoaded;
let fileText;
let fileName;
let customName;
let queryType;
var fileContentsDict = {};

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


// Function used to place selected file name into input field
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
// Define function to capture selected text and call backend to analyze that text.
$(document).ready(function() {
    $('#text-box').mouseup(function(event) {
        var selection = getSelected();
        selection = $.trim(selection);
        if(selection != ''){
            sendData(queryType, selection);
        }
    });
});

// Function to send data highlighted or typed by the user.
function sendData(key, value) {
    var data = new FormData();
    data.append(key, value);
    console.log("Sending request with action: " + key);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://mitosborn.pythonanywhere.com/query', true);
    xhr.onload = function () 
    {
        let response = this.responseText
        console.log(this.responseText);

        document.getElementById('resultCustomQuery').innerHTML= response;
    };
    xhr.send(data);
}

// Function to dynamically add buttons that represent files uploaded by user.
function addEditBtn() {
    var table = document.getElementById("myTable");
    var row = table.insertRow(-1);
    var cellInstruction = row.insertCell(-1);
    var button = document.createElement('button');
    var remove = document.createElement('button');
    button.setAttribute('type', 'button');
    button.innerHTML = customName; // Make the custom name the button name
    button.setAttribute('name', customName);
    button.setAttribute('class', 'btn btn-secondary fileBtn');

    // Add filename: filecontents to dictionary
    fileContentsDict[customName] = fileText;
    console.log(fileContentsDict);

    // Add event listener that changes contents in view
    button.addEventListener('click', (event) => {
        if(event.target.name != "")
            document.getElementById('text-box').innerHTML = fileContentsDict[event.target.name];
    });

    remove.setAttribute('class', 'removeBtn');
    // Add attribute listener to remove button if clicked
    remove.addEventListener('click', function(e) {
        // Clear main text pane when user removes that text file.
        document.getElementById('text-box').innerHTML = " ";
        e.currentTarget.parentNode.remove();
    }, false);
    remove.innerHTML = "X";
    button.prepend(remove);
    cellInstruction.appendChild(button);
}

function submitCustomQuery() {
    let selection = document.getElementById("userCustomQuery").innerHTML
    console.log(selection)
    sendData(queryType, selection)
}

var option1Button = document.getElementById('option1');
var option2Button = document.getElementById('option2');
var option3Button = document.getElementById('option3');
var option4Button = document.getElementById('option4');

// Define event listeners to select query function requested by the user
option1Button.addEventListener('click', () => {
    queryType = "summarize"
    clearText()
}
);
option2Button.addEventListener('click', () => {
    queryType = "elaborate"
    clearText()
}
);
option3Button.addEventListener('click', () => {
    queryType = "define"
    clearText()
}
);
option4Button.addEventListener('click', () => {
    queryType = "custom"
    clearText()
});


function clearText() {
    document.getElementById('resultCustomQuery').innerHTML = " ";
}