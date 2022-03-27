const APP_ID = '38e3a9c1018e4d6ca9b60f351d15c7c5'
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))

let NAME = sessionStorage.getItem('name')

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    // display room name
    document.getElementById('room-name').innerText = CHANNEL
    // first i need to subscribe the event listener
    // When a remote user publishes an audio or video track
    // the SDK triggers the user-published event.
    // This event carries two parameters: the remote user object (user) and the media type (mediaType).
     client.on('user-published', handleUserJoined)
     client.on('user-left', handleUserLeft)

    // i need to check if i have a session or not
    // maybe not have UID or token
    try {
        // join the channel
        await client.join(APP_ID, CHANNEL, TOKEN, UID)
    } catch (error) {
        console.error(error)
        window.open('/', '_self')
    }

    // create audio and video
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    // create a room member
    let member = await createMember()


    // add audio and video to our browser
    let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                    <div class="video-player" id="user-${UID}"></div>
                  </div>`
    // now i need to insert the player to the stream
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)
    // publish audio and video to others
    await client.publish([localTracks[0], localTracks[1]])

}

let handleUserJoined = async (user, mediaType) => {
    // first i need to add remote users
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)
    // now i need to check the media type
    if (mediaType === 'video') {
        // if it's a video so i need to make a video player and display it
        // but first i need to make sure that the user doesn't already exist within our DOM
        // ex leave then join
        let player = document.getElementById(`user-container-${user.uid}`)

        if (player != null) {
            // it's exist so i need to remove it
            player.remove()
        }

        let member = await getMember(user)

        player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                  </div>`
        // now i need to insert the player to the stream
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

        user.videoTrack.play(`user-${user.uid}`)
    }
    if (mediaType === 'audio') {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    // delete a specific user
    delete remoteUsers[user.uid]
    // then delete it from the DOM
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async (user) => {
    // this function will go through local video and audio
    // and we gonna ahead and stop the tracks
    // and we will unsubscribe from the channel we joined before
    // so i need to leave the channel then redirect to the lobby

    // because local tracks are in array here so i need to loop over them
    for (let i = 0; i < localTracks.length; ++i) {
        localTracks[i].stop() // here only stop and i can continue after i stop it by reopen it
        localTracks[i].close() // close will end this operation
    }
    // then the client will leave the stream
    await client.leave()

    deleteMember()

    // then redirect to lobby
    window.open('/', '_self')
}

let toggleCamera = async (e) => {
    // i need to check local tracks first
    // localTracks[0] -> audio
    // localTracks[1] -> camera
    // i need to check if the camera is off
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false) // i will turn the camera on
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[1].setMuted(true) // i will turn the camera off
        e.target.style.backgroundColor = 'rgba(255, 80, 80, 1)'
    }
}


let toggleMic = async (e) => {
    // i need to check local tracks first
    // localTracks[0] -> audio
    // localTracks[1] -> camera
    // i need to check if the mic is off
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false) // i will turn the camera on
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[0].setMuted(true) // i will turn the camera off
        e.target.style.backgroundColor = 'rgba(255, 80, 80, 1)'
    }
}

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method:'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
    return member
}


let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}

let deleteMember = async () => {
    // must be called when user leaves or close window
    // so i must call it inside leave or remover local streams
    let response = await fetch('/delete_member/', {
        method:'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()

}

joinAndDisplayLocalStream()


// delete member from database if he close call window
window.addEventListener('beforeunload', deleteMember)

// if i click leave button 'leaveAndRemoveLocalStream' will be activated
document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
// if i click camera toggle button 'toggleCamera' will be activated
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
// if i click audio toggle button 'toggleMic' will be activated
document.getElementById('mic-btn').addEventListener('click', toggleMic)