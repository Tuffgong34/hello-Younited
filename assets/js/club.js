$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    
    get_menu_items();
    if(window.club_id != null && window.club_id != ""){
        var url = '/api/club/' + window.club_id;
    
        $.ajax({
            type: "GET",
            url: url ,
            success: function(ret){
                console.log(ret); 
                if(ret.status == 'ok'){
                    $('#club_name').html(ret.data.club.name);
                    $('#club_information').html(ret.data.club.information);
                    $('#club_contact').html("Contact: " + ret.data.club.contact);
                    
                    var output = "";
                    for(var i=0; i<ret.data.players.length; i++){
                        var p = ret.data.players[i];
                        var next_item = "<div class='player_sub' onclick='load_player(" + p.id + ")'>";
                        next_item += "<h2>" + p.first_name + " " + p.last_name;
                        next_item += "</h2>";
                        if(p.position != undefined && p.position != null && p.position.name != undefined && p.position.name != "" && p.position.name != null){
                            next_item += "Position: " + p.position.name;
                        }
                        next_item += "</div>";
                        output += next_item;
                    }
                    $('#player_output').html(output);

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

function link_page(link){
    window.location.href = link;
}

function load_player(player_id){
    window.location.href='/player/' + player_id;
}