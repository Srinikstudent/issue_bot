var form = document.getElementById('myForm');
form.onsubmit = function(event){
        var xhr = new XMLHttpRequest();
        var formData = new FormData(form);
        //open the request
        xhr.open('POST','https://gt-srini-bot.herokuapp.com/api/label')
        xhr.setRequestHeader("Content-Type", "application/json");

        //send the form data
        xhr.send(JSON.stringify(Object.fromEntries(formData)));

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                form.reset(); //reset form after AJAX success or do something else
            }
        }
        //Fail the onsubmit to avoid page refresh.
        return false; 
    }
