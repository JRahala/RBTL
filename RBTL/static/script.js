var socket = io();
User = {};

// MISC INIT FUNCTION 

function init(){

	document.getElementById('welcome-card').style.display = 'block';

}

// EVENT LISTENERS

//window.addEventListener('keydown', function(event){
//	console.log('You are typing', event);
//})

// LISTENERS

socket.on('joinedRoom', function(){
	changeCard(1);
	let msg = `<b>${data.username} joined the room</b>`;
	socket.emit('chatSend', data = {user: User, msg: msg})
})

socket.on('chatRecieve', function(msg){
	addMessage(msg);
})

socket.on('roomError', function(error){
	document.getElementById('welcome-error').innerHTML = error.error; 
})

socket.on('roomInfo', function(room){
	document.getElementById('waiting-room-name').innerHTML = room.room_name;
	document.getElementById('waiting-room-host').innerHTML = room.host;

	if (room.host == User.username){
		document.getElementById('waiting-room-start').disabled = false;
	}
})

socket.on('gameStarted', function(){
	console.log('game starting');
	changeCard(index = 2);
})

socket.on('roundStart', function(data){
	console.log('starting round');
	
	let madlibFiller = '<span onclick = "fillMadlib(this)"> XXXXX </span>';
	var madlib = data.madlib.replaceAll('_', madlibFiller);

	document.getElementById('madlib').innerHTML = madlib;
})

socket.on('takenMadlib', function(data){
	index = data['index'];
	taken = document.getElementById('madlib').querySelector('span')[index];
	taken.setAttribute('data-taken', 'True');
	taken.innerHTML = '[madlib is taken]'
})

socket.on('votingStart', function(){
	console.log('start voting');
})

socket.on('roundResults', function(){
	console.log('results for round displayed');
})
// JOINING ROOM FUNCTIONS

function userData(){
	
	let username = document.getElementById('username').value;
	let room = document.getElementById('room-name').value;

	User.username = username;
	User.room = room;

	return {username: username, room: room};
}

function createRoom(){
	socket.emit('createRoom', data = userData());
}

function joinRoom(){
	socket.emit('joinRoom', data = userData());
}

// CHATTING FUNCTIONS

function chat(id){
	let msg = document.getElementById(id).value;
	socket.emit('chatSend', data = {user: User, msg: msg});
	console.log('chat sent');
}

// GAME FUNCTIONS

function startGame(){
	socket.emit('startGame', data = userData());
}

function fillMadlib(element){
	console.log(element);

	taken = element.getAttribute('data-taken');
	if taken == 'True'{
		return 0;
	}

	element.innerText = '[type your madlib]';
	element.style.color = 'red';

	User.current_madlib = element;
}

// DISPLAY FUNCTIONS

function changeCard(index){

	let cards = document.getElementsByClassName('card');
	for (i = 0; i < cards.length; i++){
		var card = cards[i];
		if (i == index){
			card.style.display = 'block';
		}
		else{
			card.style.display = 'none';
		}
	}

}

function addMessage(data){

	let chat_boxes = document.getElementsByClassName('room-chat');
	for (var chat of chat_boxes){
		chat.innerHTML += `<br><b>${data.user.username}</b>: ${data.msg}`;
	}

}



init();