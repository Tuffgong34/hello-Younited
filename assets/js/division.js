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
                    
                    var output = "";
                    for(var i=0; i<ret.data.clubs.length; i++){
                        var c = ret.data.clubs[i];
                        var next_item = "<div class='club_sub' onclick='load_club(" + c.id + ")'>";
                        next_item += "<h2>";
                        if(c.home_shirt != undefined && c.home_shirt!=null){
                            next_item += get_shirt_span(c.home_shirt)
                        }

                        next_item += c.name;
                        if(c.location != null){
                            next_item +=  " [ " + c.location + "]";
                        }
                        next_item += "</h2>";
                        // if(d.description != null){
                        //     next_item += "<h3>" + d.description + "</h3>";
                        // }
                        next_item += "</div>";
                        output += next_item;
                    }
                    $('#club_output').html(output);

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