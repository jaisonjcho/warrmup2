$(document).ready(function() {
                  show_login_page("Please sign in or create a new user")
                  //});

function show_login_page(message) {
    if(! message) message = "Please sign in or create a new user";
    $('#welcome-page').hide()
    $('#login-username').val("")
    $('#login-password').val("")
    $('#login-message').html(message)
    $('#login-page').show()
}

function show_welcome_page(user, count) {
    $('#login-page').hide();
    $('#welcome-page').show();
    $('#welcome-message').html("Welcome "+user+"<br>You have logged in "+count+" times.");
}

function handle_login_response(data, user) {
    if( data.errCode > 0 ) {
        c = data.count;
        show_welcome_page(user, c);
    } else {
        if( debug_flag ) {
            if( data.errCode != ERR_BAD_CREDENTIALS ) {
                alert( 'Illegal error code encounted for this state');
            }
        }
        show_login_page( get_message_for_errcode(data.errCode) );
    }
}

function handle_add_user_response(data, user) {
    if( data.errCode > 0 ) {
        c = data.count;
        show_welcome_page(user, c);
    } else {
        if( debug_flag ) {
            if( data.errCode != ERR_BAD_USERNAME && data.errCode != ERR_USER_EXISTS ) {
                alert( 'Illegal error code encounted for this state');
            }
        }
        show_login_page( get_message_for_errcode(data.errCode) );
    }
}

$('#login-username').blur(function(){
                          username = $('#login-username').val()
                          if (username == ""){
                            $('#login-message').html("The username cannot be empty")
                          }
                          else if (username.length > 128){
                            $('#login-message').html("The username cannot be over 128 characters")
                          }
                          else{
                            $('#login-message').html("Please sign in or create a new user")
                          }
                                            
                          });
                  
$('#login-password').blur(function(){
                          password = $('#login-password').val()
                          if (password.length > 128){
                            $('#login-message').html("The password cannot be ver 128 characters")
                          }
                                            
                          });
                  
// POST to /users/login -- log in user and increase count
$('#login-button').click(function() {
    //e.preventDefault()
    username = $('#login-username').val()
    password = $('#login-password').val()
    json_request("/users/login", { user: username, password: password }, function(data) { return handle_login_response(data, username); }, function(err) { alert('error occurred on request'); });
                         
    return false;
});

// POST to /users/add -- create new user
$('#add-user-button').click(function() {
                            username = $('#login-username').val()
                            password = $('#login-password').val()
                            json_request("/users/add", { user: username, password: password }, function(data) { return handle_add_user_response(data, username); }, function(err) {alert('error occurred on request'); });
                            
                            return false;
                            });

$('#logout-button').click(function() {
                          show_login_page();
                          
                          return false;
                          });

/* do POST requests and handle responses */
function json_request(page, dict, success, failure) {
    $.ajax({
           type: 'POST',
           url: page,
           data: JSON.stringify(dict),
           contentType: "application/json",
           dataType: "json",
           success: success,
           error: failure
           });
}

debug_flag = false;

ERR_BAD_CREDENTIALS = (-1);
ERR_USER_EXISTS = (-2);
ERR_BAD_USERNAME = (-3);
ERR_BAD_PASSWORD  = (-4);


function get_message_for_errcode(code) {
    if( code == ERR_BAD_CREDENTIALS) {
        return ("Invalid username and/or password. Please try again.");
    } else if( code == ERR_BAD_USERNAME) {
        return ("The username cannot be empty or over 128 characters. Please try again.");
    } else if( code == ERR_USER_EXISTS) {
        return ("This user name already exists. Please try again.");
    } else if( code == ERR_BAD_PASSWORD) {
        return ("The password should be at most 128 characters long. Please try again");
    } else {
        if( debug_flag ) { 
            alert('Illegal error code encountered: ' + code); 
        }
        return ("Unknown error occured: " + code);
    }
}

});