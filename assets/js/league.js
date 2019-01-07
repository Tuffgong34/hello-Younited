$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    get_menu_items();

    if(window.league_id != null && window.league_id != ""){
        var url = '/api/league/' + window.league_id;
        console.log(url);
        $.ajax({
            type: "GET",
            url: url ,
            success: function(ret){
                console.log(ret); 
                if(ret.status == 'ok'){
                    $('#league_name').html(ret.data.league.name);
                    $('#league_description').html(ret.data.league.description);
                    
                    var output = "";
                    for(var i=0; i<ret.data.divisions.length; i++){
                        var d = ret.data.divisions[i];
                        var next_item = "<div class='league_sub' onclick='load_division(" + d.id + ")'>";
                        next_item += "<h2>" + d.name;
                        if(d.location != null){
                            next_item +=  " [ " + d.location + "]";
                        }
                        next_item += "</h2>";
                        if(d.description != null){
                            next_item += "<h3>" + d.description + "</h3>";
                        }
                        next_item += "</div>";
                        output += next_item;
                    }
                    $('#league_output').html(output);

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
        $.ajax({
            type: "GET",
            url: '/api/leagues',
            success: function(ret){
                console.log(ret)
                $('#league_name').html("Leagues");
                if(ret.status == 'ok'){
                    var output = "";
                    for(var i=0; i<ret.data.leagues.length; i++){
                        var l = ret.data.leagues[i];
                        console.log(l.name);
                        var next_item = "<div class='league_sub' onclick='load_league(" + l.id + ")'>";
                        next_item += "<h2>";
                        
                        next_item += l.name;
                        if(l.location != null){
                            next_item +=  " [ " + l.location + "]";
                        }
                        next_item += "</h2>";
                        if(l.description != null){
                            next_item += "<h3>" + l.description + "</h3>";
                        }
                        next_item += "</div>";
                        output += next_item;
                    }
                    $('#league_output').html(output);
                }else{
                    $('#error').html(ret.message);
                }

                // console.log(ret);
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
    }
    
});

function link_page(link){
    window.location.href = link;
}

function load_league(league_id){
    window.location.href='/league/' + league_id;
}
function load_division(div_id){
    window.location.href='/division/' + div_id;
}