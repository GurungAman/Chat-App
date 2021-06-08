function check_user(){
    const csrftoken = (document.cookie).toString().split("=")[1];
    var room_name = $('#room-name').text();
    $.ajax({
        url: "/check_user/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'POST',
        data: JSON.stringify({
            "room_name": room_name,
        }),
        success: function(data){
            if(data['is_user_admin'] == false){
                window.location.href = "/"
            }
        },
        error: function(data){
            console.log(data)
            window.location.href = "/"
        }
    })
}