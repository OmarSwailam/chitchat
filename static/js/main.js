document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#all-rooms').addEventListener('click', () => loadRooms('All'));
    document.querySelector('#joined-rooms').addEventListener('click', () => loadRooms('Joined'));
    document.querySelector('#created-rooms').addEventListener('click', () => loadRooms('Created'));

    loadRooms('All');

    setTimeout(function () {
        $(".alert").delay(1000).slideUp(500, function () {
            $(this).alert('close');
        });
    }, 1000);

});


function loadRooms(roomsType) {
    let roomsView = document.querySelector('#rooms-view');
    roomsView.innerHTML = `<h3 id="rooms">${roomsType} Rooms</h3>`;
    var csrf_token = getCookie('csrftoken');
    fetch(`/rooms/${roomsType}`)
        .then(response => response.json())
        .then(rooms => {
            rooms.forEach(room => {
                console.log(room['id'])
                let newRoomDiv = document.createElement('div');
                newRoomDiv.classList.add('col-xs-12', 'col-sm-6', 'col-lg-4')
                newRoomDiv.innerHTML = `
                            <div id="card_room_${room['id']}" class="card p-3 mb-3">
                                <img src="${room['image']}" class="card-img room-image image-container-md">
                                <div class="card-body">
                                    <h5 class="card-title main-heading">${room['name']}</h5>
                                    <div class="row">
                                        <form action="join/${room['id']}" method="POST">
                                        <input type="hidden" name="csrfmiddlewaretoken" id="csrf-token" value="${csrf_token}" />
                                            <div class="row">
                                                  <div class="col-10">
                                                    <input placeholder="Password" class="form-control" name="password_${room['id']}" id="password_${room['id']}" type="password">
                                                </div>
                                                <div class="col-2">
                                                    <button id="join_${room['id']}" class="btn btn-primary">Join</button>
                                                </div>
                                            </div>

                                        </form>
                                    </div>

                                    <div class="row mt-3">
                                        <div class="col">
                                            <p class="">Already a member?</p>
                                        </div>
                                        <div class="col">
                                            <a href="room/${room['id']}" id="room_${room['id']}" class="btn btn-primary">Hop in!</a>
                                        </div>
                                    </div>

                                </div>
                            </div>
                                `
                document.querySelector('#rooms-view').append(newRoomDiv);

            });

        })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}