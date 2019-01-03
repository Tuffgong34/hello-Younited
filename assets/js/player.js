$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    
    get_menu_items();

    if(window.player_id != null && window.player_id != ""){
        var url = '/api/player/' + window.player_id;
    
        $.ajax({
            type: "GET",
            url: url ,
            success: function(ret){
                console.log(ret); 
                if(ret.status == 'ok'){
                    var player = ret.data.player;
                    $('#player_name').html(player.first_name + " " + player.last_name);
                    $('#player_height').html("Height: " + player.height + "cm");
                    $('#player_shirt_number').html("Shirt Number: "  + player.shirt_number);
                    if(player.club.id != null){
                        var output = "<div class='player_club_badge' onclick='load_club(" + player.club.id +")'>";
                        output += player.club.name;
                        output += "</div>";

                        $('#player_club').html(output);
                    }
                    $('#player_shirt_color').html(player.shirt_color);
                    $('#player_position').html("Position: " + player.position);
                    // TODO: Allow users to claim the player if they can
     
                }else{
                    $('#error').html(ret.message);
                }
                              
            }, 
            beforeSend: function (xhr) {
                xhr.setRequestHeader ("Authorization", "Token " + window.token);
            },
            error: function(){
                console.log("error occurred");
            },
            dataType: 'json'
        })    
    }else{
        $('error').html("No Division Id Passed In");
    }
});

function load_club(club_id){
    window.location.href='/club/' + club_id;
}