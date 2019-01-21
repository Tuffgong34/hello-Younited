$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    
    get_menu_items();

    if(window.yn_match_id == null || window.yn_match_id==undefined){
        $("#error").html("Something went wrong loading the match");
        return;
    }
    var url = '/api/match/' + window.yn_match_id;

    $.ajax({
        type: "GET",
        url: url ,
        success: function(ret){
            
            if(ret.status == 'ok'){
                var output = "";
                output += "<div class='match_overview'>"
                output += "<div class='match_club_div'>";
                output += ret.data.home_club.goals.length + " <br> ";
                output += ret.data.home_club.name;
                output += "</div>";
                output += " VS ";
                output += "<div class='match_club_div'>";
                output += ret.data.away_club.goals.length + " <br> ";
                output += ret.data.away_club.name;
                output += "</div>";
                output += "</div>";
                output += "<h2>Events</h2>"
 
                // TODO: Make all events in this list - then add 
                var all_events = ret.data.home_club.goals;
                all_events.push.apply(all_events, ret.data.away_club.goals);
                all_events.push.apply(all_events, ret.data.events);
 
                all_events.sort(function(a,b){
                    if(a.time > b.time){ return 1}
                    if(a.time < b.time){ return -1}
                    return 0;
                });
                
                for(var i=0; i<all_events.length;i++){
                    var event = all_events[i];
                    console.log(event)
                    if(event.type=='Goal'){
                        output += "<div class='goal_div' onclick='load_player(" + event.scorer_id + ")'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px;'>";
                        output += "<img src='/img/goal_icon.png' style='width: 50px'>";
                        output += "</div>";
                        output += event.scorer + " - " + event.time;
                        output += "</div>";
                    }else if(event.type=='Kick-off' || event.type=='Full-time'){
                        output += "<div class='goal_div'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px;'>";
                        output += "<img src='/img/kick_off.png' style='width: 50px'>";
                        output += "</div>";
                        output +=  event.type + " @ " + event.time;
                        output += "</div>";
                    }else if(event.type=='Yellow Card'){
                        output += "<div class='goal_div' onclick='load_player(" + event.player.id + ")'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px; width:50px; text-align: center;'>";
                        output += "<img src='/img/yellow_card.png' style='max-width: 50px; max-height: 50px;'>";
                        output += "</div>";
                        output +=  event.player.name + " @ " + event.time; 
                        output += "</div>";
                    }else if(event.type=='Red Card'){
                        output += "<div class='goal_div' onclick='load_player(" + event.player.id + ")'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px; width:50px;'>";
                        output += "<img src='/img/red_card.jpg' style='width: 50px'>";
                        output += "</div>";
                        output +=  event.player.name + " @ " + event.time; 
                        output += "</div>";
                    }else if(event.type=='Foul'){
                        output += "<div class='goal_div' onclick='load_player(" + event.player.id + ")'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px; width:50px;'>";
                        output += "<img src='/img/foul.png' style='width: 50px'>";
                        output += "</div>";
                        output +=  event.player.name + " @ " + event.time; 
                        output += "</div>";
                    }else if(event.type=='Penalty'){
                        output += "<div class='goal_div' onclick='load_player(" + event.player.id + ")'>";
                        output += "<div style='display:inline-block;background-color:white; margin-right:10px; width:50px;'>";
                        output += "<img src='/img/penalty.jpg' style='width: 50px'>";
                        output += "</div>";
                        output +=  event.player.name + " @ " + event.time; 
                        output += "</div>";
                    }
                    // TODO: Add in remaining event types
                    // # Event_Types
                    // #  id |    name     | added
                    // # ----+-------------+-------------
                    // #   1 | Goal        | x
                    // #   2 | Yellow Card | x
                    // #   3 | Red Card    | x
                    // #   4 | Kick-off    | x
                    // #   5 | Corner      |
                    // #   6 | Throw-In    |
                    // #   7 | Penalty     | x
                    // #   8 | Foul        | x
                    // #   9 | Full-time   | x
                  
                }
                if(all_events.length < 1){
                    output += "None";
                }

                $('#match_output').html(output);

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

function load_player(player_id){
    window.location.href='/player/' + player_id;
}