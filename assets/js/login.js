var awaiting_confirmation = false;
const urlParams = new URLSearchParams(window.location.search);


function perform_login(){
    $('#error').html("");
    if(awaiting_confirmation){
        $('#error').html("Already logging in, please wait and try again");
        return;
    }
    awaiting_confirmation = true;

    var username = $('#username').val();
    var password = $('#password').val();
    if(username == undefined || username == ""){
        $('#error').html("Email or Phone Number cannot be blank");
        awaiting_confirmation = false;
        return;
    }
    if(password == undefined || password == ""){
        $('#error').html("Password cannot be blank");
        awaiting_confirmation = false;
        return;
    }
    console.log("About to login")
    // Do login and store token
    $.ajax({
        type: "POST",
        data: {
            username: username,
            password: password
        },
        url: '/api/login',
        success: function(ret){
            awaiting_confirmation = false;
          
            if(ret.status == 'ok'){
                createCookie('yn_token', ret.token, 365);
                // Store the token locally ret.token
                const redirect_page = urlParams.get('r');
                if(redirect_page != undefined && redirect_page != ""){
                    window.location.href='/' + redirect_page;
                }else{
                    window.location.href='/profile';
                }
            }else{
                $('#error').html(ret.message);
            }
        },
        error: function(){
            awaiting_confirmation = false;
            console.log("error occurred");
        },
        dataType: 'json'
    })
}   

