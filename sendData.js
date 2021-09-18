var sendData = function(string) {
        var data = new FormData();
        data.append('text', string);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/summarization', true);
        xhr.onload = function () {
            console.log(this.responseText);
        };
        xhr.send(data);
}
