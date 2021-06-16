function leaveRoom(room){
    const csrftoken = (document.cookie).toString().split("=")[1];
    $.ajax({
        url: '/leave_room/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            'room_name': room,
        }),
        success: function(data){
            window.location.href = '/'
        },
        error: function(data){
            console.log(data)
        }
    })
}

function createRoom(){
    var room_name = $('#room-name-input').val();
    var is_public = $('#is_public').is(':checked');
    var is_private = $('#is_private').is(':checked');
    const csrftoken = (document.cookie).toString().split("=")[1];
    $.ajax({
        url: '/create_chat_room/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            'room_name': room_name,
            'is_private': is_private,
            'is_public': is_public

        }),
        success: function(data){
            if (data['status']==true){
            window.location.href = '/chat/' + room_name
            }
            else if (data['status']==false){
                $('#message').removeClass('d-none');
                $('#message').html("<h5>Room with name "+ room_name +" already exists.!</h5>")
                $('#message').finish().show().delay(5000).fadeOut('slow');
                $('#ModalCenter').modal('hide');
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function joinRoom(){
    var room_name = $('#room-name-input').val();
    const csrftoken = (document.cookie).toString().split("=")[1];
    $.ajax({
        url: '/join_chat_room/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            'room_name': room_name,
        }),
        success: function(data){
            console.log(data)
           if(data['status']==true){
               if(data['public_room']==true){
                   window.location.href = '/chat/' + room_name
               }
               else if(data['private_room']==true){
                   window.location.reload();
                
               }
           }
           else if (data['status'] == false){
            window.location.reload();
           }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function changeRoomType(){
    var room_name = $('#room-name').text();
    const csrftoken = (document.cookie).toString().split("=")[1];
    var is_private = $("#room-type-private").is(':checked');
    var is_public = $("#room-type-public").is(':checked');
    $.ajax({
        url: '/change_room_type/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            'room_name': room_name,
            'is_public': is_public,
            'is_private': is_private,
        }),
        success: function(data){
            if(data['status'] == true ){
                window.location.reload();
            }
            else if(data['status'] == false){
                console.log(data)
                $('#Modal').modal('hide');
                $('#message').removeClass('d-none');
                $('#message').html("<h5>"+ data['error'] +".!</h5>")
                $('#message').finish().show().delay(5000).fadeOut('slow');
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function removeUserFromChatRoom(user){
    var room_name = $('#room-name').text();
    const csrftoken = (document.cookie).toString().split("=")[1];
    $.ajax({
        url: "/remove_from_chat/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            "room_name": room_name,
            "user": user
        }),
        success: function(data){
            if (data['status'] == true){
                $('#'+user).delay(200).fadeOut('fast', function(){
                    $(this).remove();
                 });
            }
            else if (data['status'] == false){
                window.location.reload();
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function acceptPendingRequests(user){
    const csrftoken = (document.cookie).toString().split("=")[1];
    var room_name = $('#room-name').text();
    var accept_all = false
    if (typeof user ==="undefined"){
        accept_all = true
    }
    $.ajax({
        url: "/accept_pending_request/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            "user": user,
            "room_name": room_name,
            "accept_all": accept_all,
        }),
        success: function(data){
            if(data['status']==true){
                if (accept_all == true){
                    window.location.reload()
                }
                else {
                    $('#'+user+"_pending").delay(200).fadeOut('fast', function(){
                        $(this).remove();
                     });    
                }
            }
            else if(data['status']==false){
                window.location.reload();
            }
        }

    })
}


function rejectIncomingRequests(user){
    const csrftoken = (document.cookie).toString().split("=")[1];
    var room_name = $('#room-name').text();
    $.ajax({
        url: "/reject_incoming_request/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            "user": user,
            "room_name": room_name,
        }),
        success: function(data){
            if (data['status'] == true){
                $('#'+user+"_pending").delay(200).fadeOut('fast', function(){
                    $(this).remove();
                 });  
            } 
            else if(data['status'] == false){
                window.location.reload();
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function addUser(){
    const csrftoken = (document.cookie).toString().split("=")[1];
    var room_name = $('#room-name').text();
    var username = $('#username').val();
    $.ajax({
        url: "/add_user/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            "room_name": room_name,
            "username": username
        }),
        success: function(data){
            if (data['status'] == true){
                $('#message').removeClass('d-none');
                $('#message').html("<h5>User "+ username +" added.!</h5>")
                $('#message').finish().show().delay(5000).fadeOut('slow');
            } 
            else if(data['status'] == false){
                window.location.reload();
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}
