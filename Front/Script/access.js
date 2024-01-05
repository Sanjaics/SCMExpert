$( document ).ready(function() {
    if(localStorage.getItem("role") == "admin")
        {
            $("#access_role").hide();
            $("#access_rolefeedback").hide();
        }
        else if(localStorage.getItem("role") == "user")
        {

            $("#access_ui_role, #access_role_nav").hide();
            $("#Displayfeedback").hide();
        }
});