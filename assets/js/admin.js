$(document).ready(function(){
    $('#logged_in_only').hide();
    window.ret_url = 'admin';
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;

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
                if(ret.data.authorized == false){
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
    console.log(data)

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
    })
}

function add_a_league(){
    console.log("moving to league page")
    window.location.href='/admin/league';
}