function leaveRoom(){
    var room = JSON.parse(document.getElementById('room-name').textContent);
    $.ajax({
        url: '/leave_room/',
        type: 'GET',
        data: {
            'room': room,
        },
        success: function(data){
            window.location.href('/')
        },
        error: function(data){
            console.log(data)
        }
    })
}

function createRoom(){
    var room_name = $('$room-name-input').val();
    var is_public = $('#is_public').is(':checked');
    var is_private = $('#is_private').is(':checked');
    $.ajax({
        url: '/create_chat_room/',
        type: 'POST',
        data: {
            'room_name': room_name,
            'is_private': is_private,
            'is_public': is_public

        },
        success: function(data){
            window.location.href('/chat/' + room_name)
        },
        error: function(data){
            console.log(data)
        }
    })
}
