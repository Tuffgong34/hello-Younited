function check_login_status(){
    var token = readCookie('yn_token');
    if(token == undefined || token == ""){
        window.location.href='/login?r=' + window.ret_url;
        return "";
    }
    return token;
}

function logout(){
    eraseCookie('yn_token');
    window.location.href='/login' 
}