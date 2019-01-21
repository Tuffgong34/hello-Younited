$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    
    get_menu_items();

   
    var url = '/api/matches';

    $.ajax({
        type: "GET",
        url: url ,
        success: function(ret){
            // console.log(ret); 
            
            if(ret.status == 'ok'){
                var output = "";
                for(var i=0; i<ret.data.matches.length && i < 20;i++){
                    var match = ret.data.matches[i];
                    // console.log(match);
                    output += "<div class='match_section' onclick='load_match(" + match.id + ")'>";
                    output += "Home: " + match.home_club + " vs Away: " + match.away_club + " - played at: " + match.played_at;
                    output += "</div>"; 
                }
                $('#match_output').html(output);

                // $('#division_name').html(ret.data.division.name);
                // $('#division_description').html(ret.data.division.description);
                
                // update_division_list(ret.data);
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
    });    
})

function load_match(matchid){
    window.location.href='/match/' + matchid;
}