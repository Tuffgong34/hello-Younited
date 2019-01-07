$(document).ready(function(){
    $('#logged_in_only').hide();
    window.ret_url = 'admin';
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    if(window.page_type=='leaguedivision'){
        $.ajax({
            type: "GET",
            url: '/api/admin',
            success: function(ret){
            
                console.log(ret);
                if(ret.status == 'ok'){
                    $('#firstname').html("Welcome, " + ret.data.firstname);
                    
                    // var statsstring = ret.data.usercount + " users and " + ret.data.playercount + " players registered";
                    // $('#stats').html(statsstring);
                    // $('#logged_in_only').show();
                    var options = "";
                    for(var i=0; i< ret.data.leagues.length;i++){
                        var l = ret.data.leagues[i];
                        // <option value="volvo">Volvo</option>
                        var next_out = "<option value='" + l.id + "'>" + l.name + "</option>";
                        options += next_out;
                    }
                    $('#division_league').html(options);

                    var league_out = "";
                    for(var i=0; i<ret.data.leagues.length; i++){
                        var league = ret.data.leagues[i];
                        league_out += "<div class='league_sub'><h2>";
                        league_out += "<b>" + league.name + "</b>";
                        // console.log(league.name);
                        if(league.location != undefined && league.location != ""){
                            league_out += " - [" + league.location + "]";
                        }
                        league_out += "</h2>";
                        if(league.description != undefined && league.description!= ""){
                            league_out += "<h3>" + league.description + "<h3>";
                        }
                    
                        for(var j=0; j < league.divisions.length; j++){
                            var division = league.divisions[j];
                            league_out += "<div class='division_sub'><h4><b>" + division.name + "</b> - " + division.description + "</h4></div>";
                        }
                        league_out += "</div>";
                    }
                    $('#league_data').html(league_out);

                
                }else{
                    if(ret.authorized == false){
                        window.location.href='/profile';
                    }
                    
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
    }else if(window.page_type == 'clubplayer'){
        $.ajax({
            type: "GET",
            url: '/api/admin',
            success: function(ret){
                if(ret.status == 'ok'){
                    $('#firstname').html("Welcome, " + ret.data.firstname);
                    console.log(ret);
                    var options = "";
                    for(var i=0; i< ret.data.leagues.length;i++){
                        var l = ret.data.leagues[i];
                        // console.log(l.divisions);
                        for(var j=0; j<l.divisions.length; j++){
                            var d = l.divisions[j];
                            var next_out = "<option value='" + d.id + "'>" + l.name + ": " + d.name + "</option>";
                            options += next_out;
                        }
                    }
                    // console.log(options)
                    $('#club_division').html(options);

                    var club_out = "";
                    for(var i=0; i<ret.data.clubs.length; i++){
                        var club = ret.data.clubs[i];
                        // club_out += "<div class='league_sub'><h2>";
                        club_out += "<b>" + club.name + "</b>";
  
                        if(club.location != undefined && club.location != ""){
                            club_out += " - [" + club.location + "]";
                        }
                        club_out += "<br>";

                        // club_out += "</h2>";
                        // if(club.description != undefined && club.description!= ""){
                        //     club_out += "<h3>" + club.description + "<h3>";
                        // }
                    
                        // for(var j=0; j < club.divisions.length; j++){
                        //     var division = club.divisions[j];
                        //     club_out += "<div class='division_sub'><h4><b>" + division.name + "</b> - " + division.description + "</h4></div>";
                        // }
                        // club_out += "</div>";
                    }
                    $('#club_list').html(club_out);

                    // TODO: Player list
                    var pos_opts = "";
                    for(var i=0; i<ret.data.positions.length; i++){
                        var pos = ret.data.positions[i];
                        var next_pos = "<option value='" + pos.id + "'>" + pos.name + "</option>";
                        pos_opts += next_pos;
                    }
                    $('#player_position').html(pos_opts);

                    var club_options = "";
                    for(var i=0;i<ret.data.clubs.length;i++){
                        var club = ret.data.clubs[i];
                        var next_options = "<option value='" + club.id + "'>" + club.name + "</option>";
                        club_options += next_options;
                    }
                    $('#player_club').html(club_options);
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
    }else if(window.page_type == 'main_admin'){
        $.ajax({
            type: "GET",
            url: '/api/admin',
            success: function(ret){
             
                console.log(ret);
                if(ret.status == 'ok'){
                    $('#firstname').html("Welcome, " + ret.data.firstname);
                    
                    var statsstring = ret.data.usercount + " users and " + ret.data.playercount + " players registered";
                    $('#stats').html(statsstring);
                    $('#logged_in_only').show();
                    var options = "";
                    for(var i=0; i< ret.data.leagues.length;i++){
                        var l = ret.data.leagues[i];
                        // <option value="volvo">Volvo</option>
                        var next_out = "<option value='" + l.id + "'>" + l.name + "</option>";
                        options += next_out;
                    }
                    $('#division_league').html(options);
    
                    var league_out = "";
                    for(var i=0; i<ret.data.leagues.length; i++){
                        var league = ret.data.leagues[i];
                        league_out += "<div class='league_sub'><h2>";
                        league_out += "<b>" + league.name + "</b>";
                        // console.log(league.name);
                        if(league.location != undefined && league.location != ""){
                            league_out += " - [" + league.location + "]";
                        }
                        league_out += "</h2>";
                        if(league.description != undefined && league.description!= ""){
                            league_out += "<h3>" + league.description + "<h3>";
                        }
                    
                        for(var j=0; j < league.divisions.length; j++){
                            var division = league.divisions[j];
                            league_out += "<div class='division_sub'><h4><b>" + division.name + "</b> - " + division.description + "</h4></div>";
                        }
                        league_out += "</div>";
                    }
                    $('#league_data').html(league_out);
    
                   
                }else{
                    if(ret.authorized == false){
                        window.location.href='/profile';
                    }
                    
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
    }

    // Finally setup the menu
    get_menu_items();
});

function submit_league(){
    $('#error').html("");
    var name = $('#league_name').val();
    var description = $('#league_description').val();
    var location = $('#league_location').val();
    var founded = $('#league_founded').val();

    if( name == undefined || name == ""){
        $('#error').html("Name cannot be blank");
        return;
    }
    var data = {
        name: name,
        description: description,
        location: location,
        founded: founded
    }
    // console.log(data)

    $.ajax({
        type: "POST",
        url: '/api/league',
        data: data,
        success: function(ret){
         
            console.log(ret);
            if(ret.status != 'ok'){
                $('#error').html(ret.message);
                return;
            }
            $('#league_name').val('');
            $('#league_description').val('');
            $('#league_location').val('');
            $('#league_founded').val('');
        }, 
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        error: function(){
            
            console.log("error occurred");
        },
        dataType: 'json'
    })
}

function submit_division(){
    $('#error').html("");
    var name = $('#division_name').val();
    var description = $('#division_description').val();
    var location = $('#division_location').val();
    var founded = $('#division_founded').val();
    var league = $('#division_league').val();

    if( name == undefined || name == ""){
        $('#error').html("Name cannot be blank");
        return;
    }

    var data = {
        name: name,
        description: description,
        location: location,
        league: league,
        founded: founded
    }
 
    $.ajax({
        type: "POST",
        url: '/api/division',
        data: data,
        success: function(ret){
         
            if(ret.status != 'ok'){
                $('#error').html(ret.message);
                return;
            }
            $('#division_name').val('');
            $('#division_description').val('');
            $('#division_location').val('');
            $('#division_founded').val('');
        }, 
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        error: function(){
            
            console.log("error occurred");
        },
        dataType: 'json'
    });
}

function submit_club(){
    $('#error').html("");
    var name = $('#club_name').val();
    var information = $('#club_information').val();
    var contact = $('#club_contact').val();
    var location = $('#club_location').val();
    var founded = $('#club_founded').val();
    var division = $('#club_division').val();

    if( name == undefined || name == ""){
        $('#error').html("Name cannot be blank");
        return;
    }

    var data = {
        name: name,
        information: information,
        contact: contact,
        location: location,
        division: division,
        founded: founded
    }
 
    $.ajax({
        type: "POST",
        url: '/api/club',
        data: data,
        success: function(ret){
         
            if(ret.status != 'ok'){
                $('#error').html(ret.message);
                return;
            }
            $('#club_name').val('');
            $('#club_information').val('');
            $('#club_contact').val('');
            $('#club_location').val('');
            $('#club_founded').val('');
        }, 
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        error: function(){
            
            console.log("error occurred");
        },
        dataType: 'json'
    });
}

function submit_player(){
    $('#error').html("");
    // Height (cm): <input id="player_height_cm" type='number'>
    // Club: <select name="player_club" id='player_club'></select><br>
    // Position: <select name="player_position" id='player_position'></select><br>
    // Shirt Color: <input name='player_color' type='color'><br>
    // User ID: <input name='player_user_id' type='number'><br>

    var last_name = $('#player_last_name').val();
    var first_name = $('#player_first_name').val();
    var shirt_number = $('#player_shirt_number').val();
    if(shirt_number != undefined && shirt_number!= ""){
        shirt_number = parseInt(shirt_number);
    }
    var date_of_birth = $('#player_date_of_birth').val();
    var height_cm = $('#player_height_cm').val();
    if(height_cm != undefined && height_cm!= ""){
        height_cm = parseInt(height_cm);
    }

    var club = $('#player_club').val();
    if(club != undefined && club!= ""){
        club = parseInt(club);
    }
    // var shirt_color = $('#player_color').val();
    var user_id = $('#player_user_id').val();
    if(user_id != undefined && user_id!= ""){
        user_id = parseInt(user_id);
    }
    var position_id = $('#player_position').val();
    if(position_id != undefined && position_id!= ""){
        position_id = parseInt(position_id);
    }
    if( last_name == undefined || last_name == ""){
        $('#error').html("Lastname cannot be blank");
        return;
    }
    if( club == undefined || club == "" || club == 0){
        $('#error').html("Club cannot be blank");
        return;
    }

    var data = {
        last_name: last_name,
        first_name: first_name,
        shirt_number: shirt_number,
        date_of_birth: date_of_birth,
        height_cm: height_cm,
        club: club,
        shirt_color: shirt_color,
        user_id: user_id,
        position_id: position_id
    }
    // console.log(data);
    $.ajax({
        type: "POST",
        url: '/api/player',
        data: data,
        success: function(ret){
            console.log(ret);
            if(ret.status != 'ok'){
                $('#error').html(ret.message);
                return;
            }
            $('#player_last_name').val('');
            $('#player_first_name').val('');
            $('#player_shirt_number').val('');
            $('#player_date_of_birth').val('');
            $('#player_height_cm').val('');
            $('#player_club').val('');
            $('#player_color').val('');
            $('#player_user_id').val('');
        }, 
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Token " + window.token);
        },
        error: function(){
            
            console.log("error occurred");
        },
        dataType: 'json'
    });
}

function add_a_league(){
    window.location.href='/admin/league';
}

function add_a_club(){
    window.location.href='/admin/club';
}