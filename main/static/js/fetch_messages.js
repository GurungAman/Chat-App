function addToDom(data){
    const chat_log = document.getElementById('chat-log');

    let row = document.createElement('div');
    row.classList.add("row", "mt-2")

    let col_user = document.createElement('div');
    col_user.classList.add("col-2")
    col_user.innerHTML = data.user

    let col_msg = document.createElement('div');
    col_msg.classList.add("col-9", "px-5")
    col_msg.innerHTML  = data.message
    
    row.appendChild(col_user)
    row.appendChild(col_msg)

    chat_log.prepend(row)

    
}



function loadMessages(page_number){
    console.log(page_number)
    getMessages(page_number)
    $('#chat-log').on('scroll', function() {
        var scrollTop = $(this).scrollTop();

        if (scrollTop == 0) {

            page_number++;
            getMessages(page_number)
            console.log(page_number +" here")
            }
        });

}

      

function getMessages(page_number){
    const csrftoken = (document.cookie).toString().split("=")[1];

    var room_name = JSON.parse(document.getElementById('room-name').textContent);

    $.ajax({
        url: "/get_messages/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: "POST",
        data: JSON.stringify({
            "room_name": room_name,
            "page_number": parseInt(page_number)
        }),
        success: function(data){

            if (data['status'] == true){
                for(let i=0; i<data['data'].length; i++){
                    addToDom(data['data'][i])
                }
            }
            else if(data['status'] == false){
                return;
            }
        },
        error: function(data){
            console.log(data)
        }
    })
}

