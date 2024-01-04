$( document ).ready(function() {
    if(sessionStorage.getItem("role") == "admin")
        {
            $("#access_role").hide();
            $("#access_rolefeedback").hide();
        }
        else if(sessionStorage.getItem("role") == "user")
        {

            $("#access_ui_role, #access_role_nav").hide();
            $("#Displayfeedback").hide();
        }
});