function leaveRoom(room){
    const csrftoken = (document.cookie).toString().split("=")[1];
    $.ajax({
        url: '/leave_room/',
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            'room': room,
        }),
        success: function(data){
            window.location.href = 'http://127.0.0.1:8000/'
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
                $('#message').append("<h5>Room with name "+ room_name +" already exists.!</h5>")
                $('#message').delay(5000).fadeOut('slow');
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
           if(data['status']==true){
               if(data['public_room']==true){
                   window.location.href = '/chat/' + room_name
               }
               else if(data['private_room']==true){
                $('#message').removeClass('d-none');
                $('#message').append("<h5>Your request to join room "+ room_name +" is on hold.!</h5>")
                $('#message').delay(5000).fadeOut('slow');
               }
           }
        },
        error: function(data){
            console.log(data)
        }
    })
}

function changeRoomType(){
    var room_name = $('#room-name').text();
    console.log(room_name)
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
                $('#message').append("<h5>"+ data['error'] +".!</h5>")
                $('#message').delay(5000).fadeOut('slow');
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}