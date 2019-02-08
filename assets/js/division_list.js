var offset = 0;
var total_results = 0;
var RESULTS_PER_PAGE = 10;
var prompt = "";

function update_division_list(){
   var data = {
       prompt: prompt,
       offset: offset * RESULTS_PER_PAGE
   }
   $.ajax({
    type: "POST",
    url: '/api/divisions',
    data: data,
    success: function(ret){

        if(ret.status == 'ok'){
            var output = "";
            total_results = ret.data.division_count;
            $('#division_count').html(total_results);

            for(var i=0; i<ret.data.divisions.length; i++){
                if(i > RESULTS_PER_PAGE){
                    break;
                }
                var d = ret.data.divisions[i];
                var next_item = "<div class='league_sub' onclick='load_division(" + d.id + ")'>";
                next_item += "<h2>";
                
                next_item += d.name;
                next_item += "</h2>";
                next_item += "</div>";
                output += next_item;
            }
            var page_num = offset + 1;
            var total_pages = parseInt(total_results/RESULTS_PER_PAGE);
            $('#page_update').html(page_num + " of " + total_pages);

            $('#division_list_output').html(output);
        }else{
            $('#error').html(ret.message);
        }

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

$(document).ready(function(){
    var token = check_login_status();
    if(token == ""){
        // The login_handler should redirect so just wait
        return;
    }
    window.token = token;
    get_menu_items();

    update_division_list();

    $('#search_criteria').on('input', function(){
        console.log("Changing");
        prompt = $('#search_criteria').val();
        update_division_list();
    })
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

function next_tab(){
    offset += 1;
    var num_pages = parseInt(total_results/RESULTS_PER_PAGE) + 1;

    if(offset > num_pages){
        offset = num_pages;
    }
    update_division_list();
}
function prev_tab(){
    offset -= 1;
    if(offset < 0){
        offset = 0;
    }
    update_division_list();
}