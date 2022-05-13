new Vue({
	el: '#app',
	data: {
		chatColor: '#0084ff',
		colorPanelShown: false,
		newMessage: '',
		tutorialSeen: false,
		colors: ['#0084ff','#ffc300','#4af844',
						 '#7646ff','#a695c7','#ff5ca1',
						 '#fa3c4c','#f56b78','#33343f'],
		messages: [
			{id: 0, text: 'Hi there', primary: false, date: moment().format('hh:mm')},
			{id: 1, text: 'Hi rob!', primary: true, date: moment().format('hh:mm')},
			{id: 2, text: 'This is better than messenger xD', primary: false, date: moment().format('hh:mm')},
			{id: 3, text: 'ofc', primary: true, date: moment().format('hh:mm')},
			{id: 4, text: 'everything is better than messenger.. XD', primary: true, date: moment().format('hh:mm')},
			{id: 2, text: 'ok, chill bro ಠ_ಠ thats just ez script made with vue.js', primary: false, date: moment().format('hh:mm')},
			{id: 4, text: 'but look how it is cute <3', primary: true, date: moment().format('hh:mm')}
		]
	},
	methods: {
		send: function(){
			if(this.newMessage.length > 0){
				let lastId = this.messages[this.messages.length-1];
				this.messages.push({id: lastId+1, text: this.newMessage, primary: true, date: moment().format('hh:mm')});
				this.newMessage = '';
				this.tutorialSeen = true;
			}
		},
		setColor: function(color){
			this.chatColor = color;
			this.colorPanelShown = false;
		}
	}
});