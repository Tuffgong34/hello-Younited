var awaiting_confirmation = false;

function register_user(){
    if(awaiting_confirmation){
        console.log("Still waiting for return from server");
        return;
    }

    $('#error').html("");

    var email = $('#email').val();
    var firstname = $('#firstname').val();
    var lastname = $('#lastname').val();
    var phone = $('#phone').val();
    var password = $('#password').val();
    var confirm = $('#confirm').val();

    if( (email == undefined || email == "") 
      && (phone == undefined || phone == "") ){
          var err = "Please provide either phone number or email";
          $('#error').html(err);
          return;
    }
    if( (password == undefined || password == "") ){
        var err = "Password cannot be blank";
        $('#error').html(err);
        return;
    }
    
    if( (password.length < 8) ){
        var err = "Password cannot be less than 8 characters";
        $('#error').html(err);
        return;
    }
    // TODO: Check more details about the password
    if( (confirm != password) ){
        var err = "Passwords do not match";
        $('#error').html(err);
        return;
    }
    awaiting_confirmation = true;
    var data = {
        email: email,
        password: password,
        phone: phone,
        firstname: firstname,
        lastname: lastname
    }

    $.ajax({
        type: "POST",
        data: data,
        url: '/api/createuser',
        success: function(ret){
            awaiting_confirmation = false;
            console.log(ret);
            if(ret.status == 'ok'){
                $('#redirect_login').show();
                $('#register_user_button').hide();
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
$(document).ready(function(){
    $('#redirect_login').hide();
    $('#register_user_button').show();

});

function go_to_login(){
    window.location.href='/login';
}