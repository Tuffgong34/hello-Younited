function check_login_status(){
    var token = readCookie('yn_token');
    if(token == undefined || token == ""){
        if(window.ret_url == undefined || window.ret_url == ""){
            var ret_url = window.location.pathname;
            window.location.href='/login?r=' + ret_url;
        }else{
            window.location.href='/login?r=' + window.ret_url;
        }
        return "";
    }
    return token;
}

function logout(){
    eraseCookie('yn_token');
    window.location.href='/login' 
}