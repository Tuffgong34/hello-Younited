var club_data = null;
function update_division_list(data){
    club_data = data.clubs;
    club_data.sort(function(a,b){
        // Sort the clubs in order based on score
        if(a.rc.points < b.rc.points){ return 1}
        if(a.rc.points > b.rc.points){ return -1}
        // TODO: Add in other sort orders like goal difference   
        return 0;
    });

    var output = "<div class='row club_sub align-items-center'>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>Pos</b></span>";
    output += "    <span class='col-lg-2 col-md-2 col-sm-2 club_header_span'><b>Kit</b></span>";
    output += "    <span class='col-lg-2 col-md-2 col-sm-2 club_header_span'><b>Name</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>Win</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>Draw</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>Loss</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>GF</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>GA</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>GD</b></span>";
    output += "    <span class='col-lg-1 col-md-1 col-sm-1 club_header_span'><b>Points</b></span>";
    output +=  "</div>";
    for(var i=0; i<club_data.length; i++){
        var c = club_data[i];
        var next_item = "<div class='row club_sub  align-items-center' onclick='load_club(" + c.id + ")'>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + (i+1) + "</div>";
        next_item += "<div class='col-lg-2 col-md-2 col-sm-2'>";
        if(c.home_shirt != undefined && c.home_shirt!=null){
            next_item += get_shirt_span(c.home_shirt)
        }
        if(c.away_shirt != undefined && c.away_shirt!=null){
            next_item += get_shirt_span(c.away_shirt)
        }
        if(c.goalkeeper_shirt != undefined && c.goalkeeper_shirt!=null){
            next_item += get_shirt_span(c.goalkeeper_shirt)
        }
        next_item += "</div>";
        next_item += "<div class='col-lg-2 col-md-2 col-sm-2'>";
        next_item += c.name + "<br>";
        if(c.location != null){
            next_item +=  " [" + c.location + "]";
        }
        next_item += "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.win + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.draw + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.loss + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.goals_for + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.goals_against + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.goal_difference + "</div>";
        next_item += "<div class='col-lg-1 col-md-1 col-sm-1 club_header_span'>" + c.rc.points + "</div>";
        next_item += "</div>";
        output += next_item;
    }
    $('#club_output').html(output);

}

$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    
    get_menu_items();

    if(window.division_id != null && window.division_id != ""){
        var url = '/api/division/' + window.division_id;
    
        $.ajax({
            type: "GET",
            url: url ,
            success: function(ret){
                console.log(ret); 
                if(ret.status == 'ok'){
                    $('#division_name').html(ret.data.division.name);
                    $('#division_description').html(ret.data.division.description);
                    
                    update_division_list(ret.data);
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
})

function link_page(link){
    window.location.href = link;
}
function load_club(club_id){
    window.location.href='/club/' + club_id;
}