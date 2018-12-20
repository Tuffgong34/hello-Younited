$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;

    // console.log("we have a token " + token)
    $('#status').html("logged in");
    // Use token to grab details
    $.ajax({
        type: "GET",
        url: '/api/profile',
        success: function(ret){
            awaiting_confirmation = false;
            console.log(ret);
            if(ret.status == 'ok'){
                $('#firstname').html(ret.data.firstname);
                $('#lastname').html(ret.data.lastname);
            }else{
                $('#error').html(ret.message);
            }
        }, 
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        error: function(){
            awaiting_confirmation = false;
            console.log("error occurred");
        },
        dataType: 'json'
    })
})