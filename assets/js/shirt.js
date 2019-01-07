$(document).ready(function(){
    $('#logged_in_only').hide();
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    get_menu_items();

    $.ajax({
        type: 'GET',
        url: '/api/shirt',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        success: function(ret){
            console.log(ret);
            if(ret.status == 'ok'){
                // Loop through and draw shirt
                var output = "";
                for(var i=0; i<ret.data.shirts.length; i++){
                    var shirt = ret.data.shirts[i];

                    var next_span = get_shirt_span(shirt, shirt.id);
  
                    output += next_span;
                }  
                // console.log(output);
                $('#shirt_out').html(output);  
            }
        },
        error: function(ret){
            console.log('Error');
        } 
    });
});

function save_shirt(){
    var primary = $('#primary').val();
    var secondary = $('#secondary').val();
    var style = $('#style').val();

    var data = {
        'primary_color': primary,
        'secondary_color': secondary,
        'style': style
    }
    $.ajax({
        type: 'POST',
        url: '/api/shirt',
        data: data,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        success: function(ret){
            console.log(ret);
            if(ret.status == 'ok'){
                window.location.href='/admin'
            }
        },
        error: function(ret){
            console.log('Error');
        }
        
    })
}

function update_shirt(){

}

