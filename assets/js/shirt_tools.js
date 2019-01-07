function get_shirt_span(shirt, num){
    var output = "";
    if(num == undefined || num == null || num < 0){
        num = " ";   
    }

    if(shirt.style == "solid"){
        output += "<span class='shirt_desc' style='background-color:" + shirt.primary_color + "'>";
        output += num +"</span>";
    }else if(shirt.style == "solid_arms"){
        output += "<span class='shirt_desc' style='background: repeating-linear-gradient(90deg,";
        output +=  shirt.secondary_color + " 0%,";
        output +=  shirt.secondary_color + " 16%," + shirt.primary_color + " 16%, ";
        output +=  shirt.primary_color + " 88%," + shirt.secondary_color + " 88%, ";
        output +=  shirt.secondary_color + " 100%)'>";
        output +=  num + "</span>";

    }else if(shirt.style == "stripes"){
        output += "<span class='shirt_desc' style='background: repeating-linear-gradient(90deg,";
        output +=  shirt.secondary_color + " 0%," + shirt.primary_color + " 0%, ";
        output +=  shirt.primary_color + " 16%," + shirt.secondary_color + " 16%, ";
        output +=  shirt.secondary_color + " 32%," + shirt.primary_color + " 32%, ";
        output +=  shirt.primary_color + " 64%," + shirt.secondary_color + " 64%, ";
        output +=  shirt.secondary_color + " 88%," + shirt.primary_color + " 88%, ";
        output +=  shirt.primary_color + " 100%)'>";
        output +=  num + "</span>";

    }else if(shirt.style == "hoops"){
        output += "<span class='shirt_desc' style='background: repeating-linear-gradient(0deg,";
        output +=  shirt.primary_color + " 0%, ";
        output +=  shirt.primary_color + " 20%," + shirt.secondary_color + " 20%, ";
        output +=  shirt.secondary_color + " 60%," + shirt.primary_color + " 60%, ";
        output +=  shirt.primary_color + " 100%)'>";
        output +=  num + "</span>";
    }
    return output;
}